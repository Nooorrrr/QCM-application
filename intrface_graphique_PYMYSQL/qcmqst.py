import customtkinter as ctk
from conn import connect_to_database
import pymysql.cursors

class QCMApp:
    def __init__(self, root, qcm_id):
        self.root = root
        self.qcm_id = qcm_id  # ID du QCM sélectionné
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

        # Footer
        self.footer_frame = ctk.CTkFrame(self.main_frame, height=50)
        self.footer_frame.pack(side="bottom", fill="x", padx=10, pady=(5, 10))

        self.name_entry = ctk.CTkEntry(self.footer_frame, placeholder_text="Nom Prenom", width=200)
        self.name_entry.pack(pady=5, padx=10)

    def fetch_qcm_info(self):
        """Récupérer toutes les informations du QCM depuis la base de données"""
        try:
            mydb = connect_to_database()
            cursor = mydb.cursor(pymysql.cursors.DictCursor)   # Récupérer les résultats sous forme de dictionnaire
            query = """
                SELECT qcm.nomqcm, qcm.categorie, qcm.idprof, qst.idqst, qst.enonce, answer.idanswer, answer.enonce AS answer_enonce
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
            self.title_label.configure(text=f"{qcm_title} - {qcm_category}")  # Changer 'config' en 'configure'

            print("QCM info:", self.qcm_info)

            # Afficher les questions et réponses
            current_question_id = None
            question_frame = None

            for record in self.qcm_info:
                question_id = record['idqst']
                question_text = record['enonce']
                answer_id = record['idanswer']
                answer_text = record['answer_enonce']

                # Créer un nouveau cadre pour la question si nécessaire
                if question_id != current_question_id:
                    current_question_id = question_id
                    question_frame = ctk.CTkFrame(self.question_frame, corner_radius=10)
                    question_frame.pack(fill="both", padx=10, pady=(5, 10))

                    question_label = ctk.CTkLabel(question_frame, text=question_text, font=("Arial", 16, "bold"))
                    question_label.pack(anchor="w", pady=(10, 5))

                # Afficher les réponses sous forme de cases à cocher
                if answer_id:
                    answer_item = ctk.CTkCheckBox(question_frame, text=answer_text)
                    answer_item.pack(anchor="w", pady=5)


if __name__ == "__main__":
    root = ctk.CTk()
    qcm_id = 1  # Remplacez par l'ID du QCM sélectionné
    app = QCMApp(root, qcm_id)
    root.mainloop()
