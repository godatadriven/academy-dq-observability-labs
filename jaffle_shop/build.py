"""Build the sandbox in one go. Run it from this folder:

    uv run build.py

It gets dbt's packages, loads the tables, builds the models, runs Module 1's four tests,
and runs the Soda setup check. It stops at the first step that fails.
"""
import subprocess
import sys

STEPS = [
    ("Get dbt's packages", ["dbt", "deps"], "Installed"),
    ("Load the tables", ["dbt", "seed"], "PASS=4"),
    ("Build the models", ["dbt", "run"], "PASS=5"),
    ("Run Module 1's four tests", ["dbt", "test"], "PASS=4"),
    ("Check that Soda can read the tables",
     ["soda", "scan", "-d", "jaffle_shop", "-c", "soda/configuration.yml",
      "-v", "NOW=2026-05-31 09:00:00", "soda/setup_check.yml"], "All is good"),
]

for number, (name, command, expected) in enumerate(STEPS, start=1):
    print(f"Step {number} of {len(STEPS)}: {name} ...", flush=True)
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout + result.stderr
    if result.returncode != 0 or expected not in output:
        print(output[-2000:])
        sys.exit(f"Step {number} failed: {' '.join(command)}. See setup-guide.md, Common problems.")

print("Ready. Module 1's four tests pass, and Soda can read the tables.")
