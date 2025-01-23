import customtkinter as ctk
from conn import connect_to_database
from qcmqst import QCMApp


def fetch_qcm_data():
    try:
        mydb = connect_to_database()
        cursor = mydb.cursor()
        cursor.execute("SELECT idqcm, nomqcm, categorie, name FROM qcm JOIN users ON qcm.idprof = users.user_id")
        qcm_data = cursor.fetchall()

        return qcm_data
    except Exception as e:
        print("Erreur lors de la récupération des données :", e)
        return []
    finally:
        if 'mydb' in locals() and mydb:
            mydb.close()


class QCMSInterface:
    def __init__(self, root):
        # Configuration principale
        self.root = root
        self.root.title("QCMS")
        ctk.set_appearance_mode("dark")  # Mode sombre
        ctk.set_default_color_theme("dark-blue")

        # Frame principale
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Barre latérale
        self.sidebar = ctk.CTkFrame(self.main_frame, width=200)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10), pady=10)

        ctk.CTkLabel(self.sidebar, text="Menu", font=("Arial", 18, "bold"), anchor="center").pack(pady=20)
        self.menu_btn1 = ctk.CTkButton(self.sidebar, text="QCMS", width=150)
        self.menu_btn1.pack(pady=5)
        self.menu_btn2 = ctk.CTkButton(self.sidebar, text="My history", width=150)
        self.menu_btn2.pack(pady=5)

        # Contenu principal
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Titre
        ctk.CTkLabel(self.content_frame, text="Liste des QCM disponibles", font=("Arial", 18)).pack(pady=10)

        # Table
        self.table_frame = ctk.CTkFrame(self.content_frame)
        self.table_frame.pack(fill="both", expand=True, pady=10, padx=10)

        # Grille de contenu
        self.create_table_headers()
        self.populate_table()

    def create_table_headers(self):
        """Créer les en-têtes du tableau"""
        headers = ["ID", "NOMQCM", "MODULE", "PROF", "ACTION"]  # Ajout de "ID"
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                self.table_frame, text=header, font=("Arial", 14, "bold"), text_color="white"
            )
            header_label.grid(row=0, column=col, padx=10, pady=5, sticky="ew")

        # Configurer les colonnes pour s'étendre uniformément
        for col in range(len(headers)):
            self.table_frame.grid_columnconfigure(col, weight=1)

    def populate_table(self):
        """Remplir le tableau avec des données récupérées depuis la base"""
        qcm_data = fetch_qcm_data()

        # Effacer les lignes précédentes (sauf les en-têtes)
        for widget in self.table_frame.winfo_children():
            if widget.grid_info()["row"] > 0:  # Ignore les en-têtes
                widget.destroy()

        # Ajouter des lignes au tableau
        for row, data in enumerate(qcm_data, start=1):
            idqcm = data['idqcm']  # Récupérer l'ID
            nomqcm = data['nomqcm']
            categorie = data['categorie']
            prof = data['name']

            # Afficher l'ID dans la première colonne
            ctk.CTkLabel(self.table_frame, text=idqcm, text_color="white").grid(
                row=row, column=0, padx=10, pady=5, sticky="ew"
            )

            # Colonnes de texte
            ctk.CTkLabel(self.table_frame, text=nomqcm, text_color="white").grid(
                row=row, column=1, padx=10, pady=5, sticky="ew"
            )
            ctk.CTkLabel(self.table_frame, text=categorie, text_color="white").grid(
                row=row, column=2, padx=10, pady=5, sticky="ew"
            )
            ctk.CTkLabel(self.table_frame, text=prof, text_color="white").grid(
                row=row, column=3, padx=10, pady=5, sticky="ew"
            )

            # Bouton d'action
            action_btn = ctk.CTkButton(
                self.table_frame,
                text="Answer",
                fg_color="#1E90FF",
                width=80,
                height=30,
                command=lambda qcm_id=idqcm: self.open_qcm_page(qcm_id)  # Lier le bouton à la nouvelle page
            )
            action_btn.grid(row=row, column=4, padx=10, pady=5)

    def open_qcm_page(self, qcm_id):
        """Ouvrir une nouvelle fenêtre pour afficher les questions du QCM"""
        qcm_window = ctk.CTkToplevel(self.root)  # Créer une nouvelle fenêtre
        qcm_window.geometry("800x600")  # Définir la taille
        qcm_window.transient(self.root)  # Lier la fenêtre
        qcm_window.grab_set()
        QCMApp(qcm_window, qcm_id)


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("900x600")
    app = QCMSInterface(root)
    root.mainloop()