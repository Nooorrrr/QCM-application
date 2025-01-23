import hashlib
import mysql.connector

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pswd",  
        database="qcm_test"
    )

def get_user_id(username, password):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Hacher le mot de passe saisi par l'utilisateur
        hashed_password = hash_password(password)

        # Vérifier si l'utilisateur existe avec le mot de passe haché
        cursor.execute("SELECT user_id FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        user = cursor.fetchone()

        if user:
            return user[0]  # Récupérer l'ID de l'utilisateur
        else:
            print("Identifiants invalides.")
            return None
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération de l'utilisateur : {err}")
        return None
    finally:
        cursor.close()
        conn.close()
