# Lab 2 · A data contract on the staging model

> **10 minutes** · **Goal:** a data contract that stops two bad changes: an empty amount, and an amount of the wrong type.<br>
> **You write:** the data contract switched on, and a teammate's hotfix to test it.<br>
> **Done when:** `uv run tools/check.py 2` says `3 of 3 done. Well done.` Then put both back.

### 1 · Read the file

Open [`models/staging/lab2_contract.yml`](../models/staging/lab2_contract.yml). It is a data contract: the columns that `stg_pos_events` promises to deliver. dbt calls it a model contract. Here is its start:

```yaml
models:
  - name: stg_pos_events
    config:
      contract:
        enforced: false
    columns:
      - name: amount
        data_type: integer
        constraints:
          - type: not_null
```

| Line | What it means |
| --- | --- |
| `- name: stg_pos_events` | The staging model that reads the events: the first dbt model. Every night it reads the payment app's events from raw, where they land as they are. An event is the message the app sends for each payment. |
| `enforced: false` | The data contract is off. With `true`, dbt checks every promise when it builds this model. |
| `- name: amount` | One promised column. |
| `data_type: integer` | Its type: a whole number, in cents. |
| `constraints:` / `- type: not_null` | A rule on the column: it can never be empty. |

When the data breaks a promise, dbt stops the build. On 1 June the app renamed `amount` to `amount_cents`, so `stg_pos_events` finds `amount` empty.

### 2 · Build the staging model

```bash
uv run dbt run --select stg_pos_events
```

```
Done. PASS=1 WARN=0 ERROR=0 ...
```

The data contract is off, so the empty amounts get through.

---

### 3 · Your turn

**Task 1.** Switch the data contract on: `enforced: true`. Save, and build it again:

```bash
uv run dbt run --select stg_pos_events
```

It stops, and the error has this line. The empty amounts never land.

```
Constraint Error: NOT NULL constraint failed: stg_pos_events__dbt_tmp.amount
```

**Task 2.** A teammate sees the empty amounts and ships a quick hotfix: read `amount`, or else `amount_cents`. Open [`models/staging/stg_pos_events.sql`](../models/staging/stg_pos_events.sql). Replace line 10, the `amount` line, with their line:

```sql
    cast(coalesce(json_extract_string(event, '$.amount'), json_extract_string(event, '$.amount_cents')) as decimal(12, 2)) as amount,
```

Save, and build again. No amount is empty now, so a `not_null` test would pass. The data contract stops it anyway:

```
| amount      | DECIMAL(12,2)   | INTEGER       | data type mismatch |
```

The data contract promised whole cents. The hotfix gives decimals, and it mixes euros (`7.30`) with cents (`450`).

> **Hint:** dbt's page on [model contracts](https://docs.getdbt.com/docs/mesh/govern/model-contracts) explains what dbt compares before it builds.

### 4 · Check

```bash
uv run tools/check.py 2
```

```
3 of 3 done. Well done.
```

### 5 · Put both back

Undo the hotfix, and switch the data contract off again. The next labs need the Frozen Payments in the table.

```bash
git checkout models/staging/stg_pos_events.sql
```

Change `enforced: true` back to `enforced: false`, and save. Then:

```bash
uv run dbt run
```

The last line has `ERROR=0`. Now `check.py 2` shows ✗ lines. That is correct: both are back.

---

### Extra (optional)

Promise that `payment_id` is never in the table twice.

### Stuck?

- A ✗ line says what is wrong. Fix it, save (Cmd+S, or Ctrl+S on Windows), and check again.
- Later, `dbt run` shows `ERROR=1`: the data contract is still on, or the hotfix is still in. Do step 5.
