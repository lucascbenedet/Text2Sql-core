import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode
import pandas as pd


class DatabaseExecutor:
    def __init__(self):
        try:
            load_dotenv()
            _host = os.getenv("HOST")
            _database = os.getenv("DATABASE")
            _user = os.getenv("USER")
            _password = os.getenv("PASSWORD")
            self.conn = mysql.connector.connect(
                host=_host, database=_database, user=_user, password=_password
            )
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("Connection successfully!!!")

    def verify_database(self):
        try:
            if self.conn.is_connected():
                db_info = self.conn.get_server_info()
                print("Connected to the MySQL version ", db_info)
                cursor = self.conn.cursor()
                cursor.execute("select database();")
                result = cursor.fetchone()
                print("Connected to the database ", result)
                cursor.close()
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("Operation executed successfully! !!!")

    def run_query(self, query: str) -> pd.DataFrame:
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(rows, columns=columns)
