import pymysql
from pymysql.cursors import DictCursor
from tkinter import messagebox

def connect_to_database():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='qcm_py',
            cursorclass=DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
        return None
