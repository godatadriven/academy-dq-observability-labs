# Lab 4 · Every reader, and checks in front of the agent

> **Part A 12 minutes, Part B 12 minutes** · **Goal:** name every reader of the payments table, and stop the agent from reading bad data.<br>
> **You write:** Part A, owners and a new reader. Part B, your checks in front of the agent.<br>
> **Done when:** `uv run tools/check.py 4a`, then `uv run tools/check.py 4b`, say `Well done.`

## Part A · Every reader, named

### 1 · Read the file

Open [`models/lab4_exposures.yml`](../models/lab4_exposures.yml). An exposure tells dbt about a reader outside dbt: a dashboard, a report, an agent. Here is the first:

```yaml
exposures:
  - name: revenue_dashboard
    type: dashboard
    owner: {name: Sam}
    depends_on: [ref('revenue_daily')]
```

| Line | What it means |
| --- | --- |
| `- name: revenue_dashboard` | The reader. |
| `type: dashboard` | What kind of reader it is. |
| `owner: {name: Sam}` | The person who answers for it: Sam, in finance. |
| `depends_on: [ref('revenue_daily')]` | The table it reads. `ref('...')` is how dbt names a table. |

### 2 · List the readers

`stg_pos_payments+` means: the payments table, and everything that reads from it.

```bash
uv run dbt ls --select stg_pos_payments+ --resource-type exposure
```

```
exposure:jaffle_shop.finance_close
exposure:jaffle_shop.ingredient_reorder_agent
exposure:jaffle_shop.revenue_dashboard
```

---

### 3 · Your turn

**Task.** Every reader needs a person as owner, and one reader is missing:

- The agent's owner is `nobody`. Give it a person.
- Add a fourth reader: the weekly email to the café managers. It reads `revenue_daily`, and a person owns it. Add it at the end of the file, after an empty line.

> **Hint:** dbt's page on [exposures](https://docs.getdbt.com/docs/build/exposures) lists every field. For the type, an email is an `application`.

### 4 · Check

```bash
uv run tools/check.py 4a
```

```
4 of 4 done. Well done.
```

**Extra (optional).** The weekly email also shows the bank deposits. Make it read `revenue_daily` and `bank_deposits`.

> **Stop here.** Your trainer shows the agent first.

---

## Part B · Checks in front of the agent

### 5 · Read the agent's numbers

The reorder agent orders tomorrow's ingredients from yesterday's revenue: the money the cafés took. This is what it reads on the morning of 2 June:

```bash
uv run python tools/agent_tools.py read 2026-06-02
```

```
Yesterday's revenue: EUR 4,012.80
```

It looks normal, but it is built from frozen amounts. The agent orders from it.

---

### 6 · Your turn

Open [`tools/agent_tools.py`](../tools/agent_tools.py). Line 16 is the switch: `CHECKS_FIRST = False`. With `CHECKS_FIRST = True`, the agent first runs your Lab 3 checks for that morning. If a check fails, the agent gets HOLD instead of the revenue.

**Task.** Set `CHECKS_FIRST = True`, and save.

### 7 · Check

```bash
uv run tools/check.py 4b
```

```
3 of 3 done. Well done.
```

The agent gets HOLD on 2 June. On the morning of 31 May, it still gets the revenue.

### Stuck?

- A ✗ line says what is wrong. Fix it, save (Cmd+S, or Ctrl+S on Windows), and check again.
- "31 May: ✗": one of your Lab 3 checks fails on a normal day. Check your Lab 3 levels.
