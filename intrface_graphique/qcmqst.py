import customtkinter as ctk
from conn import connect_to_database
import pymysql.cursors

class QCMApp:
    def __init__(self, root, qcm_id):
        self.root = root
        self.qcm_id = qcm_id  # ID du QCM sélectionné (passé depuis main.py)
        self.root.title(f"QCM Interface - QCM {qcm_id}")
        self.root.geometry("800x600")

        # Conteneur principal
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Barre de navigation (sidebar)
        self.sidebar = ctk.CTkFrame(self.main_frame, width=150)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))

        self.qcms_btn = ctk.CTkButton(self.sidebar, text="QCMS", width=140)
        self.qcms_btn.pack(pady=10)

        self.history_btn = ctk.CTkButton(self.sidebar, text="My history", width=140)
        self.history_btn.pack(pady=10)

        # Contenu principal
        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.content_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Titre principal
        self.title_label = ctk.CTkLabel(self.content_frame, text=f"QCM {qcm_id}", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=(10, 20))

        # Détails des questions
        self.question_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        self.question_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Récupérer et afficher les informations du QCM (titre, catégorie et questions)
        self.qcm_info = self.fetch_qcm_info()
        self.display_qcm_info()

        # Bouton "Submit" en bas du contenu principal
        self.submit_btn = ctk.CTkButton(
            self.content_frame,
            text="Submit",
            width=150,
            command=self.calculate_score  # Appeler la méthode pour calculer et afficher le score
        )
        self.submit_btn.pack(pady=(20, 10))  # Espacement autour du bouton

    def fetch_qcm_info(self):
        """Récupérer toutes les informations du QCM depuis la base de données"""
        try:
            mydb = connect_to_database()
            cursor = mydb.cursor(pymysql.cursors.DictCursor)
            query = """
                SELECT qcm.nomqcm, qcm.categorie, qcm.idprof, qst.idqst, qst.enonce, 
                       answer.idanswer, answer.enonce AS answer_enonce, answer.statut
                FROM qcm
                JOIN qst ON qcm.idqcm = qst.idqcm
                LEFT JOIN answer ON qst.idqst = answer.idqst
                WHERE qcm.idqcm = %s
            """
            cursor.execute(query, (self.qcm_id,))
            results = cursor.fetchall()
            return results
        except Exception as e:
            print("Erreur lors de la récupération du QCM :", e)
            return []
        finally:
            if 'mydb' in locals() and mydb:
                mydb.close()

    def display_qcm_info(self):
        """Afficher les informations du QCM (titre, catégorie, questions et réponses)"""
        if self.qcm_info:
            # Afficher le titre et la catégorie du QCM
            qcm_title = self.qcm_info[0]['nomqcm']
            qcm_category = self.qcm_info[0]['categorie']
            self.title_label.configure(text=f"{qcm_title} - {qcm_category}")

            # Afficher les questions et réponses
            current_question_id = None
            question_frame = None

            for record in self.qcm_info:
                question_id = record['idqst']
                question_text = record['enonce']
                answer_id = record['idanswer']
                answer_text = record['answer_enonce']
                is_correct = record['statut']  # Le statut détermine si la réponse est correcte

                # Créer un nouveau cadre pour la question si nécessaire
                if question_id != current_question_id:
                    current_question_id = question_id
                    question_frame = ctk.CTkFrame(self.question_frame, corner_radius=10)
                    question_frame.pack(fill="both", padx=10, pady=(5, 10))

                    question_label = ctk.CTkLabel(question_frame, text=question_text, font=("Arial", 16, "bold"))
                    question_label.pack(anchor="w", pady=(10, 5))
                    print(f"Question ajoutée : {question_text}")  # Log pour vérifier

                # Afficher les réponses sous forme de cases à cocher
                if answer_id:
                    # Créer la case à cocher et ajouter des attributs personnalisés
                    answer_item = ctk.CTkCheckBox(question_frame, text=answer_text)
                    answer_item.is_correct = is_correct  # Stocker si la réponse est correcte
                    answer_item.pack(anchor="w", pady=5)
                    print(f"Réponse ajoutée : {answer_text} (Correct: {is_correct})")  # Log pour vérifier
        else:
            print("Aucune donnée à afficher.")  # Log si aucune donnée n'est disponible

    def calculate_score(self):
        """Calculer le score en fonction des réponses sélectionnées par l'utilisateur"""
        try:
            user_score = 0
            total_correct_answers = 0

            # Parcourir les réponses sélectionnées par l'utilisateur
            for question_frame in self.question_frame.winfo_children():
                for widget in question_frame.winfo_children():
                    if isinstance(widget, ctk.CTkCheckBox):
                        if widget.get() == 1:  # Si la case est cochée
                            if widget.is_correct == 1:  # Si la réponse est correcte
                                user_score += 1
                            total_correct_answers += widget.is_correct  # Compte total des bonnes réponses

            # Afficher le score à l'utilisateur
            self.show_score(user_score, total_correct_answers)

        except Exception as e:
            print("Erreur lors du calcul du score :", e)

    def show_score(self, user_score, total_correct_answers):
        """Afficher le score à l'utilisateur"""
        # Vérifier si une fenêtre de score est déjà ouverte
        if hasattr(self, 'score_window') and self.score_window.winfo_exists():
            self.score_window.lift()  # Amener la fenêtre existante au premier plan
            return

        # Créer une nouvelle fenêtre pour afficher le score
        self.score_window = ctk.CTkToplevel(self.root)
        self.score_window.title("Score")
        self.score_window.geometry("300x150")

        # Empêcher la fermeture automatique de la fenêtre
        self.score_window.grab_set()

        # Ajouter un message avec le score
        score_label = ctk.CTkLabel(
            self.score_window,
            text=f"Votre score est : {user_score}/{total_correct_answers}",
            font=("Arial", 18, "bold")
        )
        score_label.pack(pady=50)

        # Ajouter un bouton "Fermer"
        close_button = ctk.CTkButton(
            self.score_window,
            text="Fermer",
            command=self.score_window.destroy
        )
        close_button.pack(pady=10)


if __name__ == "__main__":
    root = ctk.CTk()
    qcm_id = 1  # Cette ligne est uniquement pour les tests. En production, l'ID est passé depuis main.py.
    app = QCMApp(root, qcm_id)
    root.mainloop()