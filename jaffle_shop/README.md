# jaffle_shop — the sandbox

dbt-labs' [jaffle_shop](https://github.com/dbt-labs/jaffle_shop_duckdb) on DuckDB, with the Frozen Payments case as real data. Every Module 2 lab runs from this folder.

## Build

```bash
uv run tools/build.py
```

The last line is `Ready. Module 1's four tests pass, and Soda can read the tables.` The steps, and what to do when it does not work, are in `../setup-guide.md`.

## What is in it

| Name | What |
| --- | --- |
| `labs/` | One short page per lab. Start here. |
| `models/` | The SQL files dbt builds, and the YAML for Labs 2, 4, and 5. |
| `seeds/` | The CSV files dbt loads, and Lab 1's tests. |
| `soda/` | The Soda connection, the setup check, Lab 3's checks, and `my_check.yml` for Lab 6. |
| `tests/` | Lab 1's query tests, and `my_check.sql` for Lab 6. |
| `tools/` | What runs the labs: `build.py`, `check.py`, the reorder agent (`agent_tools.py`, `reorder_agent.sh`), and `generate_feed.py`, which made the data. You open it only in Lab 4. |

The tables:

| Table | What |
| --- | --- |
| `stg_pos_events` | The copy. It reads `amount` from each event of the payment app. |
| `stg_pos_payments` | The payments table. It fills an empty amount with the customer's last amount, or 0. |
| `revenue_daily` | What the revenue dashboard and the finance close read. |
| `payments_repeat_rate` | Per day: how many payments equal the customer's previous one. |

VS Code hides the files that dbt and uv make or need, like `target/` and `profiles.yml`. They are still there. `selectors.yml` makes a plain `dbt test` skip the lab tests: Lab 1's fail on purpose, and the ones you write may not be ready yet.

## NOW, the morning you scan

The sandbox holds 17 May to 17 June 2026. A Soda scan pretends to run at 09:00 on the morning you pass as `NOW`. This scan runs the setup check:

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/setup_check.yml
```

Lab 3 uses the same command with `soda/lab3_checks.yml` and `soda/lab3_repeat.yml`.
