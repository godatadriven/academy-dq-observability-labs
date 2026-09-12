-- Module 1's example standard, "below 20% repeats": how many of a day's payments equal
-- that customer's previous payment? A first payment has nothing to compare with, so it is
-- not counted. Normal: 4 to 10 in 100. From 1 June: every one.
with ordered as (
    select
        payment_id, customer_id, amount, paid_at::date as pay_date,
        lag(amount) over (partition by customer_id order by paid_at, payment_id) as prev_amount
    from {{ ref('stg_pos_payments') }}
)
select
    pay_date,
    count(*) as payments,
    sum(case when amount = prev_amount then 1 else 0 end) as repeats,
    round(100.0 * sum(case when amount = prev_amount then 1 else 0 end) / count(*), 2) as repeat_rate_pct
from ordered
where prev_amount is not null
group by pay_date
order by pay_date
