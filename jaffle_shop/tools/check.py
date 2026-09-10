"""Check your lab work. Run it from this folder, with the lab and part:

    uv run tools/check.py 1        Lab 1
    uv run tools/check.py 3a       Lab 3, Part A

Each line says ✓ when that part is right, or ✗ with what to do next.
"""
import re
import subprocess
import sys

import duckdb
import yaml


def run(*command: str) -> str:
    result = subprocess.run(command, capture_output=True, text=True)
    return re.sub(r"\x1b\[[0-9;]*m", "", result.stdout + result.stderr)


def show(done: bool, what: str, todo: str = "") -> bool:
    print(f"  {'✓' if done else '✗'} {what}")
    if not done and todo:
        print(f"      {todo}")
    return done


def read_yaml(path: str):
    try:
        return yaml.safe_load(open(path)) or {}
    except yaml.YAMLError as error:
        print(f"  ✗ {path} is not valid YAML: {str(error).splitlines()[0]}")
        print("      Check the spaces at the start of the lines you changed.")
        return None


def query(sql: str):
    con = duckdb.connect("jaffle_shop.duckdb", read_only=True)
    rows = con.execute(sql).fetchall()
    con.close()
    return rows


def lab1() -> list[bool]:
    out = run("dbt", "test", "--select", "orders_daily_extract")
    failed = [line for line in out.splitlines() if "FAIL 1" in line]
    six = ["not_null_orders_daily_extract_email", "match_regex", "order_total__0", "compound_columns",
           "recent_data", "lab1_updated_before_placed"]
    yours = [line for line in failed if "be_between" in line and "order_total" in line and "order_total__0 " not in line
             and not line.rstrip().endswith("order_total__0")]
    return [
        show(all(any(t in line for line in failed) for t in six), "Module 1's six defects: six tests fail",
             "Keep the six tests as they are. Run step 1 of the lab page."),
        show(len(yours) >= 1, "Your turn: a new test that no order is above 1,000, failing on C-1045",
             "Under order_total, add a second test like the first, with 'max_value: 1000'. Keep the first one."),
    ]


def lab2() -> list[bool]:
    contract = read_yaml("models/staging/lab2_contract.yml")
    if contract is None:
        return [False]
    model = contract["models"][0]
    on = model.get("config", {}).get("contract", {}).get("enforced") is True
    method = next((c for c in model["columns"] if c["name"] == "payment_method"), {})
    rule = any(c.get("type") == "not_null" for c in method.get("constraints", []) or [])
    results = [
        show(on, "Your turn: the contract is on", "Set 'enforced: true'. Save, and check again."),
        show(rule, "Your turn: payment_method can never be empty",
             "Under payment_method, add 'constraints:' with '- type: not_null', like amount has."),
    ]
    if on:
        out = run("dbt", "run", "--select", "stg_pos_events")
        results.append(show("NOT NULL constraint failed" in out, "The gate stops the copy on the 1 June events",
                            "Read the error above. Check the spaces in the lines you added."))
    return results


def lab3a() -> list[bool]:
    checks = read_yaml("soda/lab3_checks.yml")
    if checks is None:
        return [False]
    lines = [list(c)[0] if isinstance(c, dict) else c for c in checks.get("checks for stg_pos_payments", [])]
    has_it = any(re.search(r"missing_count\(\s*customer_id\s*\)\s*=\s*0", str(line)) for line in lines)
    out = run("soda", "scan", "-d", "jaffle_shop", "-c", "soda/configuration.yml",
              "-v", "NOW=2026-05-31 09:00:00", "soda/lab3_checks.yml")
    return [
        show(has_it, "Your turn: a fourth check, every payment has a customer",
             "Add '- missing_count(customer_id) = 0:' with a name, like the other checks."),
        show("All is good" in out and (not has_it or "4/4 checks PASSED" in out),
             "All checks pass on 31 May", "Read the scan: run Part A's command."),
    ]


def lab3b() -> list[bool]:
    match = re.search(r"repeat_rate\s*<\s*([0-9.]+)", open("soda/lab3_repeat.yml").read())
    limit = float(match.group(1)) if match else None
    rates = dict(query("select pay_date::varchar, repeat_rate_pct from payments_repeat_rate "
                       "where pay_date between '2026-05-17' and '2026-06-01'"))
    may = {day: rate for day, rate in rates.items() if day < "2026-06-01"}
    loudest = max(may, key=may.get)
    return [
        show(limit is not None and all(rate < limit for rate in may.values()),
             "Your turn: quiet on every normal day in May",
             f"With a limit of {limit}, it rings on a normal day: {loudest} had {may[loudest]}. Raise it."),
        show(limit is not None and rates["2026-06-01"] >= limit, "It rings on 2 June",
             f"With a limit of {limit}, 2 June stays green. Lower it."),
    ]


def lab4a() -> list[bool]:
    doc = read_yaml("models/lab4_exposures.yml")
    if doc is None:
        return [False]
    exposures = doc.get("exposures", [])

    def named(e) -> bool:
        owner = str((e.get("owner") or {}).get("name", "")).strip().lower()
        return owner not in ("", "nobody", "team", "the team", "someone", "we")
    agent = next((e for e in exposures if e["name"] == "ingredient_reorder_agent"), {})
    extra = [e for e in exposures if e["name"] not in
             ("revenue_dashboard", "finance_close", "ingredient_reorder_agent")]
    reads_revenue = [e for e in extra if "revenue_daily" in str(e.get("depends_on"))]
    out = run("dbt", "ls", "--select", "stg_pos_payments+", "--resource-type", "exposure")
    return [
        show(named(agent), "Your turn: the agent has a person as owner", "Change 'nobody' to a person's name."),
        show(bool(reads_revenue), "Your turn: a fourth reader, the weekly email, on revenue_daily",
             "Add a fourth exposure like revenue_dashboard, with depends_on: [ref('revenue_daily')]."),
        show(bool(reads_revenue) and all(named(e) for e in reads_revenue), "The weekly email has a person as owner",
             "Give the new exposure an owner with a name."),
        show(out.count("exposure:") >= 4, "dbt lists four readers", "Save the file. Check its spaces."),
    ]


def lab4b() -> list[bool]:
    gate = re.search(r"^GATE\s*=\s*True", open("tools/agent_tools.py").read(), re.M) is not None
    results = [show(gate, "Your turn: the gate is on", "In tools/agent_tools.py, change 'GATE = False' to 'GATE = True'.")]
    if gate:
        results.append(show("HOLD" in run("python", "tools/agent_tools.py", "read", "2026-06-02"),
                            "2 June: the agent gets HOLD"))
        results.append(show("Yesterday's takings" in run("python", "tools/agent_tools.py", "read", "2026-05-31"),
                            "31 May: the agent gets the takings",
                            "A check fails on a normal day: fix your limit in Lab 3, Part B, first."))
    return results


def lab5() -> list[bool]:
    text = open("labs/my_check.md").read()
    labels = ["The standard, in one sentence", "The limit it checks, for example 20% or 04:00",
              "The owner, a person's name", "Where it runs, and when"]
    lines = [line.strip() for line in text.splitlines()]
    answers = {}
    for label in labels:
        i = next((n for n, line in enumerate(lines) if line.startswith(label + ":")), None)
        if i is None:
            continue
        after = lines[i][len(label) + 1:].strip()
        if not after:  # the answer can also be on the next line
            nxt = next((line for line in lines[i + 1:] if line), "")
            is_label = any(nxt.startswith(l + ":") for l in labels) or nxt.startswith(("The check", "A ", "```"))
            after = "" if is_label else nxt
        answers[label] = after
    blocks = [b for b in re.findall(r"```yaml\n(.*?)```", text, re.S) if "______" not in b]

    def parses(block: str) -> bool:
        try:
            return bool(yaml.safe_load(block))
        except yaml.YAMLError:
            return False
    owner = answers.get("The owner, a person's name", "").strip().lower()
    return [
        show(bool(answers.get("The standard, in one sentence", "")), "Your standard, in one sentence",
             "Write it after 'The standard, in one sentence:'."),
        show(bool(re.search(r"\d", answers.get("The limit it checks, for example 20% or 04:00", ""))),
             "A number in the limit", "A limit needs a number, for example 20% or 04:00."),
        show(bool(owner) and owner not in ("the team", "team", "someone", "we"), "A person as owner",
             "Write one person's name, not a team."),
        show(any(parses(b) for b in blocks), "Your check, as code, with no blanks left",
             "Keep one template, fill every ______, and keep the spaces as they are."),
    ]


def lab6() -> list[bool]:
    parsed = run("dbt", "parse")
    if "Error" in parsed:
        print("  ✗ dbt cannot read models/lab6_semantic.yml:")
        print("      " + next((l for l in parsed.splitlines() if "Error" in l), "").strip())
        return [False]

    def ask(metric: str) -> str:
        return run("mf", "query", "--metrics", metric, "--group-by", "metric_time__day",
                   "--start-time", "2026-06-01", "--end-time", "2026-06-01")
    return [
        show("4012.8" in ask("revenue"), "The metric revenue gives 4,012.80 for 1 June"),
        show(re.search(r"\b576\b", ask("payments")) is not None,
             "Your turn: the metric payments gives 576 for 1 June",
             "Add the metric 'payments', type simple, with the measure 'payment_count'."),
        show(re.search(r"\b6\.96", ask("average_payment")) is not None,
             "Your turn: the metric average_payment gives 6.97 for 1 June",
             "Add the metric 'average_payment', type ratio: numerator revenue, denominator payments."),
    ]


LABS = {"1": [lab1], "2": [lab2], "3a": [lab3a], "3b": [lab3b], "3": [lab3a, lab3b],
        "4a": [lab4a], "4b": [lab4b], "4": [lab4a, lab4b], "5": [lab5], "6": [lab6]}

if __name__ == "__main__":
    part = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    if part not in LABS:
        sys.exit("Use: uv run tools/check.py 1   (1, 2, 3a, 3b, 4a, 4b, 5, or 6)")
    print(f"Lab {part}")
    results = [r for step in LABS[part] for r in step()]
    done = sum(results)
    print(f"{done} of {len(results)} done." + (" Well done." if done == len(results) else ""))
