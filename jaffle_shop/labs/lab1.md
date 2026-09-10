# Lab 1 · Six defects, six tests

**Goal:** see Module 1's six defects caught by dbt tests. **Time:** 30 minutes.

> Keep this page on the right: drag its tab to the right half of the window. Click a file name on the page to open the file.

1. Open [`seeds/lab1_tests.yml`](../seeds/lab1_tests.yml). Each comment names one defect from Module 1's "Spot the defects". The table is a seed: a CSV file that dbt loads. So the file starts with `seeds:`, not `models:`.
2. Run:

   ```bash
   uv run dbt test --select orders_daily_extract
   ```

   `--select` runs only the tests on that table. You see: six lines with `FAIL 1`. The last line says `ERROR=6`: dbt counts a failed test as an error. Each test found one bad row.
3. Answer: which test catches which defect?
4. Answer: which test is built in, which come from the package `dbt_expectations`, and which one is a query? The query is [`tests/lab1_updated_before_placed.sql`](../tests/lab1_updated_before_placed.sql).
5. Change `min_value: 0` to `min_value: -200`. Save (Cmd+S, or Ctrl+S on Windows). Run step 2 again.

   You see: `ERROR=5`. Answer: why does that test pass now? Then change it back to `0`.

**Done early?** Why do most of the six need more than a built-in test?

**Stuck?** Nothing changed after an edit: save the file, then run it again.
