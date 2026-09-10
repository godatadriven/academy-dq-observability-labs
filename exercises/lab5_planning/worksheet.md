# The one check you ship

The fallback for slide 23. Use your own standard from Module 1 first: the one under your incident, in the Miro frame "Your incidents". No standard with you? Take one of these. Each has the three parts from Module 1: a number, a name, a mechanism.

## Take one of these

1. **The gate.** Any column change in the payments feed fails the copy and alerts #data-alerts within 15 minutes. Owner: Sanne. Mechanism: a contract check in the pipeline.
   *Module 1, the model answer for "Your incident, one standard".*
2. **The repeat.** Alert #data-alerts if more than 20% of a day's payments equal the customer's previous payment. Owner: Sanne. Mechanism: a check every morning after the copy.
   *Module 1, the staleness variant of the case standard. A normal day is about 6%.*
3. **The load.** The payments table is loaded by 04:00, every day. Owner: Sanne. Mechanism: a freshness check at 04:00 that posts to #data-alerts.
4. **The menu.** Every payment amount is between €2.80 and €60.00. Owner: Sam. Mechanism: a range check on the payments table every morning.

## Your check

Fill one table. The mechanism is code, not a sentence. Copy the shape from Lab 1, a dbt test, or from Lab 3, a Soda check.

| Part | Your answer |
| --- | --- |
| The standard, in one sentence | |
| The number | |
| The owner: a person's name | |
| The mechanism, as YAML | |
| Where it runs, and when | |

Done early? Write the alert it sends, in the five lines from Module 1: what, since, impact, owner, next.

## Swap

Hand it to the next pair. They have ninety seconds to find the loophole. Then swap back and fix it.

- **"The team", "someone", "we".** Not a name.
- **"Regularly", "soon", "as needed".** Not a number.
- **"We check it in the review".** Not a mechanism. Nothing runs when nobody remembers.
