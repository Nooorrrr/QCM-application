import tkinter as tk
import customtkinter as ctk
import mysql.connector  # Remplace pymysql
from mysql.connector import Error
from tkinter import messagebox
import hashlib
from admin import QCMApp

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pswd",  # Remplacez par votre mot de passe
            database="qcm_test"
        )
        return connection
    except Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None
def show_login_window(signup_window=None):
    print("Affichage de la fenêtre de login...")  # Log pour déboguer
    login_window = ctk.CTk()
    login_window.title("Login")
    login_window.geometry("800x500")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # Sidebar Menu
    sidebar = ctk.CTkFrame(login_window, width=150)
    sidebar.pack(side="left", fill="y", padx=10, pady=10)
    ctk.CTkLabel(sidebar, text="MENU", font=("Arial", 16, "bold")).pack(pady=(20, 10))

    ctk.CTkButton(sidebar, text="LOGIN", command=lambda: None).pack(pady=10, fill="x")
    ctk.CTkButton(sidebar, text="SIGN-UP", command=lambda: [login_window.destroy(), show_signup_window()]).pack(pady=10, fill="x")

    # Login Form
    form_frame = ctk.CTkFrame(login_window, width=800, height=500, corner_radius=10)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(form_frame, text="Email", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(20, 5))
    email_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your email")
    email_entry.pack(fill="x", padx=20, pady=(0, 10))

    ctk.CTkLabel(form_frame, text="Password", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))
    password_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your password", show="*")
    password_entry.pack(fill="x", padx=20, pady=(0, 10))

    def login():
        email = email_entry.get()
        password = password_entry.get()

        if not (email and password):
            messagebox.showwarning("Error", "Please fill in all fields.")
            return
        hashed_password = hash_password(password)  

        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor(dictionary=True) as cursor:
                    query = "SELECT * FROM users WHERE email = %s AND password = %s"
                    cursor.execute(query, (email, hashed_password))
                    result = cursor.fetchone()

                    if result:
                        print(f"Utilisateur trouvé : {result}")  # Log pour déboguer
                        messagebox.showinfo("Login", f"Welcome, {result['name']}!")
                        login_window.destroy()  # Fermer la fenêtre de login

                        role = result['role']
                        if role == 'prof':
                            app = QCMApp(result['user_id'], result['name'])  # Ouvrir la page Admin
                            app.mainloop()  # Lancer la boucle principale de QCMApp
                        elif role == 'user':
                            messagebox.showinfo("Login", f"Welcome, {result['name']}!")
                            # Rediriger vers la page utilisateur 
                        else:
                            messagebox.showwarning("Login Failed", "Invalid role.")
                    else:
                        messagebox.showwarning("Login Failed", "Invalid email or password.")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                connection.close()

    tk.Button(form_frame, text="Login", bg="#333333", fg="white", font=("Helvetica", 12),
              relief="flat", cursor="hand2", command=login).pack(fill="x", pady=(10, 0), ipadx=5, ipady=5)

    if signup_window:
        signup_window.destroy()

    login_window.mainloop()

def show_signup_window(login_window=None):
    signup_window = ctk.CTk()
    signup_window.title("Sign-Up")
    signup_window.geometry("800x500")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # Sidebar Menu
    sidebar = ctk.CTkFrame(signup_window, width=150)
    sidebar.pack(side="left", fill="y", padx=10, pady=10)
    ctk.CTkLabel(sidebar, text="MENU", font=("Arial", 16, "bold")).pack(pady=(20, 10))

    ctk.CTkButton(sidebar, text="LOGIN", command=lambda: [signup_window.destroy(), show_login_window()]).pack(pady=10, fill="x")
    ctk.CTkButton(sidebar, text="SIGN-UP", command=lambda: None).pack(pady=10, fill="x")

    # Sign-Up Form
    form_frame = ctk.CTkFrame(signup_window, width=600, height=800, corner_radius=10)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(form_frame, text="Username", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(20, 5))
    username_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your username")
    username_entry.pack(fill="x", padx=20, pady=(0, 10))

    ctk.CTkLabel(form_frame, text="Name", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))
    name_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your name")
    name_entry.pack(fill="x", padx=20, pady=(0, 10))

    ctk.CTkLabel(form_frame, text="Email", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))
    email_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your email")
    email_entry.pack(fill="x", padx=20, pady=(0, 10))

    ctk.CTkLabel(form_frame, text="Password", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))
    password_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your password", show="*")
    password_entry.pack(fill="x", padx=20, pady=(0, 10))

    ctk.CTkLabel(form_frame, text="Confirm Password", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))
    confirm_password_entry = ctk.CTkEntry(form_frame, placeholder_text="Confirm your password", show="*")
    confirm_password_entry.pack(fill="x", padx=20, pady=(0, 10))

    def signup():
        username = username_entry.get()
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not (username and email and password and confirm_password):
            messagebox.showwarning("Error", "Please fill in all fields.")
            return

        if password != confirm_password:
            messagebox.showwarning("Error", "Passwords do not match.")
            return
        
        hashed_password = hash_password(password)  # Hash the password before storing it

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
                    cursor.execute(query, (username, name, email, hashed_password, 'user'))  # Définir 'user' comme rôle par défaut

                    connection.commit()
                    messagebox.showinfo("Success", "Sign-Up successful!")
                    signup_window.destroy()
                    show_login_window()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                connection.close()

    ctk.CTkButton(form_frame, text="Sign Up", command=signup).pack(pady=(20, 10))

    if login_window:
        login_window.destroy()

    signup_window.mainloop()

# Lancer la première fenêtre Login
if __name__ == "__main__":
    show_login_window()