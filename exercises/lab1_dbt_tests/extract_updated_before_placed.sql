-- Lab 1 · CONSISTENCY · an order in 2027, last updated in 2026.
-- Rule: an order is not updated before it is placed, and not placed after today.
-- A test is a query that returns the bad rows. Zero rows back means it passes.
-- Copy to jaffle_shop/tests/extract_updated_before_placed.sql
select customer_id, order_date, updated_at
from {{ ref('orders_daily_extract') }}
where ______
