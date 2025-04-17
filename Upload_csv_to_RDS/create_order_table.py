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
    cursor.execute("DROP TABLE IF EXISTS orders;")

    # Create table
    create_table_sql = '''
    CREATE TABLE orders (
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
        address TEXT
    );
    '''
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Table 'orders' created successfully.")

except mysql.connector.Error as err:
    print("❌ Error:", err)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("🔒 Connection closed.")
