# Lab 2 · A gate on the pipe

**Goal:** close the gate that the Jaffle Shop did not have. **Time:** 8 minutes.

> This page stays on the left. Click a file name on it, and the file opens on the right.

1. Open [`models/staging/lab2_contract.yml`](../models/staging/lab2_contract.yml). It is a contract: the columns that the copy promises. `amount` has the rule `not_null`. `enforced: false` means the contract is off.
2. Answer first: with the contract on, what happens to the 1 June events, which have no amount?
3. Change `enforced: false` to `enforced: true`. Save (Cmd+S, or Ctrl+S on Windows). Run:

   ```bash
   uv run dbt run --select stg_pos_events
   ```

   `dbt run` builds tables. `--select` builds only the copy. You see: `Constraint Error: NOT NULL constraint failed ... amount`, and a last line with `ERROR=1`. That is the stop: the copy stops. No payment gets a guessed amount.
4. Change it back to `enforced: false`. Save. Run:

   ```bash
   uv run dbt run
   ```

   You see: `PASS=5`. The contract is off again, so the later labs still have the Frozen Payments to catch.
5. Answer: why put the gate on the copy, and not on the payments table?

**Stuck?** Later, `dbt run` shows `ERROR=1 SKIP=3`: the contract is still on. Do step 4.
