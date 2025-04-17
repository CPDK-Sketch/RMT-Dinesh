import mysql.connector

# Connect to RDS
conn = mysql.connector.connect(
    host = "returnsdb.cx46s84o832r.eu-west-2.rds.amazonaws.com",  
    username = "admin",   # r DB username
    password = "Huboo123456789"   #  DB password
)

cursor = conn.cursor()

# Show all databases
print("\n📂 Existing Databases:")
cursor.execute("SHOW DATABASES")
for db in cursor:
    print(" -", db[0])

# Optional: check tables in a specific database

cursor.execute("SHOW TABLES")
print("\n📋 Tables in 'returns_tables':")
for table in cursor:
    print(" -", table[0])

cursor.close()
conn.close()
