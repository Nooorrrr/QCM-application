import tkinter as tk
import customtkinter as ctk
import mysql.connector  # Remplace pymysql
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pswd",#diro password ta3kom hna, bon genrallemnt faregh, mais bon
            database="qcm_test"
        )
        return connection
    except Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None

def fetch_qcm_data():
    try:
        mydb = connect_to_database()
        if not mydb:
            raise Exception("La connexion à la base de données a échoué.")
        
        cursor = mydb.cursor(dictionary=True)  # Pour obtenir les résultats sous forme de dictionnaire
        cursor.execute("SELECT nomqcm, categorie, name FROM qcm JOIN users ON qcm.idprof = users.user_id")
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
        self.root = root
        self.root.title("QCMS")
        self.root.configure(bg="#1a1a1a")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Content area
        content_area = ctk.CTkFrame(self.main_frame)
        content_area.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ctk.CTkFrame(content_area)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))

        self.menu_btn1 = ctk.CTkButton(self.sidebar, text="QCMS", width=150)
        self.menu_btn1.pack(pady=5)

        self.menu_btn2 = ctk.CTkButton(self.sidebar, text="My history", width=150)
        self.menu_btn2.pack(pady=5)

        # Table container
        table_container = ctk.CTkFrame(content_area)
        table_container.pack(side="left", fill="both", expand=True)

        # Title above table
        title_frame = ctk.CTkFrame(table_container)
        title_frame.pack(pady=(20, 30))
        table_title = ctk.CTkLabel(title_frame, text="Liste des QCM disponibles", font=("Arial", 18))
        table_title.pack()

        # Table frame
        self.content = ctk.CTkFrame(table_container)
        self.content.pack(anchor="n")

        # Grid configuration
        for i in range(4):
            self.content.grid_columnconfigure(i, weight=1, minsize=150)

        # Headers
        headers = ["NOMQCM", "MODULE", "PROF", "Action"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.content, text=header, text_color="gray")
            label.grid(row=0, column=i, sticky="ew", padx=5, pady=5)

        # Remplir le tableau avec les données de la base de données
        self.populate_table()

        # Footer
        self.footer = ctk.CTkFrame(self.root)
        self.footer.pack(fill="x", side="bottom")

        self.name_entry = ctk.CTkEntry(self.footer, placeholder_text="Nom Prenom")
        self.name_entry.pack(side="left", padx=10, pady=5)

    def populate_table(self):
        # Récupérer les données de la base de données
        qcm_data = fetch_qcm_data()

        # Effacer le contenu existant du tableau (sauf les en-têtes)
        for widget in self.content.winfo_children():
            if widget.grid_info()["row"] != 0:  # Ne pas supprimer les en-têtes
                widget.destroy()

        # Remplir le tableau avec les données
        for row, data in enumerate(qcm_data, start=1):
            # Extraire les valeurs à partir du dictionnaire
            nomqcm = data['nomqcm']
            categorie = data['categorie']
            prof = data['name']

            # Afficher les données dans les colonnes
            label_nomqcm = ctk.CTkLabel(self.content, text=nomqcm, text_color="white")
            label_nomqcm.grid(row=row, column=0, sticky="ew", padx=5, pady=2)

            label_categorie = ctk.CTkLabel(self.content, text=categorie, text_color="white")
            label_categorie.grid(row=row, column=1, sticky="ew", padx=5, pady=2)

            label_prof = ctk.CTkLabel(self.content, text=prof, text_color="white")
            label_prof.grid(row=row, column=2, sticky="ew", padx=5, pady=2)

            # Bouton d'action
            action_btn = ctk.CTkButton(self.content, text="Action", fg_color="#1E90FF",width=80, height=30)
            action_btn.grid(row=row, column=3, padx=5, pady=2)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = QCMSInterface(root)
    root.mainloop()