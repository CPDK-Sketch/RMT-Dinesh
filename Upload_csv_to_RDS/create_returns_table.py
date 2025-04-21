import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read credentials from .env
db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT", 3306))
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

try:
    # Connect to MySQL RDS
    conn = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_pass,
        database=db_name
    )
    cursor = conn.cursor()
    print("✅ Connected to MySQL RDS")

    cursor.execute("USE returns_management")
    # Drop table if exists
    cursor.execute("DROP TABLE IF EXISTS returns;")

    # Create table
    create_table_sql = '''
    CREATE TABLE returns (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_date DATE,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        shipment_id VARCHAR(50),
        client_order_id VARCHAR(50),
        pi VARCHAR(50),
        order_quantity INT,
        hub VARCHAR(100),
        client_id VARCHAR(50),
        shipping_method VARCHAR(100),
        address TEXT,
        r_shipping_method VARCHAR(100),
        r_tracking_info VARCHAR(100),
        r_date_returned DATE,
        r_items_returned INT,
        r_retuned_hub BOOLEAN,
        r_return_reason VARCHAR(100),
        r_condition VARCHAR(100),
        r_comments VARCHAR(100),
        r_processed_date DATE,
        h_booked_back BOOLEAN,
        h_condition VARCHAR(100),
        h_comments VARCHAR(100),
        h_processed_date DATE,
        b_billed BOOLEAN,
        b_billing_Value FLOAT



    );
    '''
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Table 'returns' created successfully.")

except mysql.connector.Error as err:
    print("❌ Error:", err)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("🔒 Connection closed.")
