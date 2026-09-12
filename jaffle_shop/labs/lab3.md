# Lab 3 · Soda checks, from the raw events to the payments table

> **Part A 15 minutes, Part B 10 minutes** · **Goal:** Soda checks that pass on a normal morning, and catch the Frozen Payments.<br>
> **You write:** Part A, one check on the raw events. Part B, a warning level and a failure level.<br>
> **Done when:** `uv run tools/check.py 3a`, then `uv run tools/check.py 3b`, say `Well done.`

## Part A · A normal morning

### 1 · Read the file

Open [`soda/lab3_checks.yml`](../soda/lab3_checks.yml): three Soda checks on the payments table. Soda looks at a table as it is now, and says PASSED or FAILED for each check. Here is the first:

```yaml
checks for stg_pos_payments:
  - freshness(_etl_loaded_at) < 1d:
      name: "freshness: last night's data is here"
      filter: _etl_loaded_at <= '${NOW}'::timestamp
```

| Line | What it means |
| --- | --- |
| `checks for stg_pos_payments:` | The table that Soda scans: the payments table. |
| `- freshness(_etl_loaded_at) < 1d:` | The check: what must be true. Here, the newest load is less than one day older than `NOW`, the morning of the scan. |
| `name:` | The rule in words. The scan prints it. |
| `filter:` | Which rows to look at: only what was loaded before `NOW`. |

The other two checks have the same shape.

### 2 · Scan a normal morning

A scan runs every check once. `NOW` is the morning that the scan pretends it is: here, 31 May, the day before the rename.

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/lab3_checks.yml
```

```
3/3 checks PASSED
All is good. No failures. No warnings. No errors.
```

---

### 3 · Your turn

The payment team owns the raw events: the messages from the payment app, before any dbt model. They load them with their own sync, not with dbt, so no dbt test looks at them. Soda can check their table anyway. In the sandbox, a dbt seed stands in for their sync.

Open [`soda/lab3_raw.yml`](../soda/lab3_raw.yml). It holds one check, with its shape ready:

```yaml
checks for raw_pos_payments:
  - events_without_amount = 0:
      events_without_amount query: |
        select count(*)
        from raw_pos_payments
        where paid_at >= '${NOW}'::date - interval 1 day and paid_at < '${NOW}'::date
          and false
      name: "raw: every event of yesterday has an amount"
```

| Line | What it means |
| --- | --- |
| `- events_without_amount = 0:` | The check: this number must be 0. You name the number yourself. |
| `events_without_amount query:` | The SQL that gives the number. |
| `where paid_at ...` | Only yesterday's events, the morning in `NOW`. |
| `and false` | A placeholder: it counts nothing, so the check always passes. |

**Task.** Replace `false` with the rule: the event has no `amount` field. Each event is a JSON text in the column `event`, like `{"customer": 3091, "amount": 7.30}`.

> **Hint:** DuckDB reads one field from a JSON text with [`json_extract_string`](https://duckdb.org/docs/data/json/json_functions). A field that is not there comes back empty: `is null`.

Scan 31 May, the day before the rename. Your check must pass: yesterday's events all have an amount.

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/lab3_raw.yml
```

### 4 · Check

```bash
uv run tools/check.py 3a
```

```
3 of 3 done. Well done.
```

**Extra (optional).** Add a second check to `soda/lab3_raw.yml`: last night brought between 500 and 700 events. The volume check in `soda/lab3_checks.yml` has the shape.

> **Stop here.** Part B starts at the slide "Catch the Case".

---

## Part B · Catch the case

### 5 · Read the file

Open [`soda/lab3_repeat.yml`](../soda/lab3_repeat.yml). It is Module 1's rule: alert when too many payments repeat the customer's last amount.

```yaml
checks for payments_repeat_rate:
  - repeat_rate < 5:
      repeat_rate query: |
        select repeat_rate_pct from payments_repeat_rate where ...
      name: "distribution: payments do not repeat the customer's last amount"
```

| Line | What it means |
| --- | --- |
| `checks for payments_repeat_rate:` | A table with one row per day: the percent of payments that repeat the customer's last amount. |
| `- repeat_rate < 5:` | The check: the day's percent is below 5. The limit is 5. |
| `repeat_rate query:` | The SQL that gives that percent, for the day before `NOW`. |

A scan in the morning reads the payments of the day before.

### 6 · Scan a normal morning

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-26 09:00:00" soda/lab3_repeat.yml
```

```
check_value: 9.46
Oops! 1 failures. 0 warnings. 0 errors. 0 pass.
```

On a normal day, 9.46% of the payments repeat. A limit of 5 is too tight.

---

### 7 · Your turn

One limit is not enough: a normal day repeats 4 to 10%, and 2 June repeats 100%.

**Task.** Give the check two levels:

- a **warning** when more than 10% repeat: someone looks at it,
- a **failure** when more than 20% repeat, Module 1's one in five: the line stops.

A check with two levels has no limit in its check line. Change the line to only `- repeat_rate:`. Then put `warn:` and `fail:` straight under it, six spaces in, the same as `name:`. Not inside the SQL.

> **Hint:** Soda's page on [alert configurations](https://docs.soda.io/soda-cl/optional-config.html), with `warn: when > ...` and `fail: when > ...`.

### 8 · Check

```bash
uv run tools/check.py 3b
```

```
3 of 3 done. Well done.
```

`check.py` also scans the morning of 20 May. That scan warns, on purpose. 19 May's rate, 10.26%, is high only because the sandbox starts on 17 May, so few payments have one before them. A warning asks someone to look. It is not an alarm.

### 9 · Scan 2 June

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-06-02 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml soda/lab3_raw.yml
```

The last line starts with `Oops! 3 failures.` Your checks catch the Frozen Payments on the first morning: at the source, in the raw events, and in the payments table.

---

### Extra (optional)

Give the freshness check two levels too: a warning when the newest load is more than 12 hours old, and a failure after 1 day. Soda writes these as `12h` and `1d`.

### Stuck?

- A ✗ line says what is wrong. Fix it, save (Cmd+S, or Ctrl+S on Windows), and check again.
- `Configuration path ... does not exist`: the scan ran from the wrong folder. Open a new terminal: menu ☰ > Terminal > New Terminal.
