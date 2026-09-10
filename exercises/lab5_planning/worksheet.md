# Worksheet · the one check you ship

Use your own standard from Module 1 first. No standard? Take one of these. Each has a number, a name, and a mechanism. Sanne is the integrations engineer who owns the payment feed. Sam works in finance.

## Take one of these

1. **The gate.** Any column change in the payments feed stops the copy and alerts #data-alerts within 15 minutes. Owner: Sanne. Mechanism: a contract check in the pipeline.
2. **The repeat.** Alert #data-alerts if more than 20% of a day's payments equal the customer's previous payment. Owner: Sanne. Mechanism: a check every morning after the copy.
3. **The load.** The payments table is loaded by 04:00, every day. Owner: Sanne. Mechanism: a freshness check at 04:00 that posts to #data-alerts.
4. **The menu.** Every payment amount is between €2.80 and €60.00. Owner: Sam. Mechanism: a range check on the payments table every morning.

## Your check

| Part | Your answer |
| --- | --- |
| The standard, in one sentence | |
| The limit it checks, for example 20% or 04:00 | |
| The owner: a person's name | |
| The check, as code (YAML or SQL) | |
| Where it runs, and when | |

Done early? Write the alert it sends, in five lines: what, since when, impact, owner, next step.
