-- To Extract top 10 member spending
with tran_cte as
(
   select
      membership_id,
      transaction_number,
      item_name,
      (
         quantity * item_weight
      )
      as tran_cost,
      (
         quantity * item_unit_cost
      )
      as tran_weight
   from
      sales.item_master i,
      sales.transaction t
   where
      t.item_number = i. item_number
)
,
outer_cte as
(
   select
      t1.membership_id,
      item_name,
      sum(tran_weight) OVER(PARTITION BY purchase_number) as total_items_weight,
      sum(tran_cost) OVER(PARTITION BY purchase_number) as total_items_price
   from
      sales.purchase_order p,
      tran_CTE t1
   where
      p.transaction_number = t1.transaction_number
)
select
   m.membership_id,
   first_name,
   last_name,
   total_items_price,
   total_items_weight
from
   outer_cte o,
   sales.member_master m
where
   m.membership_id = o.membership_id
order by
   total_items_price desc limit 10;