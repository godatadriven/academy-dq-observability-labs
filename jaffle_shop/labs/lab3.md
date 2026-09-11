# Lab 3 · Checks on the payments table

**Part A 15 minutes, Part B 10 minutes** · Write Soda checks, and set the levels that catch the Frozen Payments.

> This page stays on the left. Click a file name to open it on the right.

## Part A · A normal morning

### 1 · Read the file

Open [`soda/lab3_checks.yml`](../soda/lab3_checks.yml): three Soda checks. Soda looks at a table as it is now, and says PASSED or FAILED for each check. Here is the first:

```yaml
checks for stg_pos_payments:
  - freshness(_etl_loaded_at) < 1d:
      name: "freshness: the copy ran last night"
      filter: _etl_loaded_at <= '${NOW}'::timestamp
```

| Line | What it means |
| --- | --- |
| `checks for stg_pos_payments:` | The table that these checks look at: the payments table. |
| `- freshness(_etl_loaded_at) < 1d:` | The check: what must be true. Here, the newest load is less than one day old. |
| `name:` | The rule in words. The scan prints it. |
| `filter:` | Which rows to look at: only what was loaded before `NOW`. |

The other two checks have the same shape: a check line, a name, and a filter.

### 2 · Scan a normal morning

A scan runs every check once. `NOW` is the morning that the scan pretends it is. This scan is on Sunday 31 May, the day before the rename.

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/lab3_checks.yml
```

**You see:** `3/3 checks PASSED` and `All is good`.

### 3 · Your turn

**Task.** Add two checks at the end of the file, each with a name:

- Every payment has a customer: `customer_id` is never empty.
- No payment is in the table twice: `payment_id` never repeats.

Put the dash of each new check under the other dashes: two spaces in.

**Hint:** Soda's pages on [missing metrics](https://docs.soda.io/soda-cl/missing-metrics.html) and [numeric metrics](https://docs.soda.io/soda-cl/numeric-metrics.html) (look for `duplicate_count`).

### 4 · Check

```bash
uv run tools/check.py 3a
```

**You see:** `3 of 3 done. Well done.`

**Extra.** Every payment method is one of `credit_card`, `coupon`, `bank_transfer`, `gift_card`. **Hint:** [validity metrics](https://docs.soda.io/soda-cl/validity-metrics.html), with `valid values`.

**Stop here.** Part B starts at the slide "Catch the Case".

## Part B · Catch the case

### 5 · Read the file

Open [`soda/lab3_repeat.yml`](../soda/lab3_repeat.yml). It is Module 1's rule: ring when too many payments repeat the customer's last amount.

| Line | What it means |
| --- | --- |
| `checks for payments_repeat_rate:` | A table with one row per day: the percent of payments that repeat the customer's last amount. |
| `- repeat_rate < 5:` | The check: the day's percent is below 5. The limit is 5. |
| `repeat_rate query:` | The SQL that gives that percent, for the day before `NOW`. |

The scan on the morning of a day reads the payments of the day before.

### 6 · Scan a normal morning

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-26 09:00:00" soda/lab3_repeat.yml
```

**You see:** `Oops! 1 failures`. On a normal day, 9.46% of the payments repeat. A limit of 5 is too tight.

### 7 · Your turn

One limit is not enough. A normal day can repeat 10% of the amounts, and 2 June repeats 100%. Give the check two levels:

- a **warning** when more than 10% of the payments repeat: someone looks at it,
- a **failure** when more than 20% repeat, Module 1's standard of one in five: the line stops.

In Soda, a check with two levels has no limit in its check line. The line is only `- repeat_rate:`, with `warn:` and `fail:` under it, next to `repeat_rate query:` and `name:`.

**Hint:** Soda's page on [alert configurations](https://docs.soda.io/soda-cl/optional-config.html), with `warn: when > ...` and `fail: when > ...`.

### 8 · Check

```bash
uv run tools/check.py 3b
```

**You see:** `3 of 3 done. Well done.` A ✗ line names what your levels get wrong.

### 9 · Scan 2 June

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-06-02 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
```

**You see:** `Oops!` and two failed checks. Your checks catch the Frozen Payments on the first morning.

### Extra

Give the freshness check in `soda/lab3_checks.yml` two levels too: a warning when the newest load is more than 12 hours old, and a failure after 1 day. `check.py 3b` shows it on the Extra line.

**Stuck?** `Configuration path ... does not exist`: open a new terminal (menu ☰ > Terminal > New Terminal).
