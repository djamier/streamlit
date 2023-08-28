select
    order_date::date as order_date
    , order_source
    , sum(total_price) as total_sales
from fct_orders
where
    order_date between {start_date_str}::timestamp and {end_date_str}::timestamp
    and order_status = 'Completed'
group by 1, 2
order by 1
