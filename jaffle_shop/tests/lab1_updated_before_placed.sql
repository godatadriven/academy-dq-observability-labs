-- Lab 1 · CONSISTENCY · an order placed in 2027 and updated in 2026. The steps: labs/lab1.md
-- Rule: an order is not updated before it is placed, and not placed after today.
-- A test query returns the bad rows. No rows back means that the test passes.
select customer_id, order_date, updated_at
from {{ ref('orders_daily_extract') }}
where order_date > updated_at
   or order_date > current_date
