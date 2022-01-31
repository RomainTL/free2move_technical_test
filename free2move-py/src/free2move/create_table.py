"""Module containing methods used to create and drop table"""

def get_tables():
    """List of all tables with their name and sql_statement to create it in a PostgreSQL database server"""

    tables = [
        {
            "table": "SELLERS",
            "sql_statement":
            """
                CREATE TABLE SELLERS(
                    seller_id CHAR(32) NOT NULL PRIMARY KEY
                )
            """
        },
        {
            "table": "CUSTOMERS",
            "sql_statement":
            """
                CREATE TABLE CUSTOMERS(
                    customer_id CHAR(32) NOT NULL PRIMARY KEY,
                    customer_unique_id CHAR(32) NOT NULL,
                    customer_zip_code_prefix CHAR(5) NOT NULL,
                    customer_city VARCHAR(64) NOT NULL,
                    customer_state CHAR(2) NOT NULL
                )
            """
        },
        {
            "table": "PRODUCTS",
            "sql_statement":
            """
                CREATE TABLE PRODUCTS(
                    product_id CHAR(32) NOT NULL PRIMARY KEY,
                    product_category_name VARCHAR(100),
                    product_name_lenght FLOAT,
                    product_description_lenght FLOAT,
                    product_photos_qty INT,
                    product_weight_g FLOAT NOT NULL,
                    product_length_cm FLOAT NOT NULL,
                    product_height_cm FLOAT NOT NULL,
                    product_width_cm FLOAT NOT NULL,
                    product_category_name_english VARCHAR(100)
                )
            """
        },
        {
            "table": "ORDERS",
            "sql_statement":
            """
                CREATE TABLE ORDERS(
                    order_id CHAR(32) NOT NULL PRIMARY KEY,
                    customer_id CHAR(32) NOT NULL,
                    order_status VARCHAR(32) NOT NULL,
                    order_purchase_timestamp TIMESTAMP NOT NULL,
                    order_approved_at TIMESTAMP,
                    order_delivered_carrier_date TIMESTAMP,
                    order_delivered_customer_date TIMESTAMP,
                    order_estimated_delivery_date TIMESTAMP NOT NULL,
                    CONSTRAINT fk_customer_id FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
                )
            """
        },
        {
            "table": "ITEMS",
            "sql_statement":
            """
                CREATE TABLE ITEMS(
                    order_id CHAR(32) NOT NULL,
                    order_item_id INT NOT NULL,
                    seller_id CHAR(32) NOT NULL,
                    product_id CHAR(32) NOT NULL,
                    shipping_limit_date TIMESTAMP NOT NULL,
                    price FLOAT NOT NULL,
                    freight_value FLOAT NOT NULL,
                    CONSTRAINT pk_items PRIMARY KEY (order_id, order_item_id),
                    CONSTRAINT fk_order_id FOREIGN KEY (order_id) REFERENCES orders (order_id),
                    CONSTRAINT fk_seller_id FOREIGN KEY (seller_id) REFERENCES sellers (seller_id),
                    CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES products (product_id)
                )
            """
        }
    ]

    return tables


def drop_table(cursor, table):
    print(f"\t{table}..")
    cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")


def create_table(cursor, table, sql_statement):
    print(f"\t{table}..")
    cursor.execute(sql_statement)
