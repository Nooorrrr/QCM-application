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
        score = 0 
        total_questions = len(questions)
        feedback = []
        time = datetime.now()
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
                            print(f"\033[92mCorrect!\033[0m\n") 
                        else:
                            correct_answer = next(rep[0] for rep in reponses if rep[1])
                            feedback.append((question, False, correct_answer))
                            print(f"\033[91mIncorrect.\033[0m")  
                            print(f"La bonne réponse : {correct_answer}\n")
                            
                        break
                    else:
                        print("Choix invalide. Veuillez sélectionner une option valide.")
                except ValueError:
                    print("Entrée invalide. Veuillez entrer un numéro.")
        
        print("\n---------------------- Résultats ----------------------")
        print(f"Score total : {score}/{total_questions}")
        print(f"Temps : {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("Feedback :")
        for idx_q, (question, is_correct, answer) in enumerate(feedback, 1):
            print(f"{idx_q}. {question}")
            if is_correct:
                print(f"   \033[92mCorrect!\033[0m")
            else:
                print(f"   \033[91mIncorrect.\033[0m")
                print(f"   La bonne réponse : {answer}")
        