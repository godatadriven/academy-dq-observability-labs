"""Lab 4, Part B · Checks in front of the reorder agent. The steps are in README.md.

The agent reads the payments table with `python agent_tools.py read`, then orders.
This version runs your Lab 3 checks first. If a check fails, the agent gets HOLD.
Fill the two blanks below.
"""
import subprocess
import sys

import duckdb


def run_checks(day: str) -> list[str]:
    """Run the Lab 3 scan for the morning of `day`. Return the names of the failed checks."""
    scan = subprocess.run(
        ["soda", "scan", "-d", "jaffle_shop", "-c", "soda/configuration.yml",
         "-v", f"NOW={day} 09:00:00", "______"],        # blank 1: the same checks-file path as in the Lab 3 scan command
        capture_output=True, text=True,
    )
    if scan.returncode == ___:                           # blank 2: every program ends with a number, its exit code.
                                                         # Find it: run a scan that passes, then run: echo $?
        return []
    failed = [line.split("]", 1)[1].replace("[FAILED]", "").strip()
              for line in scan.stdout.splitlines() if "[FAILED]" in line]
    return failed or [f"the scan did not finish (exit code {scan.returncode})"]


def read_takings(day: str) -> str:
    """Yesterday's takings, as the payments table has them, on the morning of `day`."""
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
