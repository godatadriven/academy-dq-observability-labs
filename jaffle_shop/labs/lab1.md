# Lab 1 · Six defects, six tests

**20 minutes** · Catch Module 1's six defects with dbt tests.

> This page stays on the left. Click a file name to open it on the right.
> To run a command: copy it, paste it in the terminal, press Enter.

### 1 · Run the tests

Open [`seeds/lab1_tests.yml`](../seeds/lab1_tests.yml). There is one test for each defect.

```bash
uv run dbt test --select orders_daily_extract
```

**You see:** six lines with `FAIL 1`. Each test found a bad row.

### 2 · Your turn

Finance says: no order is above €1,000. Add that test.

1. Under `order_total`, copy the test that is there.
2. In your copy, change `min_value: 0` to `max_value: 1000`.
3. Save: Cmd+S, or Ctrl+S on Windows.

### 3 · Check

```bash
uv run check.py 1
```

**You see:** `2 of 2 done. Well done.`

**Talk:** your test fails on one order of €1,310. Is the order wrong, or the rule?

**Stuck?** A ✗ line tells you what to fix.
