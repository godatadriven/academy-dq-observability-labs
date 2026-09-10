# Lab 3 · Checks on the payments table

**Part A 15 minutes, Part B 10 minutes** · See which checks ring on 2 June, and set a limit that works.

> This page stays on the left. Click a file name, and it opens on the right.

## Part A · A normal morning

### 1 · Scan Sunday 31 May

Open [`soda/lab3_checks.yml`](../soda/lab3_checks.yml): three checks, freshness, volume, and validity. `NOW` is the morning the scan pretends it is. Each scan reads yesterday's payments.

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/lab3_checks.yml
```

**You see:** `3/3 checks PASSED` and `All is good`.

**Talk:** which check rings if the copy did not run last night?

### 2 · Your turn

Write a fourth check: every payment has a customer. In the file, add it under the others, in the same shape:

```yaml
  - missing_count(customer_id) = 0:
      name: "completeness: every payment has a customer"
```

Save. Then check it:

```bash
uv run check.py 3a
```

**You see:** `2 of 2 done. Well done.`

**Stop here.** Part B starts at the slide "Catch the Case".

## Part B · Catch the case

### 3 · Scan a normal morning with Module 1's rule

Open [`soda/lab3_repeat.yml`](../soda/lab3_repeat.yml): ring when too many payments repeat the customer's last amount. Someone set the limit to 5. Scan 26 May, a normal day:

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-26 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
```

**You see:** the distribution check fails, with `check_value: 9.46`. A normal day rings.

### 4 · Your turn

Find a limit that stays quiet on every normal morning in May, and still rings on 2 June. Change the `5` in `repeat_rate < 5`. Save.

### 5 · Check

```bash
uv run check.py 3b
```

**You see:** `2 of 2 done. Well done.` A line with ✗ says which day your limit gets wrong.

### 6 · Scan 2 June

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-06-02 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
```

**You see:** `Oops! 2 failures`: validity with `check_value: 41`, the new customers set to 0, and distribution with `check_value: 100.0`, every returning customer.

**Done early?** Scan 15 June, the Monday after a busy Sunday. Which check rings only for the busy Sunday?

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-06-15 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
```

**Stuck?** `Configuration path ... does not exist`: open a new terminal (menu ☰ > Terminal > New Terminal).
