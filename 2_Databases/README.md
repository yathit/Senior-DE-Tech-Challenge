## Section 2: Databases

### Database and Docker set up

Database Name: ecom

Schema Name: sales

### Table Details

Code Tables

  * currency :  Define various currency types for different countries (Ref: item- price)
  * payment_method : List types of payments like cash, nets, credit cards (Ref: Purchase order)

Master Tables

  * manufacture_master : (Supplier details)
  * item_master :  (Product information - ref: manufacture for supplier details)
  * member_master :  ( Customer details)

Transaction Tables

  * transaction : product ordered by customer transaction details of 
  * purchase_order : product purchased by customers

### Entity-Relationship Diagram

![ERD](sales.png)

The diagram is produced by IntellJ DataGrid from the PostgreSQL DB after running the ddl script. 

### Deployment

Run dockers via compose

    docker compose up -d 

### Analytics query

1. Which are the top 10 members by spending

* Join Item and transaction to get the list of items, weight and price by multiplying quantity from tran as tran_cte
* Join the above query with purchase order to get over all weight and price as cte2
* Finally join with member master to get associate member details for max purchase

Require indexes

1. item_master.item_number (auto)
2. transaction.item_number (auto)
3. member_master.membership_id, member_master.total_items_price



2. Which are the top 3 items that are frequently brought by members

* get the count of transactions for each item
* from the above query get the maximum purchased item desc and limit by 3.

Require indexes

1. transaction.item_number, transaction.transaction_number
2. item_master.item_number (auto)