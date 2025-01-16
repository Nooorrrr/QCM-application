import tkinter as tk
from tkinter import messagebox
import pymysql
from pymysql.cursors import DictCursor
from PIL import Image, ImageTk

def connect_to_database():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='qcm_py',
            cursorclass=DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
        return None

def login():
    email = email_entry.get()
    password = password_entry.get()

    if email and password:
        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM users WHERE email = %s AND password = %s"
                    cursor.execute(query, (email, password))
                    result = cursor.fetchone()

                    if result:
                        messagebox.showinfo("Login", f"Welcome, {result['name']}!")
                    else:
                        messagebox.showwarning("Login Failed", "Invalid email or password.")
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                connection.close()
    else:
        messagebox.showwarning("Error", "Please fill in all fields.")

def create_menu_button(parent, text, y_position, command=None):
    button = tk.Button(parent, text=text,
                      bg="#1a1a1a",
                      fg="white",
                      font=("Helvetica", 10),
                      bd=0,
                      relief="flat",
                      activebackground="#2a2a2a",
                      activeforeground="white",
                      cursor="hand2",
                      width=20,
                      command=command)
    button.place(x=0, y=y_position, width=150)
    return button

def show_login_frame():
    login_frame.tkraise()

def show_signup_frame():
    # À implémenter plus tard
    pass

def show_accueil_frame():
    # À implémenter plus tard
    pass

# Configuration de la fenêtre principale
root = tk.Tk()
root.title("Login Interface")
root.geometry("800x500")

# Style global
bg_color = "#0a0a0a"
fg_color = "#FFFFFF"
accent_color = "#1a1a1a"
font = ("Helvetica", 12)

# Fond principal
root.configure(bg=bg_color)

# Création du menu latéral
menu_frame = tk.Frame(root, bg=accent_color, width=150, height=500)
menu_frame.pack(side="left", fill="y")
menu_frame.pack_propagate(False)

# Titre du menu
menu_title = tk.Label(menu_frame, text="LOG-IN", bg=accent_color, fg="white", font=("Helvetica", 14, "bold"))
menu_title.pack(pady=20)

# Boutons du menu
create_menu_button(menu_frame, "ACCUEIL", 100, show_accueil_frame)
create_menu_button(menu_frame, "LOGIN", 150, show_login_frame)
create_menu_button(menu_frame, "SIGN-UP", 200, show_signup_frame)

# Frame principal pour le contenu
content_frame = tk.Frame(root, bg=bg_color)
content_frame.pack(side="left", fill="both", expand=True)

# Frame de login
login_frame = tk.Frame(content_frame, bg=bg_color)
login_frame.pack(fill="both", expand=True)

# Conteneur pour centrer le formulaire
form_container = tk.Frame(login_frame, bg=bg_color, padx=50, pady=50)
form_container.place(relx=0.5, rely=0.5, anchor="center")

# Cadre autour du formulaire (avec une largeur spécifique)
form_frame = tk.Frame(form_container, bg="#1a1a1a", bd=2, relief="solid", padx=20, pady=20,width=500)
form_frame.pack(fill="x", padx=10, pady=10)  # fill="x" pour s'adapter à la largeur du conteneur

# Labels et champs de saisie
tk.Label(form_frame, text="Email", bg="#1a1a1a", fg=fg_color, font=font).pack(anchor="w")
email_entry = tk.Entry(form_frame, bg="#333333", fg=fg_color, font=font, insertbackground=fg_color ,width=30)
email_entry.pack(fill="x", pady=(5, 20), ipadx=10, ipady=5)  # ipadx et ipady pour un padding interne
email_entry.configure(highlightthickness=1, highlightbackground="#555555")

tk.Label(form_frame, text="Password", bg="#1a1a1a", fg=fg_color, font=font).pack(anchor="w")
password_entry = tk.Entry(form_frame, bg="#333333", fg=fg_color, font=font, show="*", insertbackground=fg_color,width=30)
password_entry.pack(fill="x", pady=(5, 20), ipadx=10, ipady=5)  # ipadx et ipady pour un padding interne
password_entry.configure(highlightthickness=1, highlightbackground="#555555")

# Bouton de connexion
login_button = tk.Button(form_frame, text="Login", bg="#333333", fg=fg_color, font=font,
                        relief="flat", command=login, cursor="hand2")
login_button.pack(fill="x", pady=(10, 20), ipadx=10, ipady=5)  # ipadx et ipady pour un padding interne

# Lien "Forgot password?"
forgot_password = tk.Label(form_frame, text="Forgot password?", bg="#1a1a1a", fg="#4a9eff",
                         font=("Helvetica", 10), cursor="hand2")
forgot_password.pack()

# Lancer l'application
root.mainloop()