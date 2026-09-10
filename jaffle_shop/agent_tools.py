"""The reorder agent's two tools. Module 1, slide 9: "an agent reorders stock ... Nobody looks."

    python agent_tools.py read 2026-06-02            yesterday's takings, for the morning of 2 June
    python agent_tools.py order 161 "why this amount" tomorrow's order

The agent (reorder_agent.sh) can run these two commands and nothing else.
With GATE = False, this is the Jaffle Shop's version: read hands the agent whatever the table says.
"""
import subprocess
import sys

import duckdb

# LAB 4 · Part B · Checks in front of the agent                     Time: 10 minutes
#
# Goal: stop the reorder agent from reading bad data.
# You learn: how to run your Soda checks before an AI agent acts, and what an exit code is.
# You need your finished soda/lab3_checks.yml, Part B included.
#
# Every morning, the reorder agent reads yesterday's takings (the money the cafés took) with one
# command, then orders ingredients. Nobody checks it. You make that command run your Lab 3 checks
# first. If a check fails, the agent gets HOLD instead of the takings.
#
# Steps
#   1. Switch the gate on: below, change GATE = False to GATE = True.
#   2. Fill the two blanks in run_checks.
#   3. Test it on two mornings:
#        python agent_tools.py read 2026-05-31
#        python agent_tools.py read 2026-06-02
#
# When it works:
#   31 May:  Yesterday's takings: EUR 5,481.40
#   2 June:  HOLD: 2 checks failed. validity: every amount is in the menu's range; distribution: payments do not repeat the customer's last amount
# Your trainer then runs the real agent with your checks in front. It gets HOLD and does not order.
# Stuck? LABS.md, Lab 4. To start over: git checkout agent_tools.py
# Done early? Run it for 15 June. How many checks fail, and is holding the order right?
GATE = False


def run_checks(day: str) -> list[str]:
    """Run the Lab 3 scan for the morning of `day`. Return the names of the failed checks."""
    scan = subprocess.run(
        ["soda", "scan", "-d", "jaffle_shop", "-c", "soda/configuration.yml",
         "-v", f"NOW={day} 09:00:00", "______"],        # blank 1: the checks file, as in the Lab 3 scan command
        capture_output=True, text=True,
    )
    if scan.returncode == ___:                           # blank 2: a scan ends with a number, its exit code.
                                                         # Soda: 0 = every check passed, 1 = a warning,
                                                         # 2 = a check failed, 3 = an error.
                                                         # return [] means: no check failed. So write the
                                                         # exit code for "every check passed".
        return []
    failed = [line.split("]", 1)[1].replace("[FAILED]", "").strip()
              for line in scan.stdout.splitlines() if "[FAILED]" in line]
    return failed or [f"the scan did not finish (exit code {scan.returncode})"]


def read_takings(day: str) -> str:
    """Yesterday's takings, as the payments table has them, on the morning of `day`."""
    if GATE:
        failed = run_checks(day=day)
        if failed:
            return f"HOLD: {len(failed)} checks failed. " + "; ".join(failed)
    con = duckdb.connect("jaffle_shop.duckdb", read_only=True)
    takings = con.execute(
        "select sum(amount) / 100.0 from stg_pos_payments where paid_at::date = cast(? as date) - 1",
        [day],
    ).fetchone()[0] or 0
    con.close()
    return f"Yesterday's takings: EUR {takings:,.2f}"


def place_order(kg: int, reason: str) -> str:
    """Order tomorrow's ingredients. In the sandbox, the order is a line on the screen."""
    return f"ORDER PLACED: {kg} kg of ingredients. {reason}"


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "read" and len(sys.argv) == 3:
        print(read_takings(day=sys.argv[2]))
    elif command == "order" and len(sys.argv) >= 3:
        print(place_order(kg=int(sys.argv[2]), reason=" ".join(sys.argv[3:])))
    else:
        sys.exit('Use: python agent_tools.py read 2026-06-02   or   python agent_tools.py order 161 "reason"')
