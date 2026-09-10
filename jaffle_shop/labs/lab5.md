# Lab 5 · The one check you ship

**12 minutes** · Write one check for your own work, with a number and a person's name.

> This page stays on the left. Click a file name to open it on the right.

### 1 · Find your standard

In Module 1 you wrote a standard for your own incident: a number, a name, and a mechanism. It is on the Miro board, in "Your incidents". No standard? Take one from the list below.

### 2 · Your turn

Open [`labs/my_check.md`](my_check.md), and fill it in:

1. Your standard, the limit, and the owner.
2. The check, as code. Keep one of the three templates, and fill every `______`.
3. Save, and check:

```bash
uv run check.py 5
```

**You see:** `4 of 4 done. Well done.`

### 3 · Find the loophole

Swap with the pair next to you. You have ninety seconds to find a loophole in their check:

- a team, not a name: "the team", "someone"
- a word, not a number: "regularly", "soon"
- a meeting, not a mechanism: "we check it in the review"

Then fix your own. Put your check on a sticky under your standard on the Miro board.

**Talk:** what does your check's alert say?

## No standard? Take one of these

Sanne owns the payment feed. Sam works in finance.

| Standard | Owner | Copy the shape from |
| --- | --- | --- |
| Any column change in the payments feed stops the copy. | Sanne | [`lab2_contract.yml`](../models/staging/lab2_contract.yml) |
| Ring if more than 20% of a day's payments repeat the last amount. | Sanne | [`lab3_repeat.yml`](../soda/lab3_repeat.yml) |
| The payments table is loaded by 04:00, every day. | Sanne | the freshness check in [`lab3_checks.yml`](../soda/lab3_checks.yml) |
| Every amount is between €2.80 and €60.00 (280 to 6000 in cents). | Sam | the validity check in [`lab3_checks.yml`](../soda/lab3_checks.yml) |
