## Section 3: System Design - Design 1


### Implementation Strategy

Database Name: ecom

Schema Name: sales

Create role for each departments

1. logistics: Logistics: Update to `item_master` and `transaction`
2. analytics: Analytics: Read to all table
3. sales: Sales: Create and delete to `sales`

### Role creation

create roles for each department

```postgresql
create role logistics login password 'abcdef';
create role analytics login password 'abcdef';
create role sales login password 'abcdef';
```


Then, grant access for the user role base on requirements.

```postgresql

GRANT UPDATE ON "item_master" IN SCHEMA "sales" TO  logistics;
GRANT UPDATE ON "transaction" IN SCHEMA "sales" TO  logistics;

GRANT SELECT ON ALL TABLES IN SCHEMA "sales" TO  analytics;

GRANT INSERT, DELETE ON item_master IN SCHEMA "sales" TO  sales;

```



