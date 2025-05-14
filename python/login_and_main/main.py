import customtkinter as ctk
from PIL import Image, ImageTk
import os
import random
import sys

pathFile = os.path.dirname(os.path.abspath(__file__))
from coin_manager import get_balance

# Classe per l'animazione delle monete
class FallingCoin:
    def __init__(self, root):
        self.root = root
        self.coins = []
        self.speed = 5

    def create_coin(self):
        x = random.randint(0, self.root.winfo_width())
        y = 0
        coin_label = ctk.CTkLabel(self.root, text="💲", font=("Helvetica", 24), text_color="gold", bg_color="transparent")
        coin_label.place(x=x, y=y)
        self.coins.append((coin_label, x, y))

    def move_coins(self):
        for i in reversed(range(len(self.coins))):
            coin_label, x, y = self.coins[i]
            if y < self.root.winfo_height():
                y += self.speed
                coin_label.place(x=x, y=y)
                self.coins[i] = (coin_label, x, y)
            else:
                coin_label.destroy()
                self.coins.pop(i)
        self.root.after(26, self.move_coins)

    def start_coin_animation(self):
        self.create_coin()
        self.root.after(400, self.start_coin_animation)

# --- FUNZIONI PER APRIRE I GIOCHI (usano os.execl per chiudere main.py e avviare direttamente il gioco) ---
def apri_slot():
    slot_path = os.path.join(os.path.dirname(__file__), "..", "slot_machine", "slot.py")
    os.execl(sys.executable, sys.executable, slot_path)

def apri_blackjack():
    blackjack_path = os.path.join(os.path.dirname(__file__), "..", "black_jack", "blackJack.py")
    os.execl(sys.executable, sys.executable, blackjack_path)

def apri_roulette():
    roulette_path = os.path.join(os.path.dirname(__file__), "..", "roulette", "roulette.py")
    os.execl(sys.executable, sys.executable, roulette_path)

# --- FUNZIONE PRINCIPALE ---
def start_casino():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    root.geometry("1200x600")
    root.title("Scienere")
    root.state('zoomed')
    root.resizable(False, False)

    # Sfondo
    bg_image = ctk.CTkImage(
        light_image=Image.open(f"{pathFile}/immagini/casino_bg.png"),
        dark_image=Image.open(f"{pathFile}/immagini/casino_bg.png"),
        size=(1920, 1080)
    )
    bg_label = ctk.CTkLabel(root, image=bg_image, text="")
    bg_label.place(relwidth=1, relheight=1)

    # Titolo
    casino_name = ctk.CTkLabel(root, text="Scienere", font=("Helvetica", 36, "bold"), text_color="white")
    casino_name.pack(pady=20)

    # Coins
    coin_frame = ctk.CTkFrame(root, fg_color="black", corner_radius=10, border_width=2, border_color="gold")
    coin_frame.place(relx=0.95, rely=0.05, anchor="ne")
    coin_label = ctk.CTkLabel(coin_frame, text=f"💰 {get_balance()}", font=("Helvetica", 18, "bold"), text_color="gold")
    coin_label.pack(padx=10, pady=5)

    def update_coin_display():
        try:
            coin_label.configure(text=f"💰 {get_balance()}")
        except:
            coin_label.configure(text="💰 Errore")

    # Pulsanti giochi
    button_frame = ctk.CTkFrame(root, fg_color="gray", corner_radius=15, border_width=2, border_color="black")
    button_frame.pack(pady=100)

    def load_image(image_path):
        try:
            img = Image.open(image_path).resize((120, 120))
            return ctk.CTkImage(light_image=img, dark_image=img, size=(120, 120))
        except FileNotFoundError:
            print(f"Immagine {image_path} non trovata!")
            return None

    roulette_photo = load_image(f"{pathFile}/immagini/roulette.png")
    slot_photo = load_image(f"{pathFile}/immagini/slot.png")
    blackjack_photo = load_image(f"{pathFile}/immagini/jack.png")

    button_style = {
        "font": ("Helvetica", 16, "bold"),
        "text_color": "white",
        "fg_color": "gray",
        "corner_radius": 12,
        "hover_color": "#4d4d4d"
    }

    roulette_button = ctk.CTkButton(
        button_frame, image=roulette_photo, text="Roulette",
        **button_style, command=apri_roulette
    )
    roulette_button.grid(row=0, column=0, padx=15, pady=15)

    slot_button = ctk.CTkButton(
        button_frame, image=slot_photo, text="Slot Machine",
        **button_style, command=apri_slot
    )
    slot_button.grid(row=0, column=1, padx=15, pady=15)

    blackjack_button = ctk.CTkButton(
        button_frame, image=blackjack_photo, text="Blackjack",
        **button_style, command=apri_blackjack
    )
    blackjack_button.grid(row=0, column=2, padx=15, pady=15)

    # Animazione monete
    falling_coin = FallingCoin(root)
    falling_coin.move_coins()
    falling_coin.start_coin_animation()

    def periodic_refresh():
        update_coin_display()
        root.after(5000, periodic_refresh)

    periodic_refresh()
    root.mainloop()

# --- AVVIO ---
if __name__ == "__main__":
    start_casino()
