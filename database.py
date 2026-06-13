import os
from mysql.connector import (connection)
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

load_dotenv()
DB_HOST=os.getenv("DB_HOST")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_DATABASE=os.getenv("DB_DATABASE")

try:
 cnx=connection.MySQLConnection(user=DB_USER,password=DB_PASSWORD,host=DB_HOST,database=DB_DATABASE)

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

