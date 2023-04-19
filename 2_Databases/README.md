## Section 2: Databases

### Database and Docker set up

Database Name: ecom_db

Schema Name: sales

### Table Details
* #### Code Tables
  * currency :  Define various currency types for different countries (Ref: item- price)
  * payment_method : List types of payments like cash, nets, credit cards (Ref: Purchase order)
* #### Master Tables
  * manufacture_master : (Supplier details)
  * item_master :  (Product information - ref: manufacture for supplier details)
  * member_master :  ( Customer details)
* #### Transaction Tables
  * transaction : product ordered by customer transaction details of 
  * purchase_order : product purchased by customers

### Entity-Relationship Diagram
![](ecom_ERD_diagram.png)

### Deployment

Run dockers via compose

    docker compose up -d 

### Additional Reference
```
\l - Display database
\c - Connect to database
\dn - List schemas
\dt - List tables inside public schemas
\dt sales. - List tables inside particular sales. For eg: 'sales'.

```
### DML Statement
* Top 10 spending customer
  * Join Item and transaction to get the list of items, weight and price by multiplying quantity from tran as tran_cte
  * Join the above query with purchase order to get over all weight and price as cte2
  * Finally join with member master to get associate member details for max purchase
* Top 3 Items:
  * get the count of transactions for each item
  * from the above query get the maximum purchased item desc and limit by 3.



