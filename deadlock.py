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

#This code illustrates deadlock. While cursor1 tries to modify "Table" it is blocked for cursor2. However, while cursor2 tries to modify "Mirror" it is blocked for cursor1. 
# The point is that they are both trying access resources that are already blocked by them 
connection1 = create_connection()
connection2 = create_connection()
cursor1 = connection1.cursor()
cursor2 = connection2.cursor()
connection1.start_transaction(isolation_level='READ UNCOMMITTED')
cursor1.execute("UPDATE shop_list SET price = 1 WHERE product = 'Table'")
cursor1.execute("UPDATE shop_list SET price = 1 WHERE product = 'Mirror'")

cursor1.execute("SELECT price FROM shop_list WHERE product = 'Table'")
print("Cursor1:"+str(cursor1.fetchone()[0]))
cursor1.execute("SELECT price FROM shop_list WHERE product = 'Mirror'")
print("Cursor1:"+str(cursor1.fetchone()[0]))

#second transaction
connection2.start_transaction(isolation_level='READ UNCOMMITTED')
cursor2.execute("UPDATE shop_list SET price = 1 WHERE product = 'Mirror'")
cursor2.execute("UPDATE shop_list SET price = 1 WHERE product = 'Table'")

cursor2.execute("SELECT price FROM shop_list WHERE product = 'Table'")
print("Cursor2:"+str(cursor2.fetchone()[0]))
cursor2.execute("SELECT price FROM shop_list WHERE product = 'Mirror'")
print("Cursor2:"+str(cursor2.fetchone()[0]))
#second transaction

connection2.rollback()

cursor1.close()
cursor2.close()
connection1.close()
connection2.close()