import mysql.connector
from mysql.connector import Error
import consts

HOST = '127.0.0.1'
USER = consts.USER
PASSWORD = consts.PASSWORD
DATABASE = 'demo'


def create_connection():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

#Dirty read is caused by two "Read uncommited" isalation type transactions. Cursor1 tries to read info, while it is modified by cursor2
connection1 = create_connection()
connection2 = create_connection()
cursor1 = connection1.cursor()
cursor2 = connection2.cursor()
connection1.start_transaction(isolation_level='READ UNCOMMITTED')
cursor1.execute("SELECT price FROM shop_list WHERE product = 'Table'")
print(cursor1.fetchone()[0])

#second transaction
connection2.start_transaction(isolation_level='READ UNCOMMITTED')
cursor2.execute("UPDATE shop_list SET price = 1 WHERE product = 'Table'")
#second transaction

cursor1.execute("SELECT price FROM shop_list WHERE product = 'Table'")
print(cursor1.fetchone()[0])
connection2.rollback()

cursor1.close()
cursor2.close()
connection1.close()
connection2.close()