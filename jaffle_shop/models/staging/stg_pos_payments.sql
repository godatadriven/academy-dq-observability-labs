-- The payments table, with a patch. A developer wrote it in 2023, when card terminals sometimes
-- sent no amount: "empty amount? Use this customer's last amount. No last amount? Use 0."
-- Since 1 June every amount is empty. So every payment gets the customer's last May amount,
-- at the old price, and a first-time customer gets 0. This is the payments table.
select
    payment_id,
    customer_id,
    cafe_id,
    payment_method,
    coalesce(
        amount,
        last_value(amount ignore nulls) over (
            partition by customer_id
            order by paid_at, payment_id
            rows between unbounded preceding and 1 preceding
        ),
        0
    ) as amount,
    paid_at,
    _etl_loaded_at
from {{ ref('stg_pos_events') }}
