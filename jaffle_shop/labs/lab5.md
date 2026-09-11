# Lab 5 · One definition of revenue

> **12 minutes** · **Goal:** revenue defined once, in a semantic layer, so every reader gets the same number.<br>
> **You write:** two metrics, `payments` and `average_payment`.<br>
> **Done when:** `uv run tools/check.py 5` says `3 of 3 done. Well done.`

### 1 · Read the file

Open [`models/lab5_semantic.yml`](../models/lab5_semantic.yml). A semantic layer defines each metric once. Every reader asks it, instead of writing its own sum. The file has two parts: `semantic_models`, the numbers that can be added up, and `metrics`, the names that readers ask for. Here are the lines that matter:

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

The file has a second measure too: `payment_count`, one for each payment.

### 2 · Ask for revenue

`mf` is MetricFlow, the command that asks the semantic layer. `metric_time__day` means: one row per day.

```bash
uv run mf query --metrics revenue --group-by metric_time__day --start-time 2026-05-31 --end-time 2026-06-02
```

```
2026-05-31T00:00:00     5783
2026-06-01T00:00:00     4012.8
2026-06-02T00:00:00     3799.3
```

A message about a new version of MetricFlow can show too. Ignore it.

---

### 3 · Your turn

Add two metrics under `revenue`, where the comment says "Your turn".

**Task 1.** `payments`: the number of payments on a day.

**Task 2.** `average_payment`: revenue divided by payments.

> **Hint:** Task 1 has the same shape as `revenue`, with the other measure. Copy the shape in our file, not the one on dbt's page. Task 2 is a [ratio metric](https://docs.getdbt.com/docs/build/ratio): it divides one metric by another.

After a change, let dbt read the file, then ask again:

```bash
uv run dbt parse
uv run mf query --metrics revenue,payments,average_payment --group-by metric_time__day --start-time 2026-06-01 --end-time 2026-06-01
```

You see `4012.8`, `576`, and `6.96667`.

### 4 · Check

```bash
uv run tools/check.py 5
```

```
3 of 3 done. Well done.
```

---

### Extra (optional)

Ask for revenue by payment method. Add `payment_method` as a dimension of the semantic model, next to `paid_at`: it is `categorical` (dbt's page on [dimensions](https://docs.getdbt.com/docs/build/dimensions)). Then run `uv run dbt parse`, and ask:

```bash
uv run mf query --metrics revenue --group-by payment__payment_method --start-time 2026-06-01 --end-time 2026-06-01
```

You see four payment methods. `credit_card` is `2653.5`.

### Stuck?

- A ✗ line says what is wrong. Fix it, save (Cmd+S, or Ctrl+S on Windows), and check again.
- An error about the file: the spaces at the start of a line you added do not line up. Fix them, and run `uv run dbt parse` again.
