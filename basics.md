# The basics

Ten minutes, before the day. Read it once, after the setup. The labs expect that you know these three things.

## The terminal

The terminal is at the bottom of your codespace. You paste a command and press Enter.

- Copy one command from a lab page, paste it, and press Enter. Wait until it finishes.
- Press ↑ to get the last command back. Press Ctrl+C to stop a command.
- Lost? Close the terminal with the bin icon, and open a new one: menu (☰) > **Terminal** > **New Terminal**.

The last line tells you the result:

| Last line | Meaning |
| --- | --- |
| `Done. PASS=4 WARN=0 ERROR=0 ...` | dbt: four tests passed, none failed. |
| `Done. PASS=0 WARN=0 ERROR=6 ...` | dbt: six tests failed. dbt counts a failed test as an error. |
| `All is good. No failures. No warnings. No errors.` | Soda: every check passed. |
| `Oops! 2 failures. 0 warnings. 0 errors. 2 pass.` | Soda: two checks failed. The lines above say which ones. |

## A YAML file

A YAML file holds settings as plain text. dbt and Soda read their tests and checks from YAML files. Here is part of `jaffle_shop/models/schema.yml`:

```yaml
# The payments table and its tests.
models:
  - name: stg_pos_payments
    columns:
      - name: payment_id
        data_tests: [unique]
      - name: payment_method
        data_tests:
          - accepted_values:
              arguments:
                values: ['credit_card', 'coupon', 'bank_transfer', 'gift_card']
```

| You see | It means |
| --- | --- |
| `# The payments table` | A comment: a note for people. The tool ignores everything after `#` on the line. |
| `name: payment_id` | A setting: a name, a colon, a space, then the value. |
| `- name: ...` | A dash starts one item of a list. Here, each dash is one column. |
| The spaces at the start | They show what belongs to what. `data_tests` is inside the column `payment_id`. |
| `[unique]` | A short list on one line. `[a, b]` is the same as two dash lines. |
| `'credit_card'` | A value in quotes. Keep the quotes that are there. |

When you change a value, keep the spaces and the quotes around it. Use spaces, never tabs.

## A query

A dbt test can also be a SQL query. It returns the bad rows. No rows back means that the test passes.

```sql
select customer_id, order_date
from {{ ref('orders_daily_extract') }}
where order_date > current_date
```

- `select` names the columns to show. `from` names the table. `where` keeps only the rows that match.
- `{{ ref('orders_daily_extract') }}` is how dbt names the table `orders_daily_extract`.
- `current_date` is today.
