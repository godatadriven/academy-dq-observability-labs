# jaffle_shop — the sandbox

dbt-labs' [jaffle_shop](https://github.com/dbt-labs/jaffle_shop_duckdb) on DuckDB, with the Frozen Payments case as real data. Every Module 2 lab runs from this folder.

## Build

```bash
uv sync
source .venv/bin/activate   # Windows: .venv\Scripts\activate. Once per terminal.
dbt deps
dbt seed
dbt run
dbt test                    # Done. PASS=4
```

## What is in it

| Name | What |
| --- | --- |
| `stg_pos_events` | The copy. It reads `amount` from each event of the payment app. |
| `stg_pos_payments` | The payments table. The note fills an empty amount with the customer's last amount, or 0. |
| `revenue_daily` | What the revenue dashboard and the finance close read. |
| `payments_repeat_rate` | Per day: how many payments equal the customer's previous one. |
| `agent_tools.py` | The reorder agent's two commands: `read` and `order`. Lab 4 changes it. |
| `reorder_agent.sh` | The reorder agent. Your trainer runs it on the day. |
| `soda/` | The Soda configuration and a demo scan. |

## NOW, the morning you scan

The sandbox holds 17 May to 17 June 2026. A Soda scan pretends to run at 09:00 on the morning you pass as `NOW`:

```bash
soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/checks.yml
```
