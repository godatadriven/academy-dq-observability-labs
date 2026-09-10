"""The reorder agent's two tools. Module 1, slide 9: "an agent reorders stock ... Nobody looks."

    python agent_tools.py read 2026-06-02            yesterday's takings, for the morning of 2 June
    python agent_tools.py order 161 "why this amount" tomorrow's order

The agent (reorder_agent.sh) may run these two commands and nothing else.
This is the Jaffle Shop's version: no gate. read hands the agent whatever the table says.
Lab 4, part 2 replaces this file with ../exercises/lab4_lineage/agent_tools.py.
"""
import sys

import duckdb


def read_takings(day: str) -> str:
    """Yesterday's takings, as the payments table has them, on the morning of `day`."""
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
