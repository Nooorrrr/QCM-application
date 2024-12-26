import mysql.connector
from datetime import datetime
import hashlib

# Connexion à la base de données
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="pswd",  
        database="qcm_test"  
    )

# Fonction pour hacher le mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fonction pour valider le mot de passe
def validate_password(password):
    if len(password) < 8:
        return "Le mot de passe doit contenir au moins 8 caractères."
    if not any(char.isupper() for char in password):
        return "Le mot de passe doit contenir au moins une lettre majuscule."
    if not any(char.isdigit() for char in password):
        return "Le mot de passe doit contenir au moins un chiffre."
    if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/`~" for char in password):
        return "Le mot de passe doit contenir au moins un caractère spécial."
    return None  # Pas d'erreur

# Fonction pour valider le nom d'utilisateur
def validate_username(username):
    if len(username) < 4:
        return "Le nom d'utilisateur doit contenir au moins 4 caractères."
    return None  # Pas d'erreur



def login():
    username = input("Entrez votre nom d'utilisateur: ")
    password = input("Entrez votre mot de passe: ")
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

        password = input("Entrez un mot de passe: ")
        error = validate_password(password)
        if error:
            print(error)
            continue

        name = input("Entrez votre nom: ")
        email = input("Entrez votre adresse email: ")

        conn = connect_to_db()
        cursor = conn.cursor()

        hashed_password = hash_password(password)
        query = """
            INSERT INTO users (username, password, name, email, role) 
            VALUES (%s, %s, %s, %s, 'user')
        """
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

# Menu principal
def main():
    print("1. Connexion")
    print("2. Inscription")
    choice = input("Choisissez une option (1 ou 2): ")

    if choice == '1':
        login()
    elif choice == '2':
        signup()
    else:
        print("Choix invalide.")

if __name__ == "__main__":
    main()