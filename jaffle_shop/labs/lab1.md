# Lab 1 · Six defects, six tests

**20 minutes** · Catch Module 1's six defects with dbt tests.

> This page stays on the left. Click a file name to open it on the right.
> To run a command: copy it, paste it in the terminal, press Enter.

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
| `- name: email` | One column. |
| `data_tests:` | Its tests. |
| `# COMPLETENESS ...` | A note: the defect and its rule. dbt skips it. |
| `- not_null` | A built-in test. |
| `- dbt_expectations...` | A test from a package. Setup installed it. |
| `regex: ...` | The test's setting. |

The sixth test does not fit in this file. It is a query that returns the bad rows: [`tests/lab1_updated_before_placed.sql`](../tests/lab1_updated_before_placed.sql).

### 2 · Run the tests

```bash
uv run dbt test --select orders_daily_extract
```

**You see:** six lines with `FAIL 1`. Six failures is the goal: each test found its bad row. Do not fix them.

### 3 · Your turn

Finance says: no order is above €1,000. Add that test.

1. Under `order_total`, copy the test that is there.
2. In your copy, change `min_value: 0` to `max_value: 1000`.
3. Save: Cmd+S, or Ctrl+S on Windows.

**Hint:** the test is [`expect_column_values_to_be_between`](https://github.com/metaplane/dbt-expectations#expect_column_values_to_be_between), from the package `dbt_expectations`. It takes a `min_value`, a `max_value`, or both.

### 4 · Check

```bash
uv run tools/check.py 1
```

**You see:** `2 of 2 done. Well done.`

**Talk:** your test fails on one order of €1,310. Is the order wrong, or the rule?

**Stuck?** A ✗ line tells you what to fix.
