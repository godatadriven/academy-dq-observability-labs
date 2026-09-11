# Lab 2 · A gate on the copy

> **10 minutes** · **Goal:** a contract that stops the copy when the amount is missing.<br>
> **You write:** the gate switched on, and two new promises.<br>
> **Done when:** `uv run tools/check.py 2` says `4 of 4 done. Well done.` Then switch it off again.

### 1 · Read the file

Open [`models/staging/lab2_contract.yml`](../models/staging/lab2_contract.yml). It is a contract: the columns that the copy promises to deliver. Here is its start:

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
| `- name: stg_pos_events` | The copy: the first dbt model. Every night it reads the payment app's events from raw, where they land as they are. An event is the message the app sends for each payment. |
| `enforced: false` | The contract is off. With `true`, dbt checks every promise when it builds the copy. |
| `- name: amount` | One promised column. |
| `data_type: integer` | Its type: a whole number, in cents. |
| `constraints:` / `- type: not_null` | A rule on the column: it can never be empty. |

When the data breaks a promise, dbt stops the build. That is the gate. On 1 June the app renamed `amount` to `amount_cents`, so the copy finds `amount` empty.

### 2 · Run the copy

```bash
uv run dbt run --select stg_pos_events
```

```
Done. PASS=1 WARN=0 ERROR=0 ...
```

The contract is off, so the empty amounts get through.

---

### 3 · Your turn

**Task.** Switch the contract on, and add two promises:

- `payment_method` can never be empty, the same way as `amount`.
- Every amount is above 0. This rule is not a `not_null`: it is the type `check`, with an `expression`.

> **Hint:** dbt's page on [constraints](https://docs.getdbt.com/reference/resource-properties/constraints) shows every type of rule, with an example of each.

Run the copy again. It stops, and the error has this line:

```bash
uv run dbt run --select stg_pos_events
```

```
Constraint Error: NOT NULL constraint failed: stg_pos_events__dbt_tmp.amount
```

### 4 · Check

```bash
uv run tools/check.py 2
```

```
4 of 4 done. Well done.
```

### 5 · Switch it off again

Change it back to `enforced: false`, and save. The next labs need the Frozen Payments in the table.

```bash
uv run dbt run
```

The last line has `ERROR=0`. Now `check.py 2` shows ✗ on "the contract is on", and `2 of 3 done`. That is correct: it is off again.

---

### Extra (optional)

Promise that `payment_id` is never in the table twice.

### Stuck?

- A ✗ line says what is wrong. Fix it, save (Cmd+S, or Ctrl+S on Windows), and check again.
- Later, `dbt run` shows `ERROR=1`: the contract is still on. Do step 5.
