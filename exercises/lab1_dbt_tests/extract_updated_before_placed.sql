-- Lab 1 · CONSISTENCY · an order in 2027, last updated in 2026.
-- Rule: an order is not updated before it is placed, and not placed after today.
-- A test is a query that returns the bad rows. Zero rows back means it passes.
-- {{ ref('x') }} is how dbt names the table x. Today, in SQL, is current_date.
select customer_id, order_date, updated_at
from {{ ref('orders_daily_extract') }}
where ______
