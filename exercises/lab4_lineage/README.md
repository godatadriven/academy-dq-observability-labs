# Lab 4 · Every reader, and checks in front of the agent

**Goal:** name every reader of the payments table in dbt. Then stop the reorder agent from reading bad data.

## Part A · Every reader, named

dbt knows only what is inside dbt. Three readers sit outside it: the revenue dashboard, the finance close (finance's month-end report), and the reorder agent. An **exposure** is a short YAML entry that tells dbt who reads a table from outside dbt.

1. From `jaffle_shop/`, see what dbt knows now. The `+` means "and everything built from it".

```bash
dbt ls --select stg_pos_payments+
```

2. Open `exposures.yml`. Fill the five blanks.
3. Copy it into place, and run the same command again:

```bash
cp ../exercises/lab4_lineage/exposures.yml models/
dbt ls --select stg_pos_payments+
```

**When it works:** three new lines appear at the top:

```
exposure:jaffle_shop.finance_close
exposure:jaffle_shop.ingredient_reorder_agent
exposure:jaffle_shop.revenue_dashboard
```

## Part B · Checks in front of the agent

You need your finished Lab 3 `checks.yml`, Part B included.

Every morning, the reorder agent reads yesterday's takings (the money the cafés took) with one command, then orders ingredients. Nobody checks it. You make that command run your Lab 3 checks first. If a check fails, the agent gets `HOLD` instead of the takings.

1. Open `agent_tools.py` in this folder. Fill the two blanks.
2. Copy it into place. It replaces the file there. Then test it on two mornings:

```bash
cp ../exercises/lab4_lineage/agent_tools.py .
python agent_tools.py read 2026-05-31
python agent_tools.py read 2026-06-02
```

**When it works:**

```
31 May:  Yesterday's takings: EUR 5,481.40
2 June:  HOLD: 2 checks failed. validity: every amount is in the menu's range; distribution: payments do not repeat the customer's last amount
```

Your trainer then runs the real agent with your checks in front. It gets HOLD and does not order.

## If it does not work

| You see | Do this |
| --- | --- |
| An error about `type` in `exposures.yml` | Use one of the types listed at the top of the file. |
| The exposures do not appear | The file must be in `models/`. |
| `NameError: name '___'` | Blank 2 is still empty. |
| `HOLD` on 31 May, "the scan did not finish" | Blank 1 is wrong, or your Lab 3 file still has a blank. |
| No `HOLD` on 2 June | Your Lab 3 file needs all its checks, Part B included. |

To put the agent's original file back: `git checkout agent_tools.py`
