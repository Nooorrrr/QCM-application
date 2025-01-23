import mysql.connector #ida mamchatch diro (pip install mysql-connector-python)
from db import connect_to_db
from datetime import datetime

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
    """
    Permet à l'utilisateur de répondre aux questions du QCM.
    Évalue chaque réponse immédiatement après la saisie.
    """
    score = 0 
    total_questions = len(questions)
    feedback = []
    time = datetime.now()
    
    print("\nBienvenue dans la session de réponses au QCM. Répondez aux questions ci-dessous :\n")
    
    for idx_q, (question, reponses) in enumerate(questions.items(), 1):
        print(f"Question {idx_q}: {question}")
        for idx_r, (reponse, _) in enumerate(reponses, 1):
            print(f"  {idx_r}) {reponse}")
        
        while True:
            try:
                choix = int(input("Entrez le numéro de votre réponse : ").strip())
                if 1 <= choix <= len(reponses):
                    user_choice_index = choix - 1
                    selected_reponse = reponses[user_choice_index]
                    if selected_reponse[1]:
                        score += 1
                        feedback.append((question, True, selected_reponse[0]))
                        print(f"Correct!\n")
                    else:
                        correct_answer = next(rep[0] for rep in reponses if rep[1])
                        feedback.append((question, False, correct_answer))
                        print(f"Incorrect.")
                        print(f"La bonne réponse : {correct_answer}\n")
                        
                    break
                else:
                    print("Choix invalide. Veuillez sélectionner une option valide.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un numéro.")
    
    print("\n--- Résultats ---")
    print(f"Score total : {score}/{total_questions}")

    return {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "score": score,
        "total_questions": total_questions,
        "feedback": feedback,
    }
