# Lab 4 · Every reader, and checks in front of the agent

**Part A 12 minutes, Part B 12 minutes** · Name every reader of the payments table, and stop the agent from reading bad data.

> This page stays on the left. Click a file name to open it on the right.

## Part A · Every reader, named

### 1 · List the readers

Open [`models/lab4_exposures.yml`](../models/lab4_exposures.yml). An exposure tells dbt who reads a table from outside dbt.

```bash
uv run dbt ls --select stg_pos_payments+
```

**You see:** three lines that start with `exposure:`.

### 2 · Your turn

1. The agent's owner is `nobody`. Change it to a person's name.
2. Add a fourth reader: the weekly email to the café managers. Copy the `revenue_dashboard` block. Change the name to `weekly_cafe_email`, the type to `application`, and the owner to a person.
3. Save, and check:

```bash
uv run check.py 4a
```

**You see:** `4 of 4 done. Well done.`

**Stop here.** Your trainer shows the agent first.

## Part B · Checks in front of the agent

### 3 · Read 2 June

```bash
uv run python agent_tools.py read 2026-06-02
```

**You see:** `EUR 4,012.80`. The agent orders from this frozen number.

### 4 · Your turn

Open [`agent_tools.py`](../agent_tools.py). Change `GATE = False` to `GATE = True`. Save, and check:

```bash
uv run check.py 4b
```

**You see:** `3 of 3 done. Well done.` Now the agent gets HOLD on 2 June.

**Talk:** why a person's name as owner, and not "the team"?

**Stuck?** "31 May: ✗": your Lab 3 limit is too tight. Fix it in Lab 3 first.
