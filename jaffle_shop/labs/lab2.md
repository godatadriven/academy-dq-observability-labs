# Lab 2 · A gate on the copy

**10 minutes** · Switch on a contract, so the copy stops when the amount is missing.

> This page stays on the left. Click a file name to open it on the right.

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
| `- name: stg_pos_events` | The copy: the model that reads the payment app's events every night. A model is a SQL file that dbt turns into a table. |
| `enforced: false` | The contract is off. When it is `true`, dbt checks every promise when it builds the copy. |
| `- name: amount` | One promised column. |
| `data_type: integer` | Its type: a whole number, in cents. |
| `constraints:` / `- type: not_null` | A rule on the column: it can never be empty. |

When the data breaks a promise, dbt stops the build. That is the gate. On 1 June, the app renamed `amount` to `amount_cents`, so the copy finds `amount` empty.

### 2 · Run the copy

```bash
uv run dbt run --select stg_pos_events
```

**You see:** `PASS=1`. The contract is off, so the empty amounts get through.

### 3 · Your turn

**Task A.** Switch the contract on. Then promise that `payment_method` can never be empty, the same way as `amount`.

**Task B.** Promise that every amount is above 0. This rule is new: it is not a `not_null`.

**Hint:** dbt's page on [constraints](https://docs.getdbt.com/reference/resource-properties/constraints) shows every type of rule. Task B uses the type `check`, with an `expression`.

Run the copy again:

```bash
uv run dbt run --select stg_pos_events
```

**You see:** `NOT NULL constraint failed ... amount`, in red. The gate stops the copy.

### 4 · Check

```bash
uv run tools/check.py 2
```

**You see:** `4 of 4 done. Well done.`

### 5 · Switch it off again

Change it back to `enforced: false`, and save. The next labs need the Frozen Payments in the table.

```bash
uv run dbt run
```

**You see:** `ERROR=0`.

### Extra

Promise that `payment_id` is never in the table twice. `check.py 2` shows it on the Extra line.

**Stuck?** Later, `dbt run` shows `ERROR=1`: the contract is still on. Do step 5.
