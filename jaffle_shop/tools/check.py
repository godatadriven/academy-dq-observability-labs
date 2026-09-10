"""Check your lab work. Run it from this folder, with the lab and part:

    uv run tools/check.py 1        Lab 1
    uv run tools/check.py 3a       Lab 3, Part A

Each line says ✓ when that part is right, or ✗ with what is wrong.
The Extra line is optional. It does not count for "Well done."
"""
import re
import subprocess
import sys
from pathlib import Path

import duckdb
import yaml

EXTRAS: list[str] = []
PEOPLE_NOT = ("", "nobody", "team", "the team", "someone", "we", "us", "finance", "data team")


def run(*command: str) -> str:
    result = subprocess.run(command, capture_output=True, text=True)
    return re.sub(r"\x1b\[[0-9;]*m", "", result.stdout + result.stderr)


def show(done: bool, what: str, wrong: str = "") -> bool:
    print(f"  {'✓' if done else '✗'} {what}")
    if not done and wrong:
        print(f"      {wrong}")
    return done


def extra(done: bool, what: str, wrong: str = "") -> None:
    EXTRAS.append(f"  Extra: ✓ {what}" if done else f"  Extra: not yet · {what}" + (f"\n      {wrong}" if wrong else ""))


def read_yaml(path: str):
    try:
        return yaml.safe_load(open(path)) or {}
    except yaml.YAMLError as error:
        print(f"  ✗ {path} is not valid YAML: {str(error).splitlines()[0]}")
        print("      The spaces at the start of a line you changed do not line up with the lines around it.")
        return None


def query(sql: str):
    con = duckdb.connect("jaffle_shop.duckdb", read_only=True)
    rows = con.execute(sql).fetchall()
    con.close()
    return rows


def has_code(path: str, comment: str) -> bool:
    """True when the file has at least one line that is not empty and not a comment."""
    file = Path(path)
    return file.exists() and any(line.strip() and not line.strip().startswith(comment)
                                 for line in file.read_text().splitlines())


def dbt_results(out: str) -> dict[str, str]:
    """Test name -> PASS, FAIL, or ERROR, from the output of dbt test."""
    found = re.findall(r"\d+ of \d+ (PASS|FAIL \d+|ERROR|WARN \d+) (\S+)", out)
    return {name: status.split()[0] for status, name in found}


def person(name) -> bool:
    return str(name or "").strip().lower() not in PEOPLE_NOT


# Lab 1 · dbt tests on Module 1's table

def lab1() -> list[bool]:
    if read_yaml("seeds/lab1_tests.yml") is None:
        return [False]
    results = dbt_results(run("dbt", "test", "--select", "orders_daily_extract"))

    def status(part: str) -> str:
        return next((s for name, s in results.items() if name.endswith(part) or part in name), "")
    six = {"email is not empty": "not_null_orders_daily_extract_email", "email looks like an email": "match_regex",
           "order_total is 0 or more": "order_total__0", "no row is in twice": "compound_columns",
           "loaded within 1 day": "recent_data", "not updated before it is placed": "lab1_updated_before_placed"}
    missing = [rule for rule, part in six.items() if status(part) != "FAIL"]
    above = [s for name, s in results.items() if "be_between" in name and "order_total" in name and "1000" in name]
    mine = status("lab1_loaded_before_placed")
    email = status("lab1_one_email_one_customer")

    extra(email == "PASS", "tests/lab1_one_email_one_customer.sql runs, and passes",
          {"": "The file has no query yet.", "ERROR": "The query does not run.",
           "FAIL": "The query returns rows, but no email belongs to two customers."}.get(email, ""))
    return [
        show(not missing, "Module 1's six defects: six tests fail",
             f"Gone, or not failing now: {', '.join(missing)}."),
        show("FAIL" in above, "Task A: a test that no order is above 1,000, failing on C-1045",
             "There is no failing test with max_value 1000 on order_total yet." if not above
             else "Your test with 1000 does not fail."),
        show(mine == "FAIL", "Task B: your query test finds the order loaded before it was placed",
             {"": "tests/lab1_loaded_before_placed.sql has no query yet, or does not read orders_daily_extract.",
              "ERROR": "tests/lab1_loaded_before_placed.sql does not run: dbt shows an error for it.",
              "PASS": "tests/lab1_loaded_before_placed.sql runs, but returns no row."}.get(mine, "")),
    ]


# Lab 2 · a contract on the copy

def lab2() -> list[bool]:
    contract = read_yaml("models/staging/lab2_contract.yml")
    if contract is None:
        return [False]
    model = contract["models"][0]
    columns = {c["name"]: [k for k in (c.get("constraints") or [])] for c in model.get("columns", [])}
    on = (model.get("config") or {}).get("contract", {}).get("enforced") is True
    method = any(k.get("type") == "not_null" for k in columns.get("payment_method", []))
    above = any(k.get("type") == "check" and re.search(r"amount\s*(>\s*0|>=\s*1)\b", str(k.get("expression", "")))
                for k in columns.get("amount", []))
    extra(any(k.get("type") in ("primary_key", "unique") for k in columns.get("payment_id", [])),
          "payment_id is never in twice", "payment_id has no primary_key or unique rule yet.")
    results = [
        show(on, "Task A: the contract is on", "enforced is not true."),
        show(method, "Task A: payment_method can never be empty", "payment_method has no not_null rule yet."),
        show(above, "Task B: every amount is above 0", "amount has no check rule with 'amount > 0' yet."),
    ]
    if on:
        out = run("dbt", "run", "--select", "stg_pos_events")
        stops = "NOT NULL constraint failed" in out and ".amount" in out
        if "Constraint Error" in out:
            wrong = "The build stops on another rule, not on the empty amount."
        elif "ERROR=0" in out:
            wrong = "The copy builds: nothing stops it."
        else:
            wrong = "dbt cannot build the copy: " + next((l.strip() for l in out.splitlines() if "Error" in l), "")
        results.append(show(stops, "The gate stops the copy on the 1 June events", wrong))
    return results


# Lab 3 · Soda checks

def scan(now: str, *files: str) -> str:
    return run("soda", "scan", "-d", "jaffle_shop", "-c", "soda/configuration.yml", "-v", f"NOW={now} 09:00:00", *files)


def failed_names(out: str) -> list[str]:
    return [line.split("]", 1)[1].replace("[FAILED]", "").strip() for line in out.splitlines() if "[FAILED]" in line]


def lab3a() -> list[bool]:
    checks = read_yaml("soda/lab3_checks.yml")
    if checks is None:
        return [False]
    items = checks.get("checks for stg_pos_payments", []) or []
    lines = {str(list(c)[0] if isinstance(c, dict) else c): (list(c.values())[0] if isinstance(c, dict) else {})
             for c in items}

    def has(pattern: str) -> bool:
        return any(re.search(pattern, line) for line in lines)
    customer = has(r"missing_count\(\s*customer_id\s*\)\s*=\s*0")
    twice = has(r"duplicate_count\(\s*payment_id\s*\)\s*=\s*0")
    out = scan("2026-05-31", "soda/lab3_checks.yml")
    passed = "All is good" in out
    method = next((cfg for line, cfg in lines.items() if re.search(r"invalid_count\(\s*payment_method\s*\)", line)), None)
    extra(method is not None and "valid values" in (method or {}) and passed,
          "every payment method is one of the four known ones",
          "There is no invalid_count check on payment_method with valid values yet.")
    return [
        show(customer, "Task A: every payment has a customer", "There is no missing_count check on customer_id yet."),
        show(twice, "Task B: no payment is in twice", "There is no duplicate_count check on payment_id yet."),
        show(passed, "All checks pass on 31 May",
             f"This check fails on 31 May: {', '.join(failed_names(out))}." if failed_names(out)
             else "Soda cannot read soda/lab3_checks.yml."),
    ]


def lab3b() -> list[bool]:
    text = "\n".join(line for line in open("soda/lab3_repeat.yml").read().splitlines()
                     if not line.strip().startswith("#"))
    match = re.search(r"repeat_rate\s*<\s*([0-9.]+)", text) or re.search(r"fail:\s*when\s*>=?\s*([0-9.]+)", text)
    limit = float(match.group(1)) if match else None
    rates = dict(query("select pay_date::varchar, repeat_rate_pct from payments_repeat_rate "
                       "where pay_date between '2026-05-17' and '2026-06-01'"))
    may = {day: rate for day, rate in rates.items() if day < "2026-06-01"}
    loud = [day for day, rate in may.items() if limit is not None and rate >= limit]
    warns = "WARNED" in scan("2026-05-20", "soda/lab3_repeat.yml")
    quiet = "All is good" in scan("2026-05-31", "soda/lab3_repeat.yml")
    rings = "[FAILED]" in scan("2026-06-02", "soda/lab3_repeat.yml")
    extra("warn:" in text and warns and quiet and rings,
          "a warning on 19 May's payments, a failure on 2 June",
          "There is no warn level yet." if "warn:" not in text
          else "The scan of 20 May does not warn, or 31 May is not quiet, or 2 June does not fail.")
    return [
        show(limit is not None and not loud, "Task: quiet on every normal day in May",
             "There is no limit in soda/lab3_repeat.yml." if limit is None
             else f"With a limit of {limit:g}, it rings on the payments of normal days: "
                  f"{', '.join(loud[:3])}{f', and {len(loud) - 3} more' if len(loud) > 3 else ''}."),
        show(limit is not None and rates["2026-06-01"] >= limit, "It rings on 2 June",
             f"With a limit of {limit:g}, 2 June stays green." if limit else ""),
    ]


# Lab 4 · readers, and the agent's gate

def lab4a() -> list[bool]:
    doc = read_yaml("models/lab4_exposures.yml")
    if doc is None:
        return [False]
    exposures = doc.get("exposures", []) or []
    agent = next((e for e in exposures if e.get("name") == "ingredient_reorder_agent"), {})
    new = [e for e in exposures if e.get("name") not in
           ("revenue_dashboard", "finance_close", "ingredient_reorder_agent")]
    email = [e for e in new if "revenue_daily" in str(e.get("depends_on"))]
    out = run("dbt", "ls", "--select", "stg_pos_payments+", "--resource-type", "exposure")
    extra(any("bank_deposits" in str(e.get("depends_on")) for e in email),
          "the weekly email reads revenue_daily and bank_deposits",
          "The weekly email does not read bank_deposits yet.")
    return [
        show(person((agent.get("owner") or {}).get("name")), "Task A: the agent has a person as owner",
             "The agent's owner is not a person's name yet."),
        show(bool(email), "Task B: a fourth reader, the weekly email, reads revenue_daily",
             "There is no fourth exposure that reads revenue_daily yet."),
        show(bool(email) and all(person((e.get("owner") or {}).get("name")) for e in email),
             "Task B: the weekly email has a person as owner", "The new exposure has no person's name as owner."),
        show(out.count("exposure:") >= 4, "dbt lists four readers",
             "dbt lists " + str(out.count("exposure:")) + " readers. It cannot read the file, or a reader is missing."),
    ]


def lab4b() -> list[bool]:
    gate = re.search(r"^GATE\s*=\s*True", open("tools/agent_tools.py").read(), re.M) is not None
    results = [show(gate, "Task: the gate is on", "GATE is not True in tools/agent_tools.py.")]
    if gate:
        results.append(show("HOLD" in run("python", "tools/agent_tools.py", "read", "2026-06-02"),
                            "2 June: the agent gets HOLD", "The agent still gets the takings on 2 June."))
        results.append(show("Yesterday's takings" in run("python", "tools/agent_tools.py", "read", "2026-05-31"),
                            "31 May: the agent gets the takings",
                            "The agent gets HOLD on a normal day: one of your Lab 3 checks fails on 31 May."))
    return results


# Lab 5 · the semantic layer

def lab5() -> list[bool]:
    parsed = run("dbt", "parse")
    if "Error" in parsed:
        print("  ✗ dbt cannot read models/lab5_semantic.yml:")
        print("      " + next((l for l in parsed.splitlines() if "Error" in l), "").strip())
        return [False]
    doc = read_yaml("models/lab5_semantic.yml") or {}
    metrics = [m.get("name") for m in doc.get("metrics", []) or []]

    def ask(metric: str, by: str = "metric_time__day") -> str:
        return run("mf", "query", "--metrics", metric, "--group-by", by,
                   "--start-time", "2026-06-01", "--end-time", "2026-06-01")

    def wrong(metric: str, number: str) -> str:
        if metric not in metrics:
            return f"There is no metric '{metric}' in models/lab5_semantic.yml yet."
        return f"The metric '{metric}' does not give {number} for 1 June."
    by_method = ask("revenue", "payment__payment_method")
    extra("credit_card" in by_method and "2653.5" in by_method, "revenue by payment method: credit_card 2,653.50",
          "mf cannot group revenue by payment__payment_method yet.")
    return [
        show("4012.8" in ask("revenue"), "The metric revenue gives 4,012.80 for 1 June", wrong("revenue", "4,012.80")),
        show(re.search(r"\b576\b", ask("payments")) is not None, "Task A: the metric payments gives 576 for 1 June",
             wrong("payments", "576")),
        show(re.search(r"\b6\.96", ask("average_payment")) is not None,
             "Task B: the metric average_payment gives 6.97 for 1 June", wrong("average_payment", "6.97")),
    ]


# Lab 6 · your own check

def answers() -> dict[str, str]:
    """Each answer in labs/my_check.md, from the same line as its label."""
    labels = ["The standard, in one sentence", "The limit, as a number", "The owner, a person's name",
              "Where it runs, and when", "Why this kind of check"]
    lines = [line.strip() for line in open("labs/my_check.md").read().splitlines()]
    return {label: next((line[len(label) + 1:].strip() for line in lines if line.startswith(label + ":")), "")
            for label in labels}


def own_soda() -> tuple[bool, str]:
    if not has_code("soda/my_check.yml", "#"):
        return False, "soda/my_check.yml has no check yet."
    out = scan("2026-06-02", "soda/my_check.yml")
    errors = re.search(r"(\d+) errors?", out)
    if (errors and int(errors.group(1)) > 0) or not re.search(r"All is good|failure|WARNED", out):
        return False, "Soda cannot run soda/my_check.yml."
    verdict = "passes" if "All is good" in out else "warns" if "failure" not in out else "fails"
    return True, f"your Soda check {verdict} on 2 June"


def own_test() -> tuple[bool, str]:
    if not has_code("tests/my_check.sql", "--"):
        return False, "tests/my_check.sql has no query yet."
    status = dbt_results(run("dbt", "test", "--select", "my_check")).get("my_check", "")
    if status not in ("PASS", "FAIL"):
        return False, "tests/my_check.sql does not run: dbt shows an error for it."
    return True, f"your query test {'passes' if status == 'PASS' else 'fails'}"


def lab6() -> list[bool]:
    found = answers()
    soda_ok, soda_says = own_soda()
    test_ok, test_says = own_test()
    extra(soda_ok and test_ok, "your standard as a Soda check and as a query test", "Only one of the two runs.")
    if soda_ok or test_ok:
        code_what, code_wrong = "Your check runs in the sandbox: " + " · ".join(
            says for ok, says in ((soda_ok, soda_says), (test_ok, test_says)) if ok), ""
    elif has_code("soda/my_check.yml", "#"):
        code_what, code_wrong = "Your check runs in the sandbox", soda_says
    elif has_code("tests/my_check.sql", "--"):
        code_what, code_wrong = "Your check runs in the sandbox", test_says
    else:
        code_what, code_wrong = "Your check runs in the sandbox", "soda/my_check.yml and tests/my_check.sql have no check yet."
    return [
        show(bool(found.get("The standard, in one sentence")), "Your standard, in one sentence",
             "The standard is empty."),
        show(bool(re.search(r"\d", found.get("The limit, as a number", ""))), "A number in the limit",
             "The limit has no number."),
        show(person(found.get("The owner, a person's name")), "A person as owner", "The owner is not a person's name."),
        show(bool(found.get("Where it runs, and when")), "Where it runs, and when", "This answer is empty."),
        show(bool(found.get("Why this kind of check")), "Why this kind of check", "This answer is empty."),
        show(soda_ok or test_ok, code_what, code_wrong),
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
    for line in EXTRAS:
        print(line)
