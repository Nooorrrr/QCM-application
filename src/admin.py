import hashlib
import mysql.connector
from db import get_user_id  # Assurez-vous d'importer la fonction pour récupérer l'ID de l'utilisateur

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pswd",  # Utilisez le mot de passe correct pour la connexion
        database="qcm_test"
    )

###################################################

def new_QCM(user_id, password):
    print(f"le PASSWORD est {password}")
    print(f"le id est {user_id}")

    nom = input("Nom du QCM : ")


    # Liste des catégories possibles
    categories = ['THI', 'BI', 'COMPILE', 'AP', 'GL', 'RO', 'CRYPTO', 'WEB']

    # Choix de la catégorie
    while True:
        print("Choisissez une catégorie parmi les suivantes :")
        for idx, cat in enumerate(categories, 1):
            print(f"{idx}: {cat}")
        choix = input("Votre choix (entrez le numéro ou le nom de la catégorie) : ").strip()

        # Vérifiez si l'entrée est valide
        if choix.isdigit() and 1 <= int(choix) <= len(categories):
            categorie = categories[int(choix) - 1]
            break
        elif choix.upper() in categories:
            categorie = choix.upper()
            break
        else:
            print("Catégorie invalide. Veuillez réessayer.")


    questions = {}
    print("Appuyez sur '!' pour terminer le QCM.\n")

    while True:
        ajouter_question(questions, len(questions) + 1)
        continuer = input("Ajouter une autre question ? (oui/non) : ").strip().lower()
        if continuer != 'oui':
            if len(questions) + 1 > 1:
                break
            else:
                print("Le QCM doit contenir au moins 1 question.")

    print("QCM créé avec succès.")
    while True:
        print(f"Nom du QCM : {nom}")
        print(f"Catégorie : {categorie}")
        print("Questions et réponses :")
        for idx_q, (q, reps) in enumerate(questions.items(), 1):
            print(f"{idx_q}. {q}")
            for idx_r, (rep, etat) in enumerate(reps, 1):
                etat_str = "correcte" if etat else "incorrecte"
                print(f"          {idx_r}. {rep} ({etat_str})")
        print("Confirmer la création du formulaire : 1")
        print("Apporter des modifications : 2")
        print("Annuler le QCM : 3")
        choix = int(input("Votre choix : "))
        if choix == 1:
            conn = connect_to_db()
            cursor = conn.cursor()
            try:
                # Insertion du QCM avec l'ID du professeur connecté
                cursor.execute("INSERT INTO qcm (nomqcm, categorie, idprof) VALUES (%s, %s, %s)", (nom, categorie, user_id))
                qcm_id = cursor.lastrowid
                for question, reponses in questions.items():
                    cursor.execute("INSERT INTO qst (idqcm, enonce) VALUES (%s, %s)", (qcm_id, question))
                    qst_id = cursor.lastrowid
                    for reponse, etat in reponses:
                        cursor.execute("INSERT INTO answer (idqst, enonce, statut) VALUES (%s, %s, %s)", (qst_id, reponse, etat))
                conn.commit()
                print("QCM ajouté à la base de données avec succès.")
            except mysql.connector.Error as err:
                print(f"Erreur : {err}")
            finally:
                cursor.close()
                conn.close()
            break
        elif choix == 2:
            nom = Modifier_Qcm(nom, questions)
        elif choix == 3:
            print("QCM annulé avec succès.")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")
############################################################
def voir_qcms(user_id):
    conn = connect_to_db()
    if conn is None:
        print("Erreur de connexion à la base de données.")
        return
    cursor = conn.cursor()

    # Récupérer l'ID du professeur connecté
    prof_id = user_id  # Assurez-vous que user_id est l'ID correct du professeur
    print(f"Affichage des QCM du professeur ID : {prof_id}")

    # Sélectionner uniquement les QCMs du professeur connecté
    cursor.execute("""
        SELECT qcm.idqcm, qcm.nomqcm, COUNT(qcm_user.iduser) AS nb_prsn
        FROM qcm
        LEFT JOIN qcm_user ON qcm.idqcm = qcm_user.idqcm
        WHERE qcm.idprof = %s
        GROUP BY qcm.idqcm
    """, (prof_id,))

    # Afficher les résultats dans un format de tableau
    print(f"{'ID QCM':<10} {'Nom du QCM':<30} {'Nombre de personnes ayant répondu':<30}")
    print("-" * 70)

    # Afficher chaque QCM et le nombre de personnes ayant répondu
    for (idqcm, nomqcm, nb_prsn) in cursor.fetchall():
        print(f"{idqcm:<10} {nomqcm:<30} {nb_prsn:<30}")

    # Fermer la connexion
    cursor.close()
    conn.close()

#########################################################

def ajouter_question(questions, numero_question):
    question = input(f"Q{numero_question}: ")
    reponses = []
    print(f"Appuyez sur '!' pour terminer l'ajout des réponses pour Q{numero_question}.")
    corr = False  # en moins une correct
    faux = False  # en moins une fausse
    while True:
        reponse = input(f"Réponse {len(reponses) + 1}: ")
        if reponse == '!':
            if len(reponses) >= 2 and corr and faux:
                break
            else:
                print("La question doit avoir au moins 2 réponses. une correct et une fausse")
        else:
            while True:
                etat = input("Est-ce une bonne réponse ? (oui/non) : ").strip().lower()
                if etat == 'oui':
                    etat = True
                    corr = True
                    break
                elif etat == 'non':
                    etat = False
                    faux = True
                    break
                else:
                    print("Veuillez entrer 'oui' ou 'non'.")
            reponses.append((reponse, etat))

    questions[question] = reponses
    print("Question ajoutée avec succès !")

################################################################################

def Modifier_Qcm(nom, questions):
    while True:
        print("\n1: Modifier le nom")
        print("2: Modifier une question ou une réponse")
        print("3: Ajouter une question ")
        print("4: Arrêter les modifications")

        choix = input("Votre choix : ").strip()
        if choix == '1':
            nom = input("Nouveau nom du QCM : ")
            print("Nom modifié avec succès.")
        elif choix == '2':
            for idx, question in enumerate(questions.keys(), 1):
                print(f"{idx}. {question}")
            try:
                num_question = int(input("Numéro de la question à modifier : "))
                question_cible = list(questions.keys())[num_question - 1]

                print("1: Modifier la question")
                print("2: Modifier une réponse")
                choix_modif = input("Votre choix : ").strip()

                if choix_modif == '1':
                    nouvelle_question = input(f"Texte de la nouvelle question : ")
                    questions[nouvelle_question] = questions.pop(question_cible)
                elif choix_modif == '2':
                    for idx, (rep, etat) in enumerate(questions[question_cible], 1):
                        etat_str = "correcte" if etat else "incorrecte"
                        print(f"{idx}. {rep} ({etat_str})")

                    num_reponse = int(input("Numéro de la réponse à modifier : "))
                    reponse_cible = questions[question_cible][num_reponse - 1]

                    print("1: Modifier le texte")
                    print("2: Modifier l'état")
                    choix_reponse = input("Votre choix : ").strip()

                    if choix_reponse == '1':
                        nouveau_texte = input("Nouveau texte de la réponse : ")
                        questions[question_cible][num_reponse - 1] = (nouveau_texte, reponse_cible[1])
                    elif choix_reponse == '2':
                        nouvel_etat = input("État de la réponse (oui/non) : ").strip().lower()
                        questions[question_cible][num_reponse - 1] = (reponse_cible[0], nouvel_etat == 'oui')
                    else:
                        print("Choix invalide.")
                else:
                    print("Choix invalide.")
            except (ValueError, IndexError):
                print("Numéro invalide.")
        elif choix == '3':
            ajouter_question(questions, len(questions) + 1)
        elif choix == '4':
            print("Modifications terminées.")
            break
        else:
            print("Choix invalide.")
    return nom
################################################################################

def admin(user_id,password):
    while True:
        print(f"le PASSWORD est {password}")
        print(f"le id est {user_id}")

        print("1: Voir tous mes QCM")
        print("2: Créer un nouveau QCM")
        choix = input("Votre choix : ").strip()
        if choix == '1':
            voir_qcms(user_id)
        elif choix == '2':
            new_QCM(user_id,password)
        else:
            print("Choix invalide.")

#admin()