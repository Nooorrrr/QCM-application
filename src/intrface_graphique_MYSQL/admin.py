import customtkinter as ctk
import mysql.connector
from tkinter import messagebox

# Configuration de l'apparence
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Thèmes: "blue" (default), "green", "dark-blue"

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pswd",  # Utilisez le mot de passe correct pour la connexion
        database="qcm_test"
    )

class QCMApp(ctk.CTk):
    def __init__(self, user_id, user_name):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name
        self.title("Gestion des QCM")
        self.geometry("1000x600")

        # Sidebar Menu
        self.sidebar = ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(self.sidebar, text="MENU", font=("Arial", 16, "bold")).pack(pady=(20, 10))
        ctk.CTkButton(self.sidebar, text="Mes QCM", command=self.show_mes_qcm).pack(pady=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Nouveau QCM", command=self.show_nouveau_qcm).pack(pady=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Déconnexion", command=self.destroy).pack(pady=10, fill="x")

        # Main Content Frame
        self.main_content = ctk.CTkFrame(self, corner_radius=10)
        self.main_content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.show_mes_qcm()

    def show_mes_qcm(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_content, text="Mes QCM", font=("Arial", 20, "bold")).pack(pady=20)

        conn = connect_to_db()
        if conn is None:
            ctk.CTkLabel(self.main_content, text="Erreur de connexion à la base de données.").pack()
            return

        cursor = conn.cursor()
        cursor.execute("""
            SELECT qcm.idqcm, qcm.nomqcm, COUNT(qcm_user.iduser) AS nb_prsn
            FROM qcm
            LEFT JOIN qcm_user ON qcm.idqcm = qcm_user.idqcm
            WHERE qcm.idprof = %s
            GROUP BY qcm.idqcm
        """, (self.user_id,))

        qcm_data = cursor.fetchall()
        cursor.close()
        conn.close()

        for (idqcm, nomqcm, nb_prsn) in qcm_data:
            qcm_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
            qcm_frame.pack(fill="x", pady=5, padx=10)

            ctk.CTkLabel(qcm_frame, text=f"ID: {idqcm} | Nom: {nomqcm} | Réponses: {nb_prsn}", font=("Arial", 14)).pack(side="left", padx=10)
    def show_nouveau_qcm(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_content, text="Nouveau QCM", font=("Arial", 20, "bold")).pack(pady=20)

        self.nom_qcm_entry = ctk.CTkEntry(self.main_content, placeholder_text="Nom du QCM")
        self.nom_qcm_entry.pack(fill="x", pady=5, padx=10)

        self.categorie_var = ctk.StringVar(value="THI")
        self.categorie_menu = ctk.CTkOptionMenu(self.main_content, values=["THI", "BI", "COMPILE", "AP", "GL", "RO", "CRYPTO", "WEB"], variable=self.categorie_var)
        self.categorie_menu.pack(fill="x", pady=5, padx=10)

        self.questions_frame = ctk.CTkScrollableFrame(self.main_content)
        self.questions_frame.pack(fill="both", expand=True, pady=10, padx=10)

        self.questions = []

        ctk.CTkButton(self.main_content, text="Ajouter une question", command=self.ajouter_question).pack(pady=5)
        ctk.CTkButton(self.main_content, text="Créer le QCM", command=self.creer_qcm).pack(pady=10)

    def ajouter_question(self):
        question_frame = ctk.CTkFrame(self.questions_frame)
        question_frame.pack(fill="x", pady=5, padx=10)

        question_entry = ctk.CTkEntry(question_frame, placeholder_text="Entrez la question")
        question_entry.pack(fill="x", pady=5, padx=10)

        reponses_frame = ctk.CTkFrame(question_frame)
        reponses_frame.pack(fill="x", pady=5, padx=10)

        reponses = []

        def ajouter_reponse():
            reponse_frame = ctk.CTkFrame(reponses_frame)
            reponse_frame.pack(fill="x", pady=5, padx=10)

            reponse_entry = ctk.CTkEntry(reponse_frame, placeholder_text="Entrez la réponse")
            reponse_entry.pack(side="left", fill="x", expand=True, pady=5, padx=5)

            correct_var = ctk.BooleanVar(value=False)
            correct_checkbox = ctk.CTkCheckBox(reponse_frame, text="Correcte", variable=correct_var)
            correct_checkbox.pack(side="left", pady=5, padx=5)

            reponses.append((reponse_entry, correct_var))

        ajouter_reponse_button = ctk.CTkButton(question_frame, text="Ajouter une réponse", command=ajouter_reponse)
        ajouter_reponse_button.pack(pady=5)

        self.questions.append((question_entry, reponses))

    def creer_qcm(self):
        nom = self.nom_qcm_entry.get()
        categorie = self.categorie_var.get()

        if not nom or not categorie:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO qcm (nomqcm, categorie, idprof) VALUES (%s, %s, %s)", (nom, categorie, self.user_id))
            qcm_id = cursor.lastrowid

            for question_entry, reponses in self.questions:
                question_text = question_entry.get()
                if question_text:
                    cursor.execute("INSERT INTO qst (idqcm, enonce) VALUES (%s, %s)", (qcm_id, question_text))
                    qst_id = cursor.lastrowid

                    for reponse_entry, correct_var in reponses:
                        reponse_text = reponse_entry.get()
                        if reponse_text:
                            cursor.execute("INSERT INTO answer (idqst, enonce, statut) VALUES (%s, %s, %s)", (qst_id, reponse_text, correct_var.get()))

            conn.commit()
            messagebox.showinfo("Succès", "QCM créé avec succès.")
            self.show_mes_qcm()
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur : {err}")
        finally:
            cursor.close()
            conn.close()


    conn = connect_to_db()
    cursor = conn.cursor()
   