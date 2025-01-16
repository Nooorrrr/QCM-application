import pymysql
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Fonction pour charger les données depuis la base de données
def load_data():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='QCM_PY'
        )
        cursor = connection.cursor()

        # Récupérer les données
        query = """
        SELECT qcm.idqcm, qcm.nomqcm, qcm.categorie, users.name 
        FROM qcm
        JOIN users ON qcm.idprof = users.user_id;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Supprimer les anciennes données
        for item in table.get_children():
            table.delete(item)

        # Insérer les nouvelles données dans le Treeview
        for row in rows:
            table.insert('', 'end', values=row)

    except pymysql.MySQLError as e:
        print(f"Erreur MySQL: {e}")
    finally:
        if connection:
            connection.close()

# Fonction appelée lorsqu'on clique sur un bouton "Faire QCM"
def start_qcm(qcm_id):
    messagebox.showinfo("Faire QCM", f"Démarrage du QCM avec l'ID: {qcm_id}")

# Interface principale Tkinter
root = tk.Tk()
root.title("Tableau des QCM")
root.geometry("1000x500")

# Créer le tableau avec Treeview
columns = ("idqcm", "nomqcm", "categorie", "professeur")
table = ttk.Treeview(root, columns=columns, show="headings", height=15)

# Configurer les colonnes
table.heading("idqcm", text="ID QCM")
table.heading("nomqcm", text="Nom QCM")
table.heading("categorie", text="Catégorie")
table.heading("professeur", text="Professeur")
table.column("idqcm", width=80, anchor="center")
table.column("nomqcm", width=200, anchor="center")
table.column("categorie", width=150, anchor="center")
table.column("professeur", width=150, anchor="center")
table.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

# Canvas pour ajouter les boutons dynamiques
action_frame = tk.Frame(root)
action_frame.pack(side=tk.RIGHT, fill="y")

# Ajouter des boutons dynamiques dans la colonne "Action"
def add_buttons_to_table():
    for widget in action_frame.winfo_children():
        widget.destroy()  # Supprimer les anciens boutons

    for child in table.get_children():
        row_data = table.item(child)['values']
        qcm_id = row_data[0]  # L'ID QCM

        # Créer un bouton pour chaque ligne
        button = tk.Button(action_frame, text="Faire QCM", command=lambda qcm_id=qcm_id: start_qcm(qcm_id))
        button.pack(pady=5)

# Bouton pour charger les données
load_button = tk.Button(root, text="Charger les données", command=lambda: [load_data(), add_buttons_to_table()])
load_button.pack(side=tk.TOP, pady=10)

root.mainloop()
