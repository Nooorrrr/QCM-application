import tkinter as tk
import customtkinter as ctk
import mysql.connector  # Remplace pymysql
from mysql.connector import Error
from tkinter import messagebox

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pswd",#diro password ta3kom hna, bon genrallemnt faregh, mais bon
            database="qcm_test"
        )
        return connection
    except Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None