{{ config(enabled=false) }}
-- LAB 1 · the sixth test, a query. The steps are at the top of seeds/lab1_extract_tests.yml.
-- Switch this file on: on the first line, change false to true.
--
-- CONSISTENCY · an order in 2027, last updated in 2026.
-- Rule: an order is not updated before it is placed, and not placed after today.
-- A singular test is a query that returns the bad rows. Zero rows back means it passes.
-- So write when a row is bad. Fill each blank with a column name or with current_date.
-- The from line is how dbt names a table: ref and the table name, in double curly braces.
-- To start over: git checkout tests/lab1_updated_before_placed.sql
select customer_id, order_date, updated_at
from {{ ref('orders_daily_extract') }}
where order_date > ______
   or order_date > ______
