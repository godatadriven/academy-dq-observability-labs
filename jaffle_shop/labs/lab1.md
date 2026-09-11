# Lab 1 · Six defects, six tests

**20 minutes** · Catch Module 1's six defects with dbt tests, then write two tests of your own.

> This page stays on the left. Click a file name to open it on the right.
> To run a command: copy it, paste it in the terminal, and press Enter.

### 1 · Read the file

Open [`seeds/lab1_tests.yml`](../seeds/lab1_tests.yml). It looks strange at first. Here is the `email` column, line by line:

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
| `- name: email` | One column of the table `orders_daily_extract`, Module 1's "Spot the defects" table. |
| `data_tests:` | The tests on this column. A test is a rule that dbt checks. |
| `# COMPLETENESS ...` | A note for people: the defect and its rule. dbt skips every line that starts with `#`. |
| `- not_null` | A test that is built into dbt. |
| `- dbt_expectations...` | A test from the package `dbt_expectations`: extra tests that someone else wrote. The setup installed it. |
| `arguments:` / `regex:` | The test's settings. |

The file holds five of the six tests. The sixth is a query that returns the bad rows: [`tests/lab1_updated_before_placed.sql`](../tests/lab1_updated_before_placed.sql).

### 2 · Run the tests

```bash
uv run dbt test --select orders_daily_extract
```

**You see:** six lines with `FAIL 1`, and a last line with `ERROR=6`, in red. That is the goal: each test found its bad row. Do not fix the data.

### 3 · Your turn

**Task A.** Finance says: no order is above €1,000. Add a second test under `order_total` for that rule. Keep the first test.

**Task B.** An order cannot be loaded before it is placed. Write that rule as a query test in [`tests/lab1_loaded_before_placed.sql`](../tests/lab1_loaded_before_placed.sql). The columns are `order_date` (placed) and `_loaded_at` (loaded).

**Hint:** Task A uses the same test as the one on `order_total` now: [`expect_column_values_to_be_between`](https://github.com/metaplane/dbt-expectations#expect_column_values_to_be_between). It takes a `min_value`, a `max_value`, or both. In our file, the settings go under `arguments:`. For Task B, dbt's page on [singular tests](https://docs.getdbt.com/docs/build/data-tests) shows the shape.

### 4 · Check

```bash
uv run tools/check.py 1
```

**You see:** `3 of 3 done. Well done.` Your Task A test fails on C-1045, an order of €1,310. Your Task B test fails on the order placed in 2027.

### Extra

One email belongs to one customer. Write that rule as a query test in [`tests/lab1_one_email_one_customer.sql`](../tests/lab1_one_email_one_customer.sql). It passes on this table. `check.py 1` shows it on the Extra line.

**Stuck?** Read the ✗ line: it says what is wrong. Fix it, save with Cmd+S (Ctrl+S on Windows), and check again.
