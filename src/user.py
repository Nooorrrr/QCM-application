import mysql.connector #ida mamchatch diro (pip install mysql-connector-python)
from datetime import datetime
import hashlib
import pwinput # meme hadi make sure to install it
from db import connect_to_db
from admin import admin
from qcm import fetch_categories, fetch_qcm, repondre_questions


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
################################################################################
def ppassword():
    while True:
        password = pwinput.pwinput("Entrez votre mot de passe: ")  
        pass2 = pwinput.pwinput("Confirmez votre mot de passe: ")
        if password != pass2:
            print("Les mots de passe est incorrect, try again.")
        else:
            break
    return password
################################################################################
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
################################################################################
def login():
    username = input("Entrez votre nom d'utilisateur: ")
    password = pwinput.pwinput("Entrez votre mot de passe: ")  # Affiche des astérisques

    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT user_id, password, role FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result and hash_password(password) == result[1]:
        print("Connexion réussie !")
        user_id = result[0]  # Correctly fetch the user_id
        password=result[1]
        if result[2] == 'prof':  # Check if the role is 'prof'
            print("Bienvenue Professeur")
            admin(user_id,password)  # Pass the user_id to admin
        else:
            print(f"Bienvenue {username}")
            #user()
    else:
        print("Nom d'utilisateur ou mot de passe incorrect.")

    cursor.close()
    conn.close()

################################################################################
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

def user_menu(user_id):
    while True:
        print("\n--- Menu Utilisateur ---")
        print("1. Répondre à un QCM")
        print("2. Voir l'historique des QCM")
        print("3. Déconnexion")
        choice = input("Choisissez une option: ")

        if choice == '1':
            categories = fetch_categories()
            print("\nCatégories disponibles:")
            for idx, category in enumerate(categories, 1):
                print(f"{idx}. {category}")
            cat_choice = int(input("Choisissez une catégorie: ")) - 1
            selected_category = categories[cat_choice]

            qcm_list = fetch_qcm(selected_category)
            print("\nQCM disponibles:")
            for idx, (qcm_name, qcm_id) in enumerate(qcm_list.items(), 1):
                print(f"{idx}. {qcm_name}")
            qcm_choice = int(input("Choisissez un QCM: ")) - 1
            selected_qcm_id = list(qcm_list.values())[qcm_choice]

            # Fetch questions and answers for the selected QCM
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT enonce FROM qst WHERE idqcm = %s", (selected_qcm_id,))
            questions = {row[0]: [] for row in cursor.fetchall()}
            for question in questions:
                cursor.execute("SELECT enonce, statut FROM answer WHERE idqst = (SELECT idqst FROM qst WHERE enonce = %s)", (question,))
                questions[question] = cursor.fetchall()
            cursor.close()
            conn.close()

            results = repondre_questions(questions)
            save_quiz_results(user_id, selected_qcm_id, results["score"], results["total_questions"])

        elif choice == '2':
            history = fetch_user_history(user_id)
            print("\n--- Historique des QCM ---")
            for qcm_name, note, timestamp in history:
                print(f"QCM: {qcm_name}, Note: {note}%, Date: {timestamp}")

        elif choice == '3':
            print("Déconnexion réussie.")
            break

        else:
            print("Choix invalide. Veuillez réessayer.")

def fetch_user_history(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
        SELECT qcm.nomqcm, qcm_user.note, qcm_user.timestamp 
        FROM qcm_user 
        JOIN qcm ON qcm_user.idqcm = qcm.idqcm 
        WHERE qcm_user.iduser = %s
    """
    cursor.execute(query, (user_id,))
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return history

def save_quiz_results(user_id, qcm_id, score, total_questions):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Check if the entry already exists
    query_check = "SELECT * FROM qcm_user WHERE iduser = %s AND idqcm = %s"
    cursor.execute(query_check, (user_id, qcm_id))
    result = cursor.fetchone()
    
    if result:
        print("Entry already exists. Updating the existing record.")
        query_update = """
            UPDATE qcm_user 
            SET note = %s, timestamp = CURRENT_TIMESTAMP
            WHERE iduser = %s AND idqcm = %s
        """
        cursor.execute(query_update, ((score / total_questions) * 100, user_id, qcm_id))
    else:
        query_insert = """
            INSERT INTO qcm_user (iduser, idqcm, note, timestamp) 
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        """
        cursor.execute(query_insert, (user_id, qcm_id, (score / total_questions) * 100))
    
    conn.commit()
    cursor.close()
    conn.close()
