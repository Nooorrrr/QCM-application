import mysql.connector #ida mamchatch diro (pip install mysql-connector-python)
from datetime import datetime
import hashlib
import pwinput # meme hadi make sure to install it
from db import connect_to_db


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# def validate_password(password):
#     if len(password) < 8:
#         return "Le mot de passe doit contenir au moins 8 caractères."
#     if not any(char.isdigit() for char in password):
#         return "Le mot de passe doit contenir au moins un chiffre."
#     if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/`~" for char in password):
#         return "Le mot de passe doit contenir au moins un caractère spécial."
#     return None  

def ppassword():
    while True:
        password = pwinput.pwinput("Entrez votre mot de passe: ")  
        pass2 = pwinput.pwinput("Confirmez votre mot de passe: ")
        if password != pass2:
            print("Les mots de passe est incorrect, try again.")
        else:
            break
    return password

def validate_username(username):
    #checl if username already exists
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return "Ce nom d'utilisateur est déjà pris."
    return None  

def login():
    username = input("Entrez votre nom d'utilisateur: ")
    password = pwinput.pwinput("Entrez votre mot de passe: ")  # Affiche des astérisques

    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result and hash_password(password) == result[0]:
        print("Connexion réussie !")
    else:
        print("Nom d'utilisateur ou mot de passe incorrect.")

    cursor.close()
    conn.close()

def signup():
    while True:
        username = input("Entrez un nom d'utilisateur: ")
        error = validate_username(username)
        if error:
            print(error)
            continue
        

        password = ppassword()

        name = input("Entrez votre nom: ")
        email = input("Entrez votre adresse email: ")

        conn = connect_to_db()
        cursor = conn.cursor()

        hashed_password = hash_password(password)
        query = """
            INSERT INTO users (username, password, name, email, role) 
            VALUES (%s, %s, %s, %s, 'user') 
        """   #role par default 7a ndiroh user
        try:
            cursor.execute(query, (username, hashed_password, name, email))
            conn.commit()
            print("Compte créé avec succès !")
            break
        except mysql.connector.Error as err:
            print(f"Erreur : {err}")
        finally:
            cursor.close()
            conn.close()

