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

def create_placeholder_label(parent, text, x, y):
    return tk.Label(parent, text=text, bg="white", fg="#666666", font=("Helvetica", 10), anchor="w")

def handle_focus_in(event, label):
    label.config(fg="#007BFF")  # Change label color when field is focused

def handle_focus_out(event, label, entry):
    label.config(fg="#666666" if not entry.get() else "#007BFF")

# Main window setup
root = tk.Tk()
root.title("Login Interface")
root.geometry("600x400")

# Background setup
background_image = Image.open("BG.jpg")
background_image = background_image.resize((600, 400), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=600, height=400)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Style configuration
bg_color = "#1E1E1E"
fg_color = "#FFFFFF"
border_color = "#5A5A5A"
font = ("Helvetica", 12)

# Main frame
frame = tk.Frame(canvas, bg="white", bd=0)
frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)

# Email field with floating label
email_label = create_placeholder_label(frame, "Email", 50, 60)
email_label.place(x=50, y=60)

email_entry = tk.Entry(frame, bg="white", fg="black", font=font, insertbackground=fg_color, bd=0)
email_entry.place(x=50, y=80, width=300, height=25)
email_entry.config(highlightbackground=border_color, highlightcolor=fg_color, highlightthickness=1)

# Bind focus events for email
email_entry.bind("<FocusIn>", lambda e: handle_focus_in(e, email_label))
email_entry.bind("<FocusOut>", lambda e: handle_focus_out(e, email_label, email_entry))

# Password field with floating label
password_label = create_placeholder_label(frame, "Password", 50, 130)
password_label.place(x=50, y=130)

password_entry = tk.Entry(frame, bg="white", fg="black", font=font, show="*", insertbackground=fg_color, bd=0)
password_entry.place(x=50, y=150, width=300, height=25)
password_entry.config(highlightbackground=border_color, highlightcolor=fg_color, highlightthickness=1)

# Bind focus events for password
password_entry.bind("<FocusIn>", lambda e: handle_focus_in(e, password_label))
password_entry.bind("<FocusOut>", lambda e: handle_focus_out(e, password_label, password_entry))

# Login button
login_button = tk.Button(frame, text="Login", bg=border_color, fg=fg_color, font=font, relief="flat", command=login)
login_button.place(x=50, y=200, width=300, height=35)

# Forgot password link
forgot_password = tk.Label(frame, text="Forgot password?", bg="white", fg="#007BFF", font=("Helvetica", 10), cursor="hand2")
forgot_password.place(x=50, y=250)

root.mainloop()