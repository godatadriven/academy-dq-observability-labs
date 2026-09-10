# Data Quality & Observability · Module 2 labs

The labs for Module 2. The case is the Frozen Payments from Module 1.

## The case in three lines

On 1 June, the Jaffle Shop's payment app renamed the field `amount` to `amount_cents`. The copy kept reading `amount`, found nothing, and did not fail. The payments table then filled each empty amount with the customer's last amount, or with 0 for a new customer. Every test passed for seventeen days, and every amount was wrong.

```
payment app ──► stg_pos_events ──► stg_pos_payments ──► revenue_daily ──► dashboard, finance close (month-end report)
                (the copy)         (the payments table)                   the reorder agent reads the payments table too
```

## Before the day

Follow `exercises/setup-guide.md`. It takes about 30 minutes.

## The labs

Do them in this order. Each folder has a `README.md` with the steps.

| Lab | Folder | You will |
| --- | --- | --- |
| 1 | `exercises/lab1_dbt_tests/` | Write one dbt test for each of Module 1's six defects. |
| 2 | `exercises/lab2_contracts/` | Stop the copy when the amount is missing. |
| 3 | `exercises/lab3_soda/` | Write Soda checks, and catch the Frozen Payments. |
| 4 | `exercises/lab4_lineage/` | Name every reader of the table, and put your checks in front of an AI agent. |
| 5 | `exercises/lab5_planning/` | Write one check for your own work. |

Run every command from `jaffle_shop/`, in a terminal where you ran `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`). Do not move the folders. Some commands use `../exercises/`.

## Words

| Word | Meaning |
| --- | --- |
| dbt | A tool that builds tables from SQL files, and tests them. |
| Soda | A tool that checks a table and says PASSED or FAILED for each rule. |
| Model | A SQL file in `jaffle_shop/models/`. dbt turns it into a table. |
| Seed | A CSV file that dbt loads as a table. |
| Test | A dbt rule about a table. It passes or fails each time you run `dbt test`. |
| Check | A Soda rule about a table. |
| Scan | Soda runs your checks once. |
| The payments table | `stg_pos_payments`. Every lab looks at it. |
