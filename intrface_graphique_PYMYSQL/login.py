<<<<<<< HEAD
import tkinter as tk
import customtkinter as ctk
import mysql.connector  # Remplace pymysql
from mysql.connector import Error
=======
import customtkinter as ctk
>>>>>>> 1bea7b4f06f9bd35e643544af29b205b47426ca1
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

<<<<<<< HEAD
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
=======

def show_login_window(signup_window=None):
    login_window = ctk.CTk()
>>>>>>> 1bea7b4f06f9bd35e643544af29b205b47426ca1
    login_window.title("Login")
    login_window.geometry("800x500")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # Sidebar Menu
    sidebar = ctk.CTkFrame(login_window, width=150)
    sidebar.pack(side="left", fill="y", padx=10, pady=10)
    ctk.CTkLabel(sidebar, text="MENU", font=("Arial", 16, "bold")).pack(pady=(20, 10))

    ctk.CTkButton(sidebar, text="LOGIN", command=lambda: None).pack(pady=10, fill="x")
    ctk.CTkButton(sidebar, text="SIGN-UP", command=lambda: [login_window.withdraw(), show_signup_window(login_window)]).pack(pady=10, fill="x")

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

    ctk.CTkButton(form_frame, text="Login", command=login).pack(pady=(20, 10))

    if signup_window:
        signup_window.withdraw()  # Masquer la fenêtre d'inscription

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

    ctk.CTkButton(sidebar, text="LOGIN", command=lambda: [signup_window.withdraw(), show_login_window(signup_window)]).pack(pady=10, fill="x")
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

        if not (username and name and email and password and confirm_password):
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
                    cursor.execute(query, (username, name, email, password, 'user'))
                    connection.commit()
                    messagebox.showinfo("Success", "Sign-Up successful!")
<<<<<<< HEAD
                    signup_window.destroy()
                    show_login_window()
            except mysql.connector.Error as e:
=======
                    signup_window.withdraw()
                    show_login_window(signup_window)
            except pymysql.MySQLError as e:
>>>>>>> 1bea7b4f06f9bd35e643544af29b205b47426ca1
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                connection.close()

    ctk.CTkButton(form_frame, text="Sign Up", command=signup).pack(pady=(20, 10))

    if login_window:
        login_window.withdraw()  # Masquer la fenêtre de connexion

    signup_window.mainloop()


# Launch the Login Window
show_login_window()