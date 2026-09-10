# jaffle_shop — the sandbox

dbt-labs' [jaffle_shop](https://github.com/dbt-labs/jaffle_shop_duckdb) on DuckDB, with the Frozen Payments case as real data. Every Module 2 lab runs from this folder.

## Build

```bash
uv run build.py
```

The last line is `Ready. Module 1's four tests pass, and Soda can read the tables.` The steps, and what to do when it does not work, are in `../setup-guide.md`.

## What is in it

| Name | What |
| --- | --- |
| `stg_pos_events` | The copy. It reads `amount` from each event of the payment app. |
| `stg_pos_payments` | The payments table. The note fills an empty amount with the customer's last amount, or 0. |
| `revenue_daily` | What the revenue dashboard and the finance close read. |
| `payments_repeat_rate` | Per day: how many payments equal the customer's previous one. |
| `agent_tools.py` | The reorder agent's two commands: `read` and `order`. Lab 4 switches on its gate. |
| `reorder_agent.sh` | The reorder agent. Your trainer runs it on the day. |
| `soda/` | The Soda connection, the setup check, and Lab 3's checks. |
| `build.py` | Builds the sandbox in one go: `uv run build.py`. |
| `labs/` | One short page per lab. |
| `check.py` | Checks your lab work: `uv run check.py 1`. A ✓ for each part you got right. |
| `models/lab6_semantic.yml` | The semantic layer: the metric `revenue`, defined once. Lab 6. |
| `selectors.yml` | Makes a plain `dbt test` skip Lab 1's tests, which fail on purpose. |

## NOW, the morning you scan

The sandbox holds 17 May to 17 June 2026. A Soda scan pretends to run at 09:00 on the morning you pass as `NOW`. This scan runs the setup check:

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/setup_check.yml
```

Lab 3 uses the same command with `soda/lab3_checks.yml` and `soda/lab3_repeat.yml`.
