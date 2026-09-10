# Lab 2 · A gate on the pipe

**8 minutes** · Stop the copy when the amount is missing.

> This page stays on the left. Click a file name to open it on the right.

### 1 · Open the contract

Open [`models/staging/lab2_contract.yml`](../models/staging/lab2_contract.yml). It lists the columns the copy promises. It is off: `enforced: false`.

### 2 · Your turn

1. Switch it on: change `enforced: false` to `enforced: true`.
2. Add a rule: `payment_method` can never be empty. Under `payment_method`, add the same two lines that `amount` has: `constraints:` and `- type: not_null`.
3. Save.

### 3 · Run the copy

```bash
uv run dbt run --select stg_pos_events
```

**You see:** `NOT NULL constraint failed ... amount`. The gate stops the copy.

### 4 · Check

```bash
uv run tools/check.py 2
```

**You see:** `3 of 3 done. Well done.`

### 5 · Switch it off again

Change it back to `enforced: false`, and save. The next labs need the Frozen Payments.

```bash
uv run dbt run
```

**Talk:** why put the gate on the copy, and not on the payments table?

**Stuck?** Later, `dbt run` shows `ERROR=1`: the contract is still on. Do step 5.
