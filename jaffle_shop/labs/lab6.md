# Lab 6 · The one check you ship

**12 minutes** · Write one check from your own standard, and run it in the sandbox.

> This page stays on the left. Click a file name to open it on the right.

### 1 · Pick your standard

In Module 1 you wrote a standard for your own incident: a number, a name, and a mechanism. No standard with you? Take one from the table at the bottom of this page.

Your check runs in the sandbox, on one of its tables. Pick the table that is closest to your own data.

### 2 · Pick the kind of check

Three kinds of check fit a standard:

| Kind | Use it when | The file |
| --- | --- | --- |
| A dbt test | A rule about every row, checked when dbt builds. A query test can compare two tables. | [`tests/my_check.sql`](../tests/my_check.sql) |
| A Soda check | How the table looks today: fresh, full, normal. It runs on its own schedule. | [`soda/my_check.yml`](../soda/my_check.yml) |
| A contract | A promise about the columns, checked before a change lands. | Lab 2's file, `models/staging/lab2_contract.yml` |

For this lab, write a query test or a Soda check. Both files are ready, with only comments in them.

### 3 · Your turn

1. Open [`labs/my_check.md`](my_check.md), and write each answer after its line.
2. Write your check in `tests/my_check.sql` or in `soda/my_check.yml`. Look at the Lab 1 and Lab 3 files for the shape.

**Hint:** a Soda scan in `check.py` runs on the morning of 2 June. A query test runs on the whole table.

### 4 · Check

```bash
uv run tools/check.py 6
```

**You see:** `6 of 6 done. Well done.` The last ✓ line says if your check passes or fails, and on how many rows. A good check fails for a real reason: on the bad days, not on every row.

### Extra

Write the same standard as the other kind too: a Soda check and a query test. `check.py 6` shows it on the Extra line. To compare two tables in Soda, copy the query shape of `soda/lab3_repeat.yml`, with `${NOW}`.

## No standard? Take one of these

Sanne owns the payment feed. Sam works in finance.

| Standard | Owner | The table, and the shape |
| --- | --- | --- |
| Every day, the payments match the bank deposit within 1%. | Sam | A query test like `tests/lab1_updated_before_placed.sql`. `revenue_daily` has one row per café per day: add up `revenue_eur` by `pay_date` first. `bank_deposits` has `deposit_date` and `amount_eur`. |
| Ring when more than 20% of a day's payments repeat the last amount. | Sanne | `payments_repeat_rate`, a Soda check like `soda/lab3_repeat.yml` |
| Last night's payments are in by the 09:00 scan. | Sanne | `stg_pos_payments`, like the freshness check in `soda/lab3_checks.yml` |
| Every amount is between €2.80 and €60.00 (280 to 6000 in cents). | Sam | `stg_pos_payments`, like the validity check in `soda/lab3_checks.yml` |

**Stuck?** Read the ✗ line: it says what is wrong. Fix it, save, and check again.
