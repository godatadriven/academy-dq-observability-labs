# Lab 5 · The one check you ship

**Goal:** write one check for your own work, with a number and a person's name, ready to use on Monday. **Time:** 12 minutes.

> Keep this page on the right: drag its tab to the right half of the window.

In Module 1 you wrote a **standard** for your own data incident: a number, a name, and a mechanism. A **mechanism** is something that runs by itself, like a test, a check, or a contract. Find your standard on the Miro board, in "Your incidents". No standard? Take one below.

## Steps

1. **Write** the mechanism of your standard as one dbt test, like Lab 1, or one Soda check, like Lab 3. Start from a template below. You do not need to run it.
2. **Add** the number and the owner's name: fill the table under "Your check". Put the check and the owner on a sticky under your standard on the Miro board.
3. **Swap** with the pair next to you. Online: the next pair on the Miro board. They have ninety seconds to find a loophole.
4. Fix it.

A loophole is:

- A team instead of a name: "the team", "someone", "we".
- A word instead of a number: "regularly", "soon", "as needed".
- A meeting instead of a mechanism: "we check it in the review". Nothing runs when nobody remembers.

**Done early?** Write the alert that your check sends, in five lines: what, since when, impact, owner, next step.

## No standard? Take one of these

Each has a number, a name, and a mechanism. Sanne is the integrations engineer who owns the payment feed. Sam works in finance.

1. **The gate.** Any column change in the payments feed stops the copy and alerts #data-alerts within 15 minutes. Owner: Sanne. Mechanism: a contract check in the pipeline.
2. **The repeat.** Alert #data-alerts if more than 20% of a day's payments equal the customer's previous payment. Owner: Sanne. Mechanism: a check every morning after the copy.
3. **The load.** The payments table is loaded by 04:00, every day. Owner: Sanne. Mechanism: a freshness check at 04:00 that posts to #data-alerts.
4. **The menu.** Every payment amount is between €2.80 and €60.00. Owner: Sam. Mechanism: a validity check on the payments table every morning.

## Your check

| Part | Your answer |
| --- | --- |
| The standard, in one sentence | |
| The limit it checks, for example 20% or 04:00 | |
| The owner: a person's name | |
| The check, as code (YAML or SQL) | |
| Where it runs, and when | |

## Templates

Pick the tool that fits. Replace each `______`.

A dbt test, like Lab 1:

```yaml
models:
  - name: ______
    columns:
      - name: ______
        data_tests:
          - ______
```

The first blank is the table, the second the column, and the third the test with its settings. `seeds/lab1_tests.yml` has examples of each. For a seed, like Lab 1's table, write `seeds:` instead of `models:`.

A Soda check, like Lab 3:

```yaml
checks for ______:
  - ______:
      name: "______"
```

The first blank is the table, the second the check with its limit, and the third the rule in plain words. `soda/lab3_checks.yml` has examples of each.
