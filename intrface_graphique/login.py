import tkinter as tk
import customtkinter as ctk
import mysql.connector  # Remplace pymysql
from mysql.connector import Error
from tkinter import messagebox


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



def show_login_window():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("800x500")
    login_window.configure(bg="#0a0a0a")

    # Menu latéral
    menu_frame = tk.Frame(login_window, bg="#1a1a1a", width=150, height=500)
    menu_frame.pack(side="left", fill="y")
    menu_frame.pack_propagate(False)

    menu_title = tk.Label(menu_frame, text="MENU", bg="#1a1a1a", fg="white", font=("Helvetica", 14, "bold"))
    menu_title.pack(pady=20)

    def open_signup():
        login_window.destroy()
        show_signup_window()

    def open_login():
        pass  # Déjà sur la page Login

    tk.Button(menu_frame, text="LOGIN", bg="#1a1a1a", fg="white", font=("Helvetica", 10),
              relief="flat", cursor="hand2", command=open_login).place(x=0, y=150, width=150)
    tk.Button(menu_frame, text="SIGN-UP", bg="#1a1a1a", fg="white", font=("Helvetica", 10),
              relief="flat", cursor="hand2", command=open_signup).place(x=0, y=200, width=150)

    # Contenu Login
    form_frame = tk.Frame(login_window, bg="#1a1a1a", padx=20, pady=20, width=500)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(form_frame, text="Email", bg="#1a1a1a", fg="white", font=("Helvetica", 12)).pack(anchor="w")
    email_entry = tk.Entry(form_frame, bg="#333333", fg="white", font=("Helvetica", 12), insertbackground="white")
    email_entry.pack(fill="x", pady=(5, 10), ipadx=5, ipady=5)

    tk.Label(form_frame, text="Password", bg="#1a1a1a", fg="white", font=("Helvetica", 12)).pack(anchor="w")
    password_entry = tk.Entry(form_frame, bg="#333333", fg="white", font=("Helvetica", 12), show="*", insertbackground="white")
    password_entry.pack(fill="x", pady=(5, 10), ipadx=5, ipady=5)

    def login():
        email = email_entry.get()
        password = password_entry.get()

        if not (email and password):
            messagebox.showwarning("Error", "Please fill in all fields.")
            return

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
            except  mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                connection.close()

    tk.Button(form_frame, text="Login", bg="#333333", fg="white", font=("Helvetica", 12),
              relief="flat", cursor="hand2", command=login).pack(fill="x", pady=(10, 0), ipadx=5, ipady=5)

    login_window.mainloop()

def show_signup_window():
    signup_window = tk.Tk()
    signup_window.title("Sign-Up")
    signup_window.geometry("800x500")
    signup_window.configure(bg="#0a0a0a")

    # Menu latéral
    menu_frame = tk.Frame(signup_window, bg="#1a1a1a", width=150, height=500)
    menu_frame.pack(side="left", fill="y")
    menu_frame.pack_propagate(False)

    menu_title = tk.Label(menu_frame, text="MENU", bg="#1a1a1a", fg="white", font=("Helvetica", 14, "bold"))
    menu_title.pack(pady=20)

    def open_login():
        signup_window.destroy()
        show_login_window()

    def open_signup():
        pass  # Déjà sur la page Sign-Up

    tk.Button(menu_frame, text="LOGIN", bg="#1a1a1a", fg="white", font=("Helvetica", 10),
              relief="flat", cursor="hand2", command=open_login).place(x=0, y=150, width=150)
    tk.Button(menu_frame, text="SIGN-UP", bg="#1a1a1a", fg="white", font=("Helvetica", 10),
              relief="flat", cursor="hand2", command=open_signup).place(x=0, y=200, width=150)

    # Contenu Sign-Up
    form_frame = tk.Frame(signup_window, bg="#1a1a1a", padx=20, pady=20, width=500)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(form_frame, text="Username", bg="#1a1a1a", fg="white", font=("Helvetica", 12)).pack(anchor="w")
    username_entry = tk.Entry(form_frame, bg="#333333", fg="white", font=("Helvetica", 12), insertbackground="white")
    username_entry.pack(fill="x", pady=(5, 10), ipadx=5, ipady=5)


    tk.Label(form_frame, text="name", bg="#1a1a1a", fg="white", font=("Helvetica", 12)).pack(anchor="w")
    name_entry = tk.Entry(form_frame, bg="#333333", fg="white", font=("Helvetica", 12), insertbackground="white")
    name_entry.pack(fill="x", pady=(5, 10), ipadx=5, ipady=5)

    tk.Label(form_frame, text="Email", bg="#1a1a1a", fg="white", font=("Helvetica", 12)).pack(anchor="w")
    email_entry = tk.Entry(form_frame, bg="#333333", fg="white", font=("Helvetica", 12), insertbackground="white")
    email_entry.pack(fill="x", pady=(5, 10), ipadx=5, ipady=5)

    tk.Label(form_frame, text="Password", bg="#1a1a1a", fg="white", font=("Helvetica", 12)).pack(anchor="w")
    password_entry = tk.Entry(form_frame, bg="#333333", fg="white", font=("Helvetica", 12), show="*", insertbackground="white")
    password_entry.pack(fill="x", pady=(5, 10), ipadx=5, ipady=5)

    tk.Label(form_frame, text="Confirm Password", bg="#1a1a1a", fg="white", font=("Helvetica", 12)).pack(anchor="w")
    confirm_password_entry = tk.Entry(form_frame, bg="#333333", fg="white", font=("Helvetica", 12), show="*", insertbackground="white")
    confirm_password_entry.pack(fill="x", pady=(5, 10), ipadx=5, ipady=5)

    def signup():
        username = username_entry.get()
        name=name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not (username and email and password and confirm_password):
            messagebox.showwarning("Error", "Please fill in all fields.")
            return

        if password != confirm_password:
            messagebox.showwarning("Error", "Passwords do not match.")
            return

        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM users WHERE email = %s"
                    cursor.execute(query, (email,))
                    if cursor.fetchone():
                        messagebox.showwarning("Error", "Email already exists.")
                        return

                    query = "INSERT INTO users (username, name, email, password, role) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(query,
                                   (username, name, email, password, 'user'))  # Définir 'user' comme rôle par défaut

                    connection.commit()
                    messagebox.showinfo("Success", "Sign-Up successful!")
                    signup_window.destroy()
                    show_login_window()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                connection.close()

    tk.Button(form_frame, text="Sign Up", bg="#333333", fg="white", font=("Helvetica", 12),
              relief="flat", cursor="hand2", command=signup).pack(fill="x", pady=(10, 0), ipadx=5, ipady=5)

    signup_window.mainloop()

# Lancer la première fenêtre Login
show_login_window()