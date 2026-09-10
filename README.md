# Data Quality & Observability · Module 2 labs

The labs for Module 2. The case is the Frozen Payments from Module 1.

## The case in three lines

On 1 June, the Jaffle Shop's payment app renamed the field `amount` to `amount_cents`. The copy kept reading `amount`, found nothing, and did not fail. The payments table then filled each empty amount with the customer's last amount, or with 0 for a new customer. Every test passed for seventeen days, and every amount was wrong.

```
payment app ──► stg_pos_events ──► stg_pos_payments ──► revenue_daily ──► dashboard, finance close (month-end report)
                (the copy)         (the payments table)                   the reorder agent reads the payments table too
```

## Before the day

Follow `setup-guide.md`. Part 1 installs the labs, in about 45 minutes. Part 2 shows how the labs work: the terminal, a YAML file, and the folders, in about 10 minutes.

## The labs

Each lab has one short page in `jaffle_shop/labs/`: the steps, what you see, and the questions. The lab files are complete. You run them, read the result, and change one value.

| Lab | You will |
| --- | --- |
| 1 | See Module 1's six defects caught by six dbt tests. |
| 2 | Switch on a contract that stops the copy when the amount is missing. |
| 3 | Scan three mornings with Soda, and see the Frozen Payments caught. |
| 4 | Name every reader of the table, and put the checks in front of an AI agent. |
| 5 | Write one check for your own work. |

Work in one VS Code window: open the whole `dq-observability-labs` folder. A new terminal starts in `jaffle_shop/`. Put `uv run` in front of every command, for example `uv run dbt test`.

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
