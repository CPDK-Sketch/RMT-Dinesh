import mysql.connector
import pandas as pd

# AWS RDS Connection Parameters
rds_host = "returnsdb.cx46s84o832r.eu-west-2.rds.amazonaws.com"  
username = "admin"   # r DB username
password = "Huboo123456789"   #  DB password
database = "returns_table"       # database name

# Path to your CSV file in GitHub Codespaces
csv_file_path = "data/your_file.csv"  # Example: "data/mydata.csv"

# Connect to the RDS instance
conn = mysql.connector.connect(
    host=rds_host,
    user=username,
    password=password,
    database=database
)

cursor = conn.cursor()

# Read the CSV file using pandas
data = pd.read_csv(csv_file_path)

# Get the column names from the DataFrame
columns = data.columns

# Prepare the INSERT query
insert_query = f"INSERT INTO your_table_name ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

# Insert data into the RDS database
for row in data.itertuples(index=False, name=None):
    cursor.execute(insert_query, row)

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Data uploaded successfully!")
