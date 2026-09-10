# Lab 6 · One definition of revenue

**12 minutes** · Define revenue once, and ask the semantic layer for it.

> This page stays on the left. Click a file name, and it opens on the right.

### 1 · Ask for revenue

Open [`models/lab6_semantic.yml`](../models/lab6_semantic.yml): the metric `revenue`, Module 1's one definition, owner Sam. `mf` is the semantic layer's command.

```bash
uv run mf query --metrics revenue --group-by metric_time__day --start-time 2026-05-31 --end-time 2026-06-02
```

**You see:** three rows: `5783` for 31 May, `4012.8` for 1 June, `3799.3` for 2 June.

**Talk:** the dashboard, the finance close, and the agent now all get 4,012.80 for 1 June. Is it right?

### 2 · Your turn

Add two metrics under `revenue`, in the same shape:

1. `payments`: the number of payments. Type `simple`, with the measure `payment_count`.
2. `average_payment`: revenue divided by payments. Type `ratio`:

```yaml
  - name: average_payment
    label: Average payment
    type: ratio
    type_params:
      numerator: revenue
      denominator: payments
```

Save. Then let dbt read the file again:

```bash
uv run dbt parse
```

### 3 · Check

```bash
uv run check.py 6
```

**You see:** `3 of 3 done. Well done.` For 1 June: 576 payments, and 6.97 on average.

**Done early?** Ask both metrics at once:

```bash
uv run mf query --metrics revenue,payments,average_payment --group-by metric_time__day --start-time 2026-05-31 --end-time 2026-06-02
```

**Stuck?** An error about the file: keep the spaces as they are, and run `uv run dbt parse` again.
