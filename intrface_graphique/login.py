import tkinter as tk
from tkinter import messagebox
import pymysql
from pymysql.cursors import DictCursor

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

# Créer la fenêtre principale
root = tk.Tk()
root.title("Login Interface")
root.geometry("600x400")
root.configure(bg="#1E1E1E")

# Style global
bg_color = "#1E1E1E"
fg_color = "#FFFFFF"
border_color = "#5A5A5A"
font = ("Helvetica", 12)

# Cadre principal
frame = tk.Frame(root, bg=bg_color, highlightbackground=border_color, highlightthickness=1)
frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)

# Email label et champ de saisie
tk.Label(frame, text="Email", bg=bg_color, fg=fg_color, font=font).place(x=50, y=50)
email_entry = tk.Entry(frame, bg=bg_color, fg=fg_color, font=font, insertbackground=fg_color, bd=0)
email_entry.place(x=50, y=80, width=300, height=25)
email_entry.config(highlightbackground=border_color, highlightcolor=fg_color, highlightthickness=1)

# Password label et champ de saisie
tk.Label(frame, text="Password", bg=bg_color, fg=fg_color, font=font).place(x=50, y=120)
password_entry = tk.Entry(frame, bg=bg_color, fg=fg_color, font=font, show="*", insertbackground=fg_color, bd=0)
password_entry.place(x=50, y=150, width=300, height=25)
password_entry.config(highlightbackground=border_color, highlightcolor=fg_color, highlightthickness=1)

# Bouton login
login_button = tk.Button(frame, text="Login", bg=border_color, fg=fg_color, font=font, relief="flat", command=login)
login_button.place(x=50, y=200, width=300, height=35)

# Lien "Forgot password?"
forgot_password = tk.Label(frame, text="Forgot password?", bg=bg_color, fg="#007BFF", font=("Helvetica", 10), cursor="hand2")
forgot_password.place(x=50, y=250)

# Lancer l'application
root.mainloop()