# The labs

Every lab file is already in this folder, in the place where dbt or Soda reads it. Most start switched off, so that their blanks cannot break the other commands. You open the file, switch it on, fill the blanks, and run it. You copy nothing.

Run every command in the VS Code terminal. The last folder name in the prompt must be `jaffle_shop`, and `(jaffle-shop-dq)` must be at the start of the line.

| Lab | Open this file | Run | Time |
| --- | --- | --- | --- |
| 1 · Six defects, six tests | `seeds/lab1_extract_tests.yml`, then `tests/lab1_updated_before_placed.sql` | `dbt test --select orders_daily_extract` | 30 min |
| 2 · A gate on the pipe | `models/staging/lab2_contract.yml` | `dbt run --select stg_pos_events` | 10 min |
| 3 · Checks on the payments table | `soda/lab3_checks.yml` | the `soda scan` command at the top of the file | 25 + 15 min |
| 4 · Every reader, and checks in front of the agent | `models/lab4_exposures.yml`, then `agent_tools.py` | `dbt ls --select stg_pos_payments+`, then `python agent_tools.py read 2026-06-02` | 20 + 10 min |
| 5 · The one check you ship | `lab5_worksheet.md` | nothing to run | 12 min |

## The commands in the table

- `dbt test --select X` runs only the tests on X. Without `--select`, dbt runs everything.
- `dbt run --select X` builds only X.
- `dbt ls --select X+` lists X and everything that dbt knows reads from it. The `+` means "and everything built from it".
- `dbt show --select X`, or `dbt show --inline "select ..."`, prints some rows of a table.
- `soda scan ... -v NOW="2026-05-31 09:00:00" soda/lab3_checks.yml` runs the checks in that file. `-v NOW=...` sets `NOW`, and the file uses it as `${NOW}`.
- `python agent_tools.py read 2026-06-02` runs the agent's read command for the morning of 2 June.

## How a lab works

1. **Open** the file. The steps are in the comment at the top.
2. **Switch it on.** How depends on the file:
   - A YAML file: select every line below the `START` line, then press Cmd+/ (Windows: Ctrl+/). The `#` at the start of each line goes away.
   - A SQL file: on the first line, change `enabled=false` to `enabled=true`.
   - `agent_tools.py`: change `GATE = False` to `GATE = True`.
   - Soda's `lab3_checks.yml`: nothing to switch on. Soda reads it only when you scan.
3. **Fill** the blanks: `______` or `___`. Replace only the blank. Keep the spaces and the quotes around it.
4. **Run** the command. Save the file first: Cmd+S (Windows: Ctrl+S).
5. **Compare** the last line with "When it works" in the file. Not the same? Fix the blank and run again.

To start a lab over, run `git checkout` and the file name, for example `git checkout seeds/lab1_extract_tests.yml`. The file goes back to how it was, switched off.

## If it does not work

### Every lab

| You see | Do this |
| --- | --- |
| `dbt: command not found` or `soda: command not found` | The terminal is not activated. Run `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`). |
| An error with `______` or `___` in it | A blank is still empty. The error names the file. |
| An error in a file of a lab you did not start | You switched on a file too early. Switch it off again with Cmd+/, or run `git checkout` and the file name. |
| Nothing changed after your fix | Save the file, then run the command again. |

### Lab 1

| You see | Do this |
| --- | --- |
| Five lines say `FAIL 1`, not six | `tests/lab1_updated_before_placed.sql` is still switched off. Change `false` to `true` on its first line. |
| `Syntax error near line 44` or an error about an escape | In the pattern, write each backslash twice: `\\.` |
| A test says `PASS` | One of your blanks is wrong. Read the rule in the comment again. |
| Every line after `START` still starts with `#` | The file is still switched off. Select the lines below `START` and press Cmd+/. |

### Lab 2

| You see | Do this |
| --- | --- |
| `Invalid constraint type on column amount` | The blank after `type:` is still empty. |
| The build passes in step 4 | The file is still switched off, or `enforced` is not `true`. |
| Later, `dbt run` shows `ERROR=1 SKIP=3` | The contract is still switched on. Switch the file off with Cmd+/, then run `dbt run`. |

### Lab 3

| You see | Do this |
| --- | --- |
| `Configuration path ... does not exist` | You are in the wrong folder. Open a new terminal in VS Code. |
| An error about `${NOW}` | The `-v NOW="..."` part is missing from the command. |
| Freshness fails on 31 May | The limit is too small. Use `1d`. |
| Volume fails on 31 May | Make the band wider, and keep the `filter` line. It counts only one day. |
| A YAML error in Part B | A `#` or a space is left at the start of a line. `checks for` starts at the very start of the line. |
| The repeat check passes on 2 June | The threshold is too high. |

### Lab 4

| You see | Do this |
| --- | --- |
| An error about `type` in `lab4_exposures.yml` | Use one of the types listed at the top of the list. |
| The exposures do not appear | The file is still switched off. |
| `NameError: name '___'` | Blank 2 in `agent_tools.py` is still empty. |
| `HOLD` on 31 May, "the scan did not finish" | Blank 1 is wrong, or `soda/lab3_checks.yml` still has a blank. |
| No `HOLD` on 2 June | `GATE` is still `False`, or your Lab 3 file needs all its checks, Part B included. |
