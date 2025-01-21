import mysql.connector #ida mamchatch diro (pip install mysql-connector-python)
from db import connect_to_db

def fetch_categories():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT categorie FROM qcm")
    categories = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return categories

def fetch_qcm(category):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT idqcm, nomqcm FROM qcm WHERE categorie = %s", (category,))
    qcm = {row[1]: row[0] for row in cursor.fetchall()}
    cursor.close()
    conn.close()
    return qcm

def repondre_questions(questions):
        reponses_utilisateur = []
        print("\nBienvenue dans la session de réponses au QCM. Répondez aux questions ci-dessous :\n")
        
        for idx_q, (question, reponses) in enumerate(questions.items(), 1):
            print(f"Question {idx_q}: {question}")
            for idx_r, reponse in enumerate(reponses, 1):
                print(f"  {idx_r}) {reponse}")
            
            while True:
                try:
                    choix = int(input("Entrez le numéro de votre réponse : ").strip())
                    if 1 <= choix <= len(reponses):
                        reponses_utilisateur.append(choix)
                        break
                    else:
                        print("Choix invalide. Veuillez sélectionner une option valide.")
                except ValueError:
                    print("Entrée invalide. Veuillez entrer un numéro.")
        
        print("\nMerci d'avoir répondu au QCM.")
        return reponses_utilisateur
