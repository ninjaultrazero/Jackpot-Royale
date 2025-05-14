import customtkinter as ctk
import re
import json
import os
from PIL import Image, ImageTk
from main import *
import session
from session import set_logged_user

# Percorso del file JSON
pathFile = os.path.dirname(os.path.abspath(__file__))  
json_path = os.path.join(pathFile, "users.json") 

ctk.set_appearance_mode("dark")
# ----------------------- UTILS -----------------------

def window_login_geometry(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 900
    window_height = 490
    x_cordinate = (screen_width - window_width) // 2
    y_cordinate = (screen_height - window_height) // 2
    return f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}"

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

def is_email_registered(email):
    try:
        if os.path.exists(json_path):
            with open(json_path, "r") as file:
                users = json.load(file)
                for user in users:
                    if user["email"] == email and user["status"] == "user":
                        return True
        return False
    except json.JSONDecodeError:
        return False


# ----------------------- UI COMPONENTS -----------------------

def image_label_logo(root):
    frame = ctk.CTkFrame(root, height=200, width=200, fg_color="transparent")
    frame.pack(pady=20)
    
    img_path = os.path.join(pathFile, "./immagini/scienere.jpeg") 
    image = Image.open(img_path).resize((200, 200))
    photo = ctk.CTkImage(light_image=image, dark_image=image, size=(200, 200))
    
    img_label = ctk.CTkLabel(frame, image=photo, text="")
    img_label.pack()

def frame_imagine_log(root):
    frame = ctk.CTkFrame(master=root, fg_color="green", width=500, height=600, corner_radius=0)
    frame.place(relx=0, rely=0)
    return frame

def frame_label_log(root):
    frame = ctk.CTkFrame(master=root, fg_color="transparent", width=500, height=600, corner_radius=0)
    frame.place(relx=0.5, rely=0)
    return frame

def image_side(frame):
    img_path = os.path.join(pathFile, "./immagini/scienere.jpeg") 
    image = Image.open(img_path).resize((500, 600))
    photo = ImageTk.PhotoImage(image)

    img_label = ctk.CTkLabel(frame, image=photo, text="")
    img_label.photo = photo
    img_label.pack(pady=0, padx=0)


# ----------------------- MAIN LOGIN/REGISTER UI -----------------------

def create_login(root, visitor_log_window, registration_status):
    ctk.CTkLabel(master=root, text_color="gold", text="Welcome", font=("Helvetica", 30, "bold")).place(relx=0.5, rely=0.15, anchor="center")

    widget_frame = ctk.CTkFrame(master=root, fg_color="transparent")
    widget_frame.place(relx=0.1, rely=0.225)

    # Email
    ctk.CTkLabel(master=widget_frame, text_color="gold", text="📧 Email", font=("Helvetica", 14, "bold")).place(relx=0)
    email_entry = ctk.CTkEntry(master=widget_frame, placeholder_text="Email", width=300, font=("Helvetica", 14))
    email_entry.pack(pady=(30, 30))

    # Password
    ctk.CTkLabel(master=widget_frame, text_color="gold", text="🔑 Password", font=("Helvetica", 14, "bold")).place(relx=0, rely=0.25)
    password_entry = ctk.CTkEntry(master=widget_frame, placeholder_text="Password", width=300, font=("Helvetica", 14), show="*")
    password_entry.pack(pady=5)

    # Show password checkbox
    def toggle_password_visibility():
        password_entry.configure(show="" if show_password_var.get() else "*")

    show_password_var = ctk.BooleanVar(value=False)
    ctk.CTkCheckBox(
        master=widget_frame,
        text="Mostra Password",
        variable=show_password_var,
        command=toggle_password_visibility,
        font=("Helvetica", 12),
        text_color="gray"
    ).pack(pady=10)

    # Message label
    message_label = ctk.CTkLabel(master=root, text_color="red", font=("Helvetica", 12))
    message_label.place_forget()

    # Navigate to next window
    def new_visitor_window(current_window, email=None):
        current_window.destroy()
        registration_status[0] = True
        if email and is_valid_email(email):
            session.current_user_email = email
        start_casino()

    # Login function
    def login_user():
        email = email_entry.get()
        password = password_entry.get()

        if not email or not password:
            show_message("Inserisci email e password.", "red")
        elif not is_valid_email(email):
            show_message("Email non valida. Controlla il formato.", "red")
        else:
            try:
                with open(json_path, "r") as file:
                    users = json.load(file)
                    for user in users:
                        if user["email"] == email and user["password"] == password and user["status"] == "user":
                            show_message("Login effettuato con successo!", "green")
                            set_logged_user(email)
                            visitor_log_window.after(1500, lambda: new_visitor_window(visitor_log_window, email))
                            return
                    show_message("Email o password errata.", "red")
            except json.JSONDecodeError:
                show_message("Errore nel file utenti.", "red")

    # Register function
    def register_user():
        email = email_entry.get()
        password = password_entry.get()

        if not email or not password:
            show_message("Inserisci email e password", "red")
        elif not is_valid_email(email):
            show_message("Email non valida. Controlla il formato.", "red")
        elif len(password) < 6:
            show_message("La password deve avere almeno 6 caratteri.", "red")
        elif is_email_registered(email):
            show_message("Email già registrata. Usa un'altra email.", "red")
        else:
            user_data = {"email": email, "password": password, "status": "user", "balance": 1000}
            try:
                if not os.path.exists(json_path):
                    with open(json_path, "w") as file:
                        json.dump([user_data], file, indent=4)
                else:
                    with open(json_path, "r+") as file:
                        users = json.load(file)
                        users.append(user_data)
                        file.seek(0)
                        json.dump(users, file, indent=4)
                show_message("Registrazione completata con successo!", "green")
                visitor_log_window.after(1500, lambda: new_visitor_window(visitor_log_window, email))
            except Exception as e:
                show_message(f"Errore durante la registrazione: {str(e)}", "red")

    def show_message(text, color):
        message_label.configure(text=text, text_color=color)
        message_label.place(relx=0.5, rely=0.825, anchor="center")

    # Buttons
    ctk.CTkButton(
        master=widget_frame,
        text="Login",
        width=300,
        font=("Helvetica", 14),
        fg_color="darkred",
        text_color="white",
        hover_color="#990000",
        command=login_user
    ).pack(pady=1)

    ctk.CTkLabel(master=widget_frame, text="or", font=("Helvetica", 14), text_color="gray").pack(pady=1)

    ctk.CTkButton(
        master=widget_frame,
        text="Sign Up",
        width=300,
        font=("Helvetica", 14),
        fg_color="blue",
        text_color="white",
        hover_color="#000099",
        command=register_user
    ).pack(pady=1)


# ----------------------- APP MAIN -----------------------

if __name__ == '__main__':  
    registration_status = [False]
    window_visitorLog = ctk.CTk()
    window_visitorLog.title("Casinò Scienere - Visitor Sign Up/Login")
    window_visitorLog.resizable(False, False)
    window_visitorLog.geometry(window_login_geometry(window_visitorLog))

    frame_image = frame_imagine_log(window_visitorLog)
    frame_log = frame_label_log(window_visitorLog)

    image_side(frame_image)
    create_login(frame_log, window_visitorLog, registration_status)

    window_visitorLog.mainloop()
