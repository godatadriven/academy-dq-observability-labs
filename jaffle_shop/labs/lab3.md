# Lab 3 · Checks on the payments table

**Part A 15 minutes, Part B 10 minutes** · Write a Soda check, and set a limit that catches the Frozen Payments.

> This page stays on the left. Click a file name to open it on the right.

## Part A · A normal morning

### 1 · Read the file

Open [`soda/lab3_checks.yml`](../soda/lab3_checks.yml): three Soda checks. Here is the first:

```yaml
checks for stg_pos_payments:
  - freshness(_etl_loaded_at) < 1d:
      name: "freshness: the copy ran last night"
      filter: _etl_loaded_at <= '${NOW}'::timestamp
```

| Line | What it means |
| --- | --- |
| `checks for stg_pos_payments:` | The table these checks look at. |
| `- freshness(_etl_loaded_at) < 1d:` | The check: what must be true. Here, the newest load is less than one day old. |
| `name:` | The rule in words. The scan prints it. |
| `filter:` | Which rows to look at: only what was loaded before `NOW`. |

`NOW` is the morning the scan pretends it is. You set it in the command.

### 2 · Scan Sunday 31 May

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/lab3_checks.yml
```

**You see:** `All is good`.

### 3 · Your turn

Add a fourth check: every payment has a customer. Add these lines under the others, and save. **Hint:** Soda's page on [missing metrics](https://docs.soda.io/soda-cl/missing-metrics.html) explains `missing_count`.

```yaml
  - missing_count(customer_id) = 0:
      name: "completeness: every payment has a customer"
```

```bash
uv run tools/check.py 3a
```

**You see:** `2 of 2 done. Well done.`

**Stop here.** Part B starts at the slide "Catch the Case".

## Part B · Catch the case

### 4 · Scan a normal day

Open [`soda/lab3_repeat.yml`](../soda/lab3_repeat.yml). `repeat_rate < 5` is the check: what must be true. `repeat_rate query` is the SQL that gives the day's percent of repeats. The limit is 5.

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-26 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
```

**You see:** it fails on a normal day, 26 May. The limit is too tight.

### 5 · Your turn

Change the `5` to a limit that is quiet all of May, but rings on 2 June. Save, and check:

```bash
uv run tools/check.py 3b
```

**You see:** `2 of 2 done. Well done.` A ✗ line names the day your limit gets wrong.

### 6 · Scan 2 June

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-06-02 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
```

**You see:** `Oops! 2 failures`. Your checks catch the Frozen Payments.

**Talk:** why is the 1 June scan still green?

**Stuck?** `Configuration path ... does not exist`: open a new terminal (menu ☰ > Terminal > New Terminal).
