# Data Quality & Observability · Module 2 labs

The sandbox and the lab files for Module 2. The case is the Frozen Payments from Module 1: the Jaffle Shop's payment app renamed a field on 1 June, and every test stayed green for seventeen days.

## Before the day

Follow `exercises/setup-guide.md`. It takes about 30 minutes. Reply to your trainer with the last line of `dbt test`: `Done. PASS=4`.

## Folders

| Folder | What |
| --- | --- |
| `jaffle_shop/` | The sandbox: dbt on DuckDB, with the case as real data. Every command runs from here. |
| `exercises/lab1_dbt_tests/` | Lab 1. Module 1's six defects, one dbt test each. |
| `exercises/lab2_contracts/` | Lab 2. A gate on the copy. |
| `exercises/lab3_soda/` | Lab 3. Soda checks on the payments table. |
| `exercises/lab4_lineage/` | Lab 4. Every reader of the table, and a gate in front of the reorder agent. |
| `exercises/lab5_planning/` | The one check you ship, if you did not bring a standard from Module 1. |

Keep `jaffle_shop/` and `exercises/` side by side. The lab commands use paths like `../exercises/lab3_soda/checks.yml`.
