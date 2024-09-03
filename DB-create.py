import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345@Soni"
)

mycursor = mydb.cursor()

# Create database
mycursor.execute("CREATE DATABASE IF NOT EXISTS symptoms")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345@Soni",
  database="symptoms"
)

mycursor = mydb.cursor()

# Create table
mycursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    dob DATE NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")

mycursor.close()
mydb.close()
