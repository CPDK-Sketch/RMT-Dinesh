import mysql.connector

# Connect to RDS
conn = mysql.connector.connect(
    host = "returnsdb.cx46s84o832r.eu-west-2.rds.amazonaws.com",  
    username = "admin",   # r DB username
    password = "Huboo1234567890"   #  DB password
)

cursor = conn.cursor()

# Show all databases
print("\n📂 Existing Databases:")
cursor.execute("SHOW DATABASES")
for db in cursor:
    print(" -", db[0])

# Optional: check tables in a specific database
cursor.execute("USE returns_management")
cursor.execute("SHOW TABLES")
print("\n📋 Tables in 'returns_management':")
for table in cursor:
    print(" -", table[0])

cursor.close()
conn.close()
