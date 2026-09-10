"""The reorder agent's two tools. Module 1, slide 9: "an agent reorders stock ... Nobody looks."

    python tools/agent_tools.py read 2026-06-02            yesterday's takings, for the morning of 2 June
    python tools/agent_tools.py order 161 "why this amount" tomorrow's order

The agent (tools/reorder_agent.sh) can run these two commands and nothing else.
"""
import subprocess
import sys

import duckdb

# Lab 4 · The gate: run your Lab 3 checks before the agent reads. The steps: labs/lab4.md
# False: the agent reads whatever the table says, as at the Jaffle Shop.
# True: if a check fails, the agent gets HOLD instead of the takings.
GATE = False


def run_checks(day: str) -> list[str]:
    """Run the Lab 3 scan for the morning of `day`. Return the names of the failed checks."""
    scan = subprocess.run(
        ["soda", "scan", "-d", "jaffle_shop", "-c", "soda/configuration.yml",
         "-v", f"NOW={day} 09:00:00", "soda/lab3_checks.yml", "soda/lab3_repeat.yml"],
        capture_output=True, text=True,
    )
    if scan.returncode == 0:  # Soda ends with 0 when every check passed
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
        sys.exit('Use: python tools/agent_tools.py read 2026-06-02   or   python tools/agent_tools.py order 161 "reason"')
