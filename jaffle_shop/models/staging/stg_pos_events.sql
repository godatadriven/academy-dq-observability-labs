-- The parse. Every night at 03:30 it reads the day's events from raw, where the payment app puts them.
-- Until 31 May an event says {"amount": 3.50}. On 1 June the payment app ships API v2.4,
-- and an event says {"amount_cents": 450}. The parse still reads "amount".
-- A field that is not there comes back empty, not as an error. So the parse never fails.
select
    payment_id,
    customer_id,
    cafe_id,
    payment_method,
    cast(round(cast(json_extract_string(event, '$.amount') as decimal(10, 2)) * 100) as integer) as amount,
    paid_at,
    _etl_loaded_at
from {{ ref('raw_pos_payments') }}
