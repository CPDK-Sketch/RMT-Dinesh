import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)

cursor = conn.cursor()

# Create DB if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS returns_management")
print("✅ Database 'returns_management' ensured.")

cursor.close()
conn.close()
