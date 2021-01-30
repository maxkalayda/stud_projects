import sqlite3 as db
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = db.connect(path)
    except Error as e:
        print(e)
    return (connection)