import mysql.connector
import pandas as pd

# AWS RDS Connection Parameters
rds_host = "returns-db.c5oyyuuuetdv.eu-west-1.rds.amazonaws.com"  
username = "admin"   # r DB username
password = "Huboo1234567890"   #  DB password
#database = "returns_db"       # database name

# Path to your CSV file in GitHub Codespaces
csv_file_path = "/workspaces/RMT-Dinesh/Tables/Orders-table.csv"  # Example: "data/mydata.csv"

# Connect to the RDS instance
conn = mysql.connector.connect(
    host=rds_host,
    user=username,
    password=password,
    #database=database
)

cursor = conn.cursor()
cursor.execute("USE returns_management")


# Read the CSV file using pandas
data = pd.read_csv(csv_file_path)

# Get the column names from the DataFrame
columns = data.columns

# Prepare the INSERT query
#insert_query = f"INSERT INTO orders ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
insert_query = """
INSERT INTO orders (
    `Order_Date`, `First_Name`, `Last_Name`, `Shipment_ID`, `Client_Order_Id`,
    `PI`, `Order_Quantity`,  `Hub`, `Client_ID`,
    `Shipping_Method`, `Address`
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Insert data into the RDS database
for row in data.itertuples(index=False, name=None):
    cursor.execute(insert_query, row)

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Data uploaded successfully!")
