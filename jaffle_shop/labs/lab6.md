# Lab 6 · One definition of revenue

**12 minutes** · Define revenue once, and ask the semantic layer.

> This page stays on the left. Click a file name to open it on the right.

### 1 · Ask for revenue

Open [`models/lab6_semantic.yml`](../models/lab6_semantic.yml): the metric `revenue`, owned by Sam.

```bash
uv run mf query --metrics revenue --group-by metric_time__day --start-time 2026-05-31 --end-time 2026-06-02
```

**You see:** three days. 1 June is `4012.8`.

### 2 · Your turn

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

3. Save. Then let dbt read the file:

```bash
uv run dbt parse
```

### 3 · Check

```bash
uv run tools/check.py 6
```

**You see:** `3 of 3 done. Well done.`

**Talk:** every reader now gets 4,012.80 for 1 June. Is it right?

**Stuck?** An error about the file: check the spaces, and run `uv run dbt parse` again.
