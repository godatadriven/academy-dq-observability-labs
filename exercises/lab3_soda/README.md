# Lab 3 · Checks on the payments table

**Goal:** write checks that pass on a normal morning, then a check that catches the Frozen Payments.

A Soda **check** is a rule about a table. A **scan** runs your checks and says PASSED or FAILED for each one.

## Pick the morning

The data covers 17 May to 17 June 2026, one load per night. `NOW` is the time the scan pretends it is. A scan at 09:00 looks at the payments of the day before.

Every scan in this lab uses this command, from `jaffle_shop/`. Change only the date. Do not copy `checks.yml`. The command reads it where it is.

```bash
soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" ../exercises/lab3_soda/checks.yml
```

## Part A · A normal morning, 31 May

1. Look at the data first. How many payments arrive each day?

```bash
dbt show --inline "select paid_at::date as day, count(*) from {{ ref('stg_pos_payments') }} group by 1 order by 1" --limit 40
```

2. Open `checks.yml`. Fill the five blanks: freshness, volume, and the lowest and highest amount.
3. Scan 31 May.
4. Go on when all three checks pass. Do not scan 2 June yet.

**When it works:** three lines say `[PASSED]`, and the last line is `All is good. No failures.`

## Part B · Catch the case

Module 1's example rule: alert when more than 20 in 100 payments equal the customer's last payment. A normal day has about 6 in 100.

1. In `checks.yml`, delete the `# ` at the start of the last five lines.
2. Fill the threshold.
3. Scan 31 May, then 1 June, then 2 June.

**When it works:**

- 31 May and 1 June pass. The scan on 1 June looks at 31 May's payments, which were still right.
- 2 June fails twice. The repeat check shows `check_value: 100.0`: every returning customer paid exactly their last amount. New customers are not counted in it. The range check shows `check_value: 41`: 41 new customers had no last payment, so they got 0.

## If it does not work

| You see | Do this |
| --- | --- |
| `Configuration path ... does not exist` | You are in the wrong folder. Go to `jaffle_shop/`. |
| An error about `${NOW}` | The `-v NOW="..."` part is missing from the command. |
| Freshness fails on 31 May | The limit is too small. Use `1d`. |
| Volume fails on 31 May | Make the band wider, and keep the `filter` line. It counts only one day. |
| A YAML error in Part B | A space is left at the start of a line. `checks for` starts at the very start of the line, with no space. |
| The repeat check passes on 2 June | The threshold is too high. |
