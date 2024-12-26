def ajouter_question(questions, numero_question):
    """
    Ajoute une nouvelle question avec ses réponses.
    """
    question = input(f"Q{numero_question}: ")
    reponses = []
    print(f"Appuyez sur '!' pour terminer l'ajout des réponses pour Q{numero_question}.")
    corr=False #en moins une correct
    faux=False #en moins une fausse
    while True:
        reponse = input(f"Réponse {len(reponses) + 1}: ")
        if reponse == '!':
            if len(reponses) >= 2 and corr==True and faux==True:  # Au moins 2 réponses nécessaires et en moins 1 correct et une fauss
                break
            else:
                print("La question doit avoir au moins 2 réponses. une correct et une fausse")
        else:
            while True:
                etat = input("Est-ce une bonne réponse ? (oui/non) : ").strip().lower()
                if etat=='oui':
                    etat = True  # Convertit en booléen
                    corr=True
                    break
                elif etat=='non':
                    etat = False  # Convertit en booléen
                    faux=True
                    break
                else:
                    print("Veuillez entrer 'oui' ou 'non'.")
            reponses.append((reponse, etat))
    
    questions[question] = reponses
    print("Question ajoutée avec succès !")


def Modifier_Qcm(nom, questions):
    """
    Modifie le nom, les questions ou les réponses d'un QCM.
    """
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


def new_QCM():
    nom = input("Nom du QCM : ")
    questions = {}
    print("Appuyez sur '!' pour terminer le QCM.\n")
    
    while True:
        ajouter_question(questions, len(questions) + 1)
        continuer = input("Ajouter une autre question ? (oui/non) : ").strip().lower()
        if continuer != 'oui' :
            if len(questions)+1>1:
                break
            else:
                print("le qcm doit contenir en moins 1 question")
    
    print("QCM créé avec succès.")
    while True:
        print(f"Nom du QCM : {nom}")
        print("Questions et réponses :")
        for idx_q, (q, reps) in enumerate(questions.items(), 1):  # Commence l'énumération des questions à 1
            print(f"{idx_q}. {q}")  # Affiche le numéro de la question et son texte
            for idx_r, (rep, etat) in enumerate(reps, 1):  # Commence l'énumération des réponses à 1
                etat_str = "correcte" if etat else "incorrecte"
                print(f"          {idx_r}. {rep} ({etat_str})")  # Affiche les réponses avec leur état
        print("Confirmer la création du formulaire : 1")
        print("Apporter des modifications : 2")
        print("annuler le QCM : 3")
        choix = int(input("Votre choix : "))
        if choix == 1:
            #ajout a la bdd
            print("Fonctionnalité non encore implémentée.")
            break
        elif choix == 2:
            nom = Modifier_Qcm(nom, questions) 
        elif choix==3:
            print("QCM annulle avec succee")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")


def admin():
    while True:
        print("1: Voir tous mes QCM")
        print("2: Créer un nouveau QCM")
        choix = input("Votre choix : ").strip()
        if choix == '1':
            print("Fonctionnalité non encore implémentée.")
        elif choix == '2':
            new_QCM()
        else:
            print("Choix invalide.")


admin()
