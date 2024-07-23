import mysql.connector
from dotenv import load_dotenv
import time
import os


class Database():

    def __init__(self):
        self.connect_to_db()



    def connect_to_db(self):
        

        load_dotenv()
        ENV_DATABASE_USER = os.getenv('DATABASE_USER')
        ENV_DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
        ENV_DATABASE_HOST = os.getenv('DATABASE_HOST')
        ENV_DATABASE_NAME = os.getenv('DATABASE_NAME')
        ENV_DATABASE_PORT = os.getenv('DATABASE_PORT')

        self.connection = mysql.connector.connect(
            user=ENV_DATABASE_USER,
            password=ENV_DATABASE_PASSWORD,
            port=ENV_DATABASE_PORT,
            host=ENV_DATABASE_HOST,
            database=ENV_DATABASE_NAME
        )

        self.cursor = self.connection.cursor()
        print(f'Database : connect_to_db ' + "Connection is done")
        # self.cursor.execute(f"""USE {ENV_DATABASE_NAME}""")
        print('Database --> ' + f"{ENV_DATABASE_NAME} Database is in use")


    def select_query(self, query):

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        
        return result



    def insert_db(self, query):
        self.cursor.execute(query)

        self.connection.commit()
        print('Database : insert_db done')

        



    def update_db(self, table, parameters):

        pass

