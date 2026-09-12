# Lab 1 · Six defects, six tests

> **15 minutes** · **Goal:** catch Module 1's six defects with dbt tests.<br>
> **You write:** a range test, and a query test.<br>
> **Done when:** `uv run tools/check.py 1` says `3 of 3 done. Well done.`

This page stays on the left. Click a file name to open the file on the right. To run a command, copy it, paste it in the terminal, and press Enter.

### 1 · Read the file

Open [`seeds/lab1_tests.yml`](../seeds/lab1_tests.yml). It holds five of the six tests. Here is the `email` column:

```yaml
      - name: email
        data_tests:
          # COMPLETENESS · an email is missing. Rule: email is not empty.
          - not_null
          # VALIDITY · "(at)" is not an email address. Rule: ...
          - dbt_expectations.expect_column_values_to_match_regex:
              arguments:
                regex: ".+@.+\\..+"
```

| Line | What it means |
| --- | --- |
| `- name: email` | One column of Module 1's "Spot the defects" table. |
| `data_tests:` | The tests on this column. A test is a rule that dbt checks. |
| `# COMPLETENESS ...` | A note for people: the defect and its rule. dbt skips it. |
| `- not_null` | A test built into dbt. |
| `- dbt_expectations...` | A test from the package `dbt_expectations`. The setup installed it. |
| `arguments:` / `regex:` | The test's settings. |

The sixth test is a query: [`tests/lab1_updated_before_placed.sql`](../tests/lab1_updated_before_placed.sql). You read it in Task 2.

### 2 · Run the tests

```bash
uv run dbt test --select orders_daily_extract
```

You see six lines with `FAIL 1`. The last line starts like this:

```
Done. PASS=0 WARN=0 ERROR=6 ...
```

Six failures is the goal: each test found its bad row. Do not fix the data.

---

### 3 · Your turn

**Task 1 · A range.** Finance says: no order is above €1,000. Add a second test under `order_total` for that rule. Keep the first test.

> **Hint:** the test on `order_total` is [`expect_column_values_to_be_between`](https://github.com/metaplane/dbt-expectations#expect_column_values_to_be_between). It takes a `min_value`, a `max_value`, or both. In our file, the settings go under `arguments:`.

**Task 2 · A query.** A query test is a SELECT that returns the bad rows. No rows back means that the test passes. Here is the one in [`tests/lab1_updated_before_placed.sql`](../tests/lab1_updated_before_placed.sql):

```sql
select customer_id, order_date, updated_at
from {{ ref('orders_daily_extract') }}
where order_date > updated_at
   or order_date > current_date
```

| Line | What it means |
| --- | --- |
| `select ...` | The columns to show for each bad row. |
| `from {{ ref('orders_daily_extract') }}` | The table. `ref(...)` is how dbt names a table. |
| `where ...` | The rule, turned around: keep only the rows that break it. |

Write a new rule the same way: **no order is loaded before its order date.** The columns are `order_date` (the day the order was placed) and `_loaded_at` (the moment the row arrived in the table). Write it in [`tests/lab1_loaded_before_placed.sql`](../tests/lab1_loaded_before_placed.sql), under the comments.

### 4 · Check

```bash
uv run tools/check.py 1
```

```
3 of 3 done. Well done.
```

Your range test fails on C-1045, an order of €1,310. Your query fails on the order placed in 2027.

---

### Extra (optional)

One email belongs to one customer. Write that rule as a query test in [`tests/lab1_one_email_one_customer.sql`](../tests/lab1_one_email_one_customer.sql). It passes on this table.

### Stuck?

- A ✗ line says what is wrong. Fix it, save (Cmd+S, or Ctrl+S on Windows), and check again.
- "Gone, or not failing now": one of the six tests changed. Your range test must be a second test, not a change to the first.
