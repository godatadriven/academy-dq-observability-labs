# Lab 2 · A gate on the pipe

**8 minutes** · Close the gate that the Jaffle Shop did not have.

> This page stays on the left. Click a file name, and it opens on the right.

### 1 · Open the contract

Open [`models/staging/lab2_contract.yml`](../models/staging/lab2_contract.yml). It lists the columns the copy promises. `amount` has the rule `not_null`. `enforced: false` means the contract is off.

**Talk:** with the contract on, what happens to the 1 June events, which have no amount?

### 2 · Your turn

1. Switch the contract on: change `enforced: false` to `enforced: true`.
2. Add a second rule: `payment_method` can never be empty. Under `payment_method`, add `constraints:` with `- type: not_null`, like `amount` has.

Save.

### 3 · Run the copy

```bash
uv run dbt run --select stg_pos_events
```

**You see:** `Constraint Error: NOT NULL constraint failed ... amount`, and a red last line with `ERROR=1`. That is the gate: the copy stops.

### 4 · Check

```bash
uv run check.py 2
```

**You see:** `3 of 3 done. Well done.`

### 5 · Switch it off again

Change it back to `enforced: false`. Save. The later labs need the Frozen Payments.

```bash
uv run dbt run
```

**You see:** `PASS=6`, and `ERROR=0`.

**Stuck?** Later, `dbt run` shows `ERROR=1 SKIP=3`: the contract is still on. Do step 5.
