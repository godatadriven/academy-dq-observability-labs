-- One row per day. The semantic layer (Lab 5) needs it to group a metric by day.
select cast(range as date) as date_day
from range(date '2026-05-01', date '2026-07-01', interval 1 day)
