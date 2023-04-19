

DROP SCHEMA IF EXISTS sales CASCADE;
CREATE SCHEMA sales;
SET search_path TO sales;

-- Code tables


-- Master tables
CREATE TABLE IF NOT EXISTS sales.manufacture_master (
  manufacture_cd  serial PRIMARY KEY,
  manufacture_name varchar(100),
  country varchar(100),
  address varchar(255),
  added_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  added_by varchar(20),
  updated_by varchar(20)

);


CREATE TABLE IF NOT EXISTS sales.item_master (
  item_number  serial PRIMARY KEY,
  item_name varchar(255),
  item_weight float,
  item_measure_units varchar(10),
  item_unit_cost float,
   manufacture_cd int,
  currency_cd varchar(3),
  added_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  added_by varchar(20),
  updated_by varchar(20)

);

ALTER TABLE sales.item_master ADD FOREIGN KEY (manufacture_cd) REFERENCES sales.manufacture_master (manufacture_cd);


CREATE TABLE IF NOT EXISTS sales.member_master (
  membership_id varchar(255) PRIMARY KEY,
  first_name varchar(255),
  last_name varchar(255),
  mobile_no numeric(8,0),
  email varchar(255),
  date_of_birth date,
  above_18 bool,
  added_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  added_by varchar(20),
  updated_by varchar(20)

);

-- transaction tables
CREATE TABLE IF NOT EXISTS sales.transaction (
  transaction_number serial PRIMARY KEY,
  item_number int,
  membership_id varchar(255),
  quantity float,
  added_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  added_by varchar(20),
  updated_by varchar(20)

);

ALTER TABLE sales.transaction ADD FOREIGN KEY (item_number) REFERENCES sales.item_master (item_number);
ALTER TABLE sales.transaction ADD FOREIGN KEY (membership_id) REFERENCES sales.member_master (membership_id);

CREATE TABLE IF NOT EXISTS sales.purchase_order (
  purchase_number int,
  transaction_number int,
  payment_cd int,
  added_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  added_by varchar(20),
  updated_by varchar(20),
  PRIMARY KEY (purchase_number , transaction_number)

);

ALTER TABLE sales.purchase_order ADD FOREIGN KEY (transaction_number) REFERENCES sales.transaction (transaction_number);
