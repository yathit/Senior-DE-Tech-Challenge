-- select top 3 items purchased by members
WITH cte as
(
   select
      t.item_number,
      item_name,
      count(transaction_number) over (partition by t.item_number) as max_purchase
   from
      sales.transaction t,
      sales.item_master i
   where
      t.item_number = i. item_number
)
select
   item_number,
   item_name,
   max_purchase
from
   cte
order by
   max_purchase desc limit 3;