# Lab 4 · Every reader, and checks in front of the agent

**Goal:** name every reader of the payments table, and stop the agent from reading bad data. **Time:** Part A 20 minutes, Part B 10 minutes.

## Part A · Every reader, named

1. Open `models/lab4_exposures.yml`. An exposure tells dbt who reads a table from outside dbt: the dashboard, the finance close, and the reorder agent.
2. Run. The `+` means "and everything built from it".

   ```bash
   uv run dbt ls --select stg_pos_payments+
   ```

   You see: three lines that start with `exposure:`, then the tables and tests.
3. Answer: which reader reads the payments table itself? Who owns each reader?
4. The reorder agent's owner is `nobody`. Write a person's name. Save (Cmd+S). Answer: why a name, and not "the team"?

## Part B · Checks in front of the agent

5. Run the agent's read command for 2 June:

   ```bash
   uv run python agent_tools.py read 2026-06-02
   ```

   You see: `Yesterday's takings: EUR 4,012.80`. That is the frozen number that the agent orders from.
6. Open `agent_tools.py`. Change `GATE = False` to `GATE = True`. Save.
7. Run step 5 again, and once for `2026-05-31`.

   You see: 31 May gives the takings, `EUR 5,481.40`. 2 June gives `HOLD: 2 checks failed`.
8. Answer: what runs now before the agent reads?

**Done early?** Run it for `2026-06-15`. How many checks fail? Is holding the order right?

**Stuck?** No `HOLD` on 2 June: save `agent_tools.py`, and check that `GATE = True`.
