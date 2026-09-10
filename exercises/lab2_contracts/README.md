# Lab 2 · A gate on the pipe

**Goal:** make the copy stop when the amount is missing. The Jaffle Shop did not have this gate.

## What went wrong

The copy, the model `stg_pos_events`, reads each payment from the payment app. It feeds the payments table, `stg_pos_payments`. From 1 June the app sends `amount_cents` instead of `amount`. The copy finds no `amount` and writes an empty value (NULL). The payments table then fills the empty value with the customer's last amount. Nothing fails.

## Words

- **Gate:** something that stops a bad change before it lands. In this lab, the gate is a contract.
- **Contract:** the columns and types a model promises. dbt checks them each time it builds the model.
- **Constraint:** one rule in the contract. `not_null` means the column can never be empty.

## Steps

1. Guess first: with the contract on, what happens when dbt builds the copy?
2. Open `stg_pos_events.yml`. Fill the two blanks.
3. From `jaffle_shop/`, copy it into place and build the copy:

```bash
cp ../exercises/lab2_contracts/stg_pos_events.yml models/staging/
dbt run --select stg_pos_events
```

4. Read the error out loud. That is the gate.
5. Delete the file and build everything again. Labs 3 and 4 need the copy without the gate, as the Jaffle Shop had it.

```bash
rm models/staging/stg_pos_events.yml
dbt run
```

## When it works

Step 3 stops with this error. The build stops, so no payment gets a guessed amount:

```
Constraint Error: NOT NULL constraint failed: stg_pos_events__dbt_tmp.amount
```

Step 5 ends with `Done. PASS=5`.

## If it does not work

| You see | Do this |
| --- | --- |
| `Invalid constraint type on column amount` | The blank after `type:` is still empty. |
| The build passes in step 3 | Check that the file is in `models/staging/` and that `enforced` is `true`. |
| Later, `SKIP=3` on `dbt run` | The file is still in `models/staging/`. Delete it. |
