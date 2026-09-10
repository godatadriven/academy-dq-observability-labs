# Lab 6 · One definition of revenue

**12 minutes** · Define revenue once, and ask the semantic layer.

> This page stays on the left. Click a file name to open it on the right.

### 1 · Read the file

Open [`models/lab6_semantic.yml`](../models/lab6_semantic.yml). It has two parts. Here are the lines that matter:

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
| `measures:` | Numbers the semantic layer can add up, from the payments table. |
| `- name: amount_eur` | One measure: the amount of each payment, in euros. |
| `agg: sum` / `expr: amount / 100.0` | How: add up `amount`, divided by 100, because amounts are in cents. |
| `- name: revenue` | The metric: the name every reader asks for. |
| `type: simple` / `measure: amount_eur` | A simple metric is one measure. Here, revenue is the sum of the amounts. |

### 2 · Ask for revenue

```bash
uv run mf query --metrics revenue --group-by metric_time__day --start-time 2026-05-31 --end-time 2026-06-02
```

**You see:** three days. 1 June is `4012.8`.

### 3 · Your turn

Add two metrics under `revenue`:

1. `payments`: the number of payments. Copy the `revenue` block. Change the name, the label, and the measure to `payment_count`.
2. `average_payment`: revenue divided by payments. Add these lines:

```yaml
  - name: average_payment
    label: Average payment
    type: ratio
    type_params:
      numerator: revenue
      denominator: payments
```

3. Save. Then let dbt read the file. **Hint:** dbt's pages on [simple metrics](https://docs.getdbt.com/docs/build/simple) and [ratio metrics](https://docs.getdbt.com/docs/build/ratio).

```bash
uv run dbt parse
```

### 4 · Check

```bash
uv run tools/check.py 6
```

**You see:** `3 of 3 done. Well done.`

**Talk:** every reader now gets 4,012.80 for 1 June. Is it right?

**Stuck?** An error about the file: check the spaces, and run `uv run dbt parse` again.
