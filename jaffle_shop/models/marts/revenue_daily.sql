-- What the revenue dashboard and the finance close read. From 1 June every amount is stale.
select paid_at::date as pay_date, cafe_id,
       count(*) as payments, round(sum(amount) / 100.0, 2) as revenue_eur
from {{ ref('stg_pos_payments') }}
group by 1, 2
order by 1, 2
