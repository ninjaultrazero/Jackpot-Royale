import customtkinter as ctk
import re
import json
import os
from PIL import Image, ImageTk
from main import start_casino  # Importa la funzione per avviare il casinò
pathFile = os.path.dirname(os.path.abspath(__file__))  # Percorso della cartella corrente
json_path = os.path.join(pathFile, "users.json") 
print(json_path)
# Dimensioni finestra Login/Sign Up
def window_login_geometry(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 900
    window_height = 600
    x_cordinate = (screen_width - window_width) // 2
    y_cordinate = (screen_height - window_height) // 2
    return f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}"

def image_label_logo(root):
    frame = ctk.CTkFrame(root, height=200, width=200, fg_color="transparent")
    frame.pack(pady=20)
    
    img_path =os.path.join(pathFile, "./immagini/scienere.jpeg") 
    print(img_path)
    image = Image.open(img_path)
    image = image.resize((200, 200))
    photo = ImageTk.PhotoImage(image)

    img_label = ctk.CTkLabel(frame, image=photo, text="")
    img_label.photo = photo
    img_label.pack()

def frame_imagine_log(root):
    frame = ctk.CTkFrame(
        master=root,
        fg_color="green",
        width=500,
        height=600,
        corner_radius=0
    )
    frame.place(relx=0, rely=0)
    return frame

def frame_label_log(root):
    frame = ctk.CTkFrame(
        master=root,
        fg_color="transparent",
        width=500,
        height=600,
        corner_radius=0
    )
    frame.place(relx=0.5, rely=0)
    return frame

def create_login(root, visitor_log_window, registration_status):
    label = ctk.CTkLabel(
        master=root,
        text_color="gold",
        text="Welcome",
        font=("Helvetica", 30, "bold"),
    )
    label.place(relx=0.5, rely=0.15, anchor="center")
    
    widget_frame = ctk.CTkFrame(master=root, fg_color="transparent")
    widget_frame.place(relx=0.1, rely=0.225)

    label_email = ctk.CTkLabel(
        master=widget_frame,
        text_color="gold",
        text="📧 Email",
        font=("Helvetica", 14, "bold")
    )
    label_email.place(relx=0)
    
    email_entry = ctk.CTkEntry(
        master=widget_frame,
        placeholder_text="Email",
        width=300,
        font=("Helvetica", 14)
    )
    email_entry.pack(pady=(30, 30))
    
    label_password = ctk.CTkLabel(
        master=widget_frame,
        text_color="gold",
        text="🔑 Password",
        font=("Helvetica", 14, "bold")
    )
    label_password.place(relx=0, rely=0.25)

    password_entry = ctk.CTkEntry(
        master=widget_frame,
        placeholder_text="Password",
        width=300,
        font=("Helvetica", 14),
        show="*",
    )
    password_entry.pack(pady=5)
    
    def toggle_password_visibility():
        if show_password_var.get():
            password_entry.configure(show="") 
        else:
            password_entry.configure(show="*")

    show_password_var = ctk.BooleanVar(value=False)

    show_password_checkbox = ctk.CTkCheckBox(
        master=widget_frame,
        text="Mostra Password",
        variable=show_password_var,
        command=toggle_password_visibility,
        font=("Helvetica", 12),
        text_color="gray"
    )
    show_password_checkbox.pack(pady=10)

    message_label = ctk.CTkLabel(master=root, text_color="red", font=("Helvetica", 12))
    message_label.place(relx=0.5, rely=0.825, anchor="center")
    message_label.place_forget()
    
    def new_visitor_window(current_window):
        current_window.destroy()  # Chiudi la finestra di login
        registration_status[0] = True
        start_casino()  # Avvia la finestra principale del casinò
    
    def is_valid_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email)
    
    def login_user():
        email = email_entry.get()
        password = password_entry.get()

        if not email or not password:
            message_label.configure(text="Inserisci email e password.", text_color="red")
            message_label.place(relx=0.5, rely=0.825, anchor="center")
            return
        elif not is_valid_email(email):
            message_label.configure(text="Email non valida. Controlla il formato.", text_color="red")
            message_label.place(relx=0.5, rely=0.825, anchor="center")
            return

        try:
            with open("users.json", "r") as file:
                users = json.load(file)
                login_successful = False

                for user in users:
                    if user["email"] == email and user["password"] == password and user["status"] == "user":
                        login_successful = True
                        message_label.configure(text="Login effettuato con successo!", text_color="green")
                        message_label.place(relx=0.5, rely=0.825, anchor="center")
                        visitor_log_window.after(1500, lambda: new_visitor_window(visitor_log_window))
                        break
                
                if not login_successful:
                    message_label.configure(text="Email o password errata.", text_color="red")
                    message_label.place(relx=0.5, rely=0.825, anchor="center")
        except json.JSONDecodeError:
            message_label.configure(text="Errore nel file utenti.", text_color="red")
            message_label.place(relx=0.5, rely=0.825, anchor="center")
    
    login_button = ctk.CTkButton(
        master=widget_frame,
        text="Login",
        width=300,
        font=("Helvetica", 14),
        fg_color="darkred",
        text_color="white",
        hover_color="#990000",
        command=login_user
    )
    login_button.pack(pady=1)

    divider = ctk.CTkLabel(
        master=widget_frame,
        text="or",
        font=("Helvetica", 14),
        text_color="gray"
    )
    divider.pack(pady=1)

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

    def register_user():
        email = email_entry.get()
        password = password_entry.get()

        if not email or not password:
            message_label.configure(text="Inserisci email e password", text_color="red")
            message_label.place(relx=0.5, rely=0.825, anchor="center")
            return  
        elif not is_valid_email(email):
            message_label.configure(text="Email non valida. Controlla il formato.", text_color="red")
            message_label.place(relx=0.5, rely=0.825, anchor="center")
            return
        elif is_email_registered(email):
            message_label.configure(text="Email già registrata. Usa un'altra email.", text_color="red")
            message_label.place(relx=0.5, rely=0.825, anchor="center")
            return
        
        user_data = {"email": email, "password": password, "status": "user"}
        try:
            if not os.path.exists(json_path):
                with open("users.json", "w") as file:
                    json.dump([user_data], file, indent=4)
            else:
                with open("users.json", "r+") as file:
                    users = json.load(file)
                    users.append(user_data)
                    file.seek(0)
                    json.dump(users, file, indent=4)
            message_label.configure(text="Registrazione completata con successo!", text_color="green")
            message_label.place(relx=0.5, rely=0.825, anchor="center")
            visitor_log_window.after(1500, lambda: new_visitor_window(visitor_log_window))
        except Exception as e:
            message_label.configure(text=f"Errore durante la registrazione: {str(e)}", text_color="red")
            message_label.place(relx=0.5, rely=0.825, anchor="center")
    
    signup_button = ctk.CTkButton(
        master=widget_frame,
        text="Sign Up",
        width=300,
        font=("Helvetica", 14),
        fg_color="blue",
        text_color="white",
        hover_color="#000099",
        command=register_user
    )
    signup_button.pack(pady=1)
    
def image_side(frame):
    img_path =os.path.join(pathFile, "./immagini/scienere.jpeg") 
    image = Image.open(img_path)
    image = image.resize((500, 600))
    photo = ImageTk.PhotoImage(image)

    img_label = ctk.CTkLabel(frame, image=photo, text="")
    img_label.photo = photo
    img_label.pack(pady=0, padx=0)
        
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