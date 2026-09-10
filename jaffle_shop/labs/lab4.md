# Lab 4 · Every reader, and checks in front of the agent

**Part A 12 minutes, Part B 12 minutes** · Name every reader of the payments table, and stop the agent from reading bad data.

> This page stays on the left. Click a file name, and it opens on the right.

## Part A · Every reader, named

### 1 · List the readers

Open [`models/lab4_exposures.yml`](../models/lab4_exposures.yml). An exposure tells dbt who reads a table from outside dbt. The `+` means "and everything built from it".

```bash
uv run dbt ls --select stg_pos_payments+
```

**You see:** three lines that start with `exposure:`, then the tables and tests.

### 2 · Your turn

1. The reorder agent's owner is `nobody`. Change it to a person's name, and keep the `{ }` around it.
2. Add a fourth reader: the weekly email to the café managers. It reads `revenue_daily`. Copy the `revenue_dashboard` block, then change the name to `weekly_cafe_email`, the type to `application`, and the owner to a person.

Save. Then check it:

```bash
uv run check.py 4a
```

**You see:** `4 of 4 done. Well done.`

**Talk:** why a person's name, and not "the team"?

**Stop here.** Your trainer shows the agent first.

## Part B · Checks in front of the agent

### 3 · Read 2 June, without checks

```bash
uv run python agent_tools.py read 2026-06-02
```

**You see:** `Yesterday's takings: EUR 4,012.80`. The agent orders from this frozen number.

### 4 · Your turn

Open [`agent_tools.py`](../agent_tools.py). Change `GATE = False` to `GATE = True`. Save. Now your Lab 3 checks run before the agent reads.

### 5 · Check

```bash
uv run check.py 4b
```

**You see:** `3 of 3 done. Well done.` The check reads both mornings: HOLD on 2 June, the takings on 31 May.

**Done early?** Read 15 June. How many checks fail, and is holding the order right?

```bash
uv run python agent_tools.py read 2026-06-15
```

**Stuck?** "31 May: ✗": your Lab 3 limit rings on a normal day. Fix it in Lab 3 first.
