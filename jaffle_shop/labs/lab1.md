# Lab 1 · Six defects, six tests

**20 minutes** · See Module 1's six defects caught by dbt tests.

> This page stays on the left. Click a file name, and it opens on the right.
> To run a command: copy it from the grey box, paste it in the terminal, press Enter.

### 1 · Run the tests

Open [`seeds/lab1_tests.yml`](../seeds/lab1_tests.yml): one test per defect. The table is a seed, a CSV file that dbt loads.

```bash
uv run dbt test --select orders_daily_extract
```

**You see:** six lines with `FAIL 1`, then `ERROR=6`. Each failed test found a bad row.

**Talk:** which test catches which defect?

### 2 · Your turn

Finance says: no order is above €1,000. Write that rule as a new test.
Under `order_total`, copy the test that is there, and change `min_value: 0` to `max_value: 1000` in your copy. Keep the first test. Save: Cmd+S, or Ctrl+S on Windows.

**Talk:** your test fails on C-1045, €1,310. Is the order wrong, or is the rule wrong?

### 3 · Check

```bash
uv run check.py 1
```

**You see:** two lines with ✓, and `2 of 2 done. Well done.`

**Stuck?** A line with ✗ says what to do. Nothing changed after an edit: save the file.
