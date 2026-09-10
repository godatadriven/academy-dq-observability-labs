# Lab 5 · The one check you ship

**Goal:** write one check for your own work, with a number and a person's name, ready to use on Monday. **Time:** 12 minutes.

> This page stays on the left. Your files open on the right.

In Module 1 you wrote a **standard** for your own data incident: a number, a name, and a mechanism. A **mechanism** is something that runs by itself, like a test, a check, or a contract. Find your standard on the Miro board, in "Your incidents". No standard? Take one below.

## Steps

1. **Write** the mechanism of your standard as code: a dbt test (Lab 1), a contract (Lab 2), or a Soda check (Lab 3). Write it in [`labs/my_check.md`](my_check.md), from a template. Copy the shape from a Lab 1, 2, or 3 file: the list below names one for each standard. You do not need to run it.
2. **Add** the number and the owner's name in the file. Then put your check on a sticky under your standard on the Miro board.
3. **Swap** with the pair next to you. They have ninety seconds to find a loophole. Then fix it. Online: swap with the next pair on the Miro board.

A loophole is:

- A team instead of a name: "the team", "someone", "we".
- A word instead of a number: "regularly", "soon", "as needed".
- A meeting instead of a mechanism: "we check it in the review". Nothing runs when nobody remembers.

**Done early?** Write the alert that your check sends, in five lines: what, since when, impact, owner, next step.

## No standard? Take one of these

Each has a number, a name, and a mechanism. Sanne is the integrations engineer who owns the payment feed. Sam works in finance.

1. **The gate.** Any column change in the payments feed stops the copy and alerts #data-alerts within 15 minutes. Owner: Sanne. Mechanism: a contract check in the pipeline. Copy the shape from [`models/staging/lab2_contract.yml`](../models/staging/lab2_contract.yml).
2. **The repeat.** Alert #data-alerts if more than 20% of a day's payments equal the customer's previous payment. Owner: Sanne. Mechanism: a check every morning after the copy. Copy the shape from [`soda/lab3_repeat.yml`](../soda/lab3_repeat.yml).
3. **The load.** The payments table is loaded by 04:00, every day. Owner: Sanne. Mechanism: a freshness check at 04:00 that posts to #data-alerts. Copy the shape from the freshness check in [`soda/lab3_checks.yml`](../soda/lab3_checks.yml).
4. **The menu.** Every payment amount is between €2.80 and €60.00: 280 to 6000 in cents. Owner: Sam. Mechanism: a validity check on the payments table every morning. Copy the shape from the validity check in [`soda/lab3_checks.yml`](../soda/lab3_checks.yml).
