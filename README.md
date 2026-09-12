# Data Quality & Observability · Module 2 labs

The labs for Module 2. The case is the Frozen Payments from Module 1.

## The case in three lines

On 1 June, the Jaffle Shop's payment app renamed the field `amount` to `amount_cents`. The staging model kept reading `amount`, found nothing, and did not fail. A patch in the payments table then filled each empty amount with the customer's last amount, or with 0 for a new customer. Every test passed for seventeen days, and every amount was wrong.

```
payment app ──► raw_pos_payments ──► stg_pos_events ──► stg_pos_payments ──► revenue_daily ──► dashboard, finance close
                (raw: the events,     (staging: reads    (the payments table)                   (month-end report)
                 as they land)         the events)        the reorder agent reads the payments table too
```

## Required before the day

You must know these. The day does not teach SQL or dbt, and without them the labs are very hard to follow.

- **SQL:** you can read and write SELECT, WHERE, JOIN, and GROUP BY.
- **dbt:** you know what a model is, and what `ref()`, `dbt run`, and `dbt test` do.
- **A terminal and YAML:** you can run a command, and read a YAML file. `basics.md` shows both.
- **Module 1:** you took part in it. The labs replay its case.

New to SQL or dbt? Do one of these before the day. Both are free.

- SQL: [SQLBolt](https://sqlbolt.com/), lessons 1 to 11.
- dbt: [dbt Fundamentals](https://learn.getdbt.com/courses/dbt-fundamentals).

## Before the day

1. Follow `setup-guide.md`: open the labs in GitHub Codespaces, VS Code in your browser, in about 10 minutes.
2. Read `basics.md`: the terminal, a YAML file, and a query, in about 10 minutes.

## The labs

Each lab has one short page in `jaffle_shop/labs/`: read the file, run it, then do two tasks of your own. An Extra task is there for when you finish early. `uv run tools/check.py 1` (and so on) shows a ✓ for each part you got right, and says what is wrong for each ✗.

| Lab | You will |
| --- | --- |
| 1 | See Module 1's six defects caught by dbt tests, then write a package test and a query test. |
| 2 | Switch on a data contract that stops the staging model, and add two rules to it. |
| 3 | Write two Soda checks, and set the limit that catches the Frozen Payments. |
| 4 | Name every reader of the table, and put your checks in front of an AI agent. |
| 5 | Define revenue once, in a semantic layer, and add two metrics. |
| 6 | Write one check from your own standard, and run it in the sandbox. |

Your codespace opens on the Lab 1 page. A new terminal starts in `jaffle_shop/`. Put `uv run` in front of every command, as the lab pages do.

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
| pos | Point of sale: the payment app in the cafés. |
| `raw_` | The start of a table name in raw: the data as it landed. |
| `stg_` | The start of a table name in staging: cleaned by dbt. |
