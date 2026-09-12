# Lab 6 · Your own check

> **12 minutes** · **Goal:** one check from your own standard, running in the sandbox.<br>
> **You write:** three short answers, and one check: a query test or a Soda check.<br>
> **Done when:** `uv run tools/check.py 6` says `4 of 4 done. Well done.`

### 1 · Pick your standard

In Module 1 you wrote a standard for your own incident: a number, a name, and a mechanism. No standard with you? Take one from the table at the bottom of this page. It goes from the easiest to the hardest.

Your check runs in the sandbox, on one of its tables. Pick the table that is closest to your own data.

### 2 · Pick the kind of check

| Kind | Use it when | The file |
| --- | --- | --- |
| A dbt test | A rule about every row, checked when dbt builds. A query test can compare two tables. | [`tests/my_check.sql`](../tests/my_check.sql) |
| A Soda check | How the table looks today: fresh, full, normal. It runs on its own schedule. | [`soda/my_check.yml`](../soda/my_check.yml) |
| A data contract | A promise about the columns, checked before a change lands. | Lab 2's file, not in this lab |

Both files hold a starter: a working check, written as comments.

---

### 3 · Your turn

**Task.**

1. Open [`labs/my_check.md`](my_check.md), and write the three answers, each on the line of its question.
2. Open [`tests/my_check.sql`](../tests/my_check.sql) or [`soda/my_check.yml`](../soda/my_check.yml). Remove the comment marks from the starter's lines. Then change them to your own rule.

> **Hint:** `check.py` scans a Soda check on the morning of 2 June. A query test runs on the whole table.

### 4 · Check

```bash
uv run tools/check.py 6
```

```
4 of 4 done. Well done.
```

The last ✓ line says if your check passes or fails, and on how many rows. A good check fails for a real reason: on the bad days, not on every row.

---

### Extra (optional)

Write the same standard as the other kind too: a Soda check and a query test. To compare two tables in Soda, copy the query shape of `soda/lab3_repeat.yml`, with `${NOW}`. The name before `query:` must match the name in the check line. Either table can go after `checks for`.

### Stuck?

- A ✗ line says what is wrong. Fix it, save (Cmd+S, or Ctrl+S on Windows), and check again.
- Your query test fails on every row: look at the rule in your `where` line, and at the columns you compare.
- "Soda cannot run soda/my_check.yml": the spaces at the start of the lines do not line up. After you remove the `# `, the dash is two spaces in, and `name:` six.

## No standard? Take one of these

Sanne owns the payment feed. Sam works in finance.

| Standard | Owner | The table, and the shape |
| --- | --- | --- |
| 1 · Every amount is between €2.80 and €60.00 (280 to 6000 in cents). | Sam | `stg_pos_payments`. The starter in `tests/my_check.sql` is this check. |
| 2 · Last night's payments are in by the 09:00 scan: the newest is less than 1 day old. | Sanne | `stg_pos_payments`. Copy the freshness check in `soda/lab3_checks.yml`, with its `filter:` line. |
| 3 · Alert when more than 20% of a day's payments repeat the last amount. | Sanne | `payments_repeat_rate`. Copy the check in `soda/lab3_repeat.yml`, and give it one limit: `- repeat_rate <= 20:`. |
| 4 · Harder: every day, the payments match the bank deposit within 1%. | Sam | A query test like `tests/lab1_updated_before_placed.sql`. `revenue_daily` has one row per café per day: add up `revenue_eur` by `pay_date` first. `bank_deposits` has `deposit_date` and `amount_eur`. |
