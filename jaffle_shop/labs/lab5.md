# Lab 5 · One definition of revenue

**12 minutes** · Define revenue once, in a semantic layer, and add two metrics of your own.

> This page stays on the left. Click a file name to open it on the right.

### 1 · Read the file

Open [`models/lab5_semantic.yml`](../models/lab5_semantic.yml). A semantic layer defines each metric once. Every reader asks it, instead of writing its own sum. The file has two parts: `semantic_models`, what can be added up, and `metrics`, the names that readers ask for. Here are the lines that matter:

```yaml
    measures:
      - name: amount_eur
        agg: sum
        expr: amount / 100.0

metrics:
  - name: revenue
    type: simple
    type_params:
      measure: amount_eur
```

| Line | What it means |
| --- | --- |
| `measures:` | Numbers from the payments table that can be added up or counted. |
| `- name: amount_eur` | One measure: the amount of each payment, in euros. |
| `agg: sum` / `expr: amount / 100.0` | How: add up `amount`, divided by 100, because the amounts are in cents. |
| `- name: revenue` | The metric: the name that every reader asks for. |
| `type: simple` / `measure: amount_eur` | A simple metric is one measure. Here, revenue is the sum of the amounts. |

The file also has a second measure, `payment_count`: one for each payment.

### 2 · Ask for revenue

`mf` is MetricFlow, the command that asks the semantic layer. `metric_time__day` means: one row per day.

```bash
uv run mf query --metrics revenue --group-by metric_time__day --start-time 2026-05-31 --end-time 2026-06-02
```

**You see:** three days. 1 June is `4012.8`.

### 3 · Your turn

Add two metrics under `revenue`, where the comment says "Your turn".

**Task A.** `payments`: the number of payments on a day.

**Task B.** `average_payment`: revenue divided by payments.

**Hint:** dbt's pages on [simple metrics](https://docs.getdbt.com/docs/build/simple) (Task A) and [ratio metrics](https://docs.getdbt.com/docs/build/ratio) (Task B). A ratio metric divides one metric by another.

After a change, let dbt read the file, then ask again:

```bash
uv run dbt parse
uv run mf query --metrics revenue,payments,average_payment --group-by metric_time__day --start-time 2026-06-01 --end-time 2026-06-01
```

**You see:** `4012.8`, `576`, and `6.96667`.

### 4 · Check

```bash
uv run tools/check.py 5
```

**You see:** `3 of 3 done. Well done.`

### Extra

Ask for revenue by payment method. Add `payment_method` as a dimension of the semantic model, next to `paid_at`, and group by `payment__payment_method`. **Hint:** dbt's page on [dimensions](https://docs.getdbt.com/docs/build/dimensions): a payment method is `categorical`.

**Stuck?** An error about the file: the spaces at the start of a line you added do not line up. Fix them, and run `uv run dbt parse` again.
