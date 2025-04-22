import customtkinter as ctk
import pygame
import random
from PIL import Image
import threading
import time
import os
from customtkinter import CTkImage
import json
import tkinter.messagebox as msgbox

# Importa la variabile globale per il saldo delle monete dal main
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'login_and_main')))
from coin_manager import get_balance, remove_coins

# Ottieni il saldo iniziale delle monete con gestione dell'errore
try:
    coin_balance = get_balance()
except ValueError as e:
    msgbox.showerror("Errore", str(e))
    sys.exit()

# Variabile per la scommessa selezionata
selected_bet = 1

# Init Pygame
pygame.init()
pygame.mixer.init()

# Paths
pathFile = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(pathFile, "./immagini")

# Sounds
spin_sound = pygame.mixer.Sound(os.path.join(pathFile, "spin.mp3"))
win_sound = pygame.mixer.Sound(os.path.join(pathFile, "win.mp3"))
spin_sound.set_volume(0.5)
win_sound.set_volume(0.5)

# Load image symbols
symbol_files = ["cherry.png", "bell.png", "lemon.png", "star.png", "watermelon.png", "seven.png", "diamond.png"]
symbols_images = [Image.open(os.path.join(images_path, f)).resize((60, 60)) for f in symbol_files]
symbols = [CTkImage(light_image=img, size=(60, 60)) for img in symbols_images]

# UI setup
root = ctk.CTk()
root.title("Slot Machine")
root.geometry("800x600")
ctk.set_appearance_mode("dark")

# Main frame (using grid for both reels and lever)
main_frame = ctk.CTkFrame(root)
main_frame.grid(row=0, column=0, padx=20, pady=20)

# Reels frame
reels_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
reels_frame.grid(row=0, column=0, padx=20)

# Reel containers
reels = []
reel_values = []
for i in range(5):
    frame = ctk.CTkFrame(reels_frame, fg_color="white", border_color="black", border_width=3, width=80, height=100)
    frame.pack_propagate(False)
    frame.grid(row=0, column=i, padx=10)
    symbol = random.choice(symbols)
    label = ctk.CTkLabel(frame, text="", image=symbol, text_color="black")
    label.pack(expand=True)
    reels.append(label)
    reel_values.append(symbol)

# Coin display
coin_frame = ctk.CTkFrame(root, fg_color="black", corner_radius=10, border_width=2, border_color="gold")
coin_frame.place(relx=0.95, rely=0.05, anchor="ne")
coin_label = ctk.CTkLabel(coin_frame, text=f"\U0001F4B0 {coin_balance}", font=("Helvetica", 18, "bold"), text_color="gold")
coin_label.pack(padx=10, pady=5)

def update_coin_label():
    coin_label.configure(text=f"\U0001F4B0 {coin_balance}")

# Result label
result_label = ctk.CTkLabel(root, text="", font=("Arial", 20))
result_label.grid(row=1, column=0, pady=10)

# Bet selection
bet_frame = ctk.CTkFrame(root)
bet_frame.place(relx=0.5, rely=0.92, anchor="center")

bet_label = ctk.CTkLabel(bet_frame, text="Scommessa: 1", font=("Helvetica", 14))
bet_label.pack(side="left", padx=(0, 10))

def set_bet(amount):
    global selected_bet
    selected_bet = amount
    bet_label.configure(text=f"Scommessa: {amount}")

for amount in [1, 10, 25, 50, 100]:
    btn = ctk.CTkButton(bet_frame, text=str(amount), width=40, command=lambda a=amount: set_bet(a))
    btn.pack(side="left", padx=5)

# Global spin state
running = False

def spin_reels():
    global running, coin_balance, selected_bet

    if running:
        return

    if coin_balance < selected_bet:
        msgbox.showwarning("Saldo insufficiente", "Non hai abbastanza monete per questa scommessa.")
        return

    coin_balance -= selected_bet
    update_coin_label()

    running = True
    spin_sound.play(0, 0)

    spins = [random.randint(10, 20) for _ in range(5)]
    stop_times = [1, 2, 3, 4, 5]

    def stop_reel(index, delay):
        time.sleep(delay)
        spins[index] = 0

    for i in range(5):
        threading.Thread(target=stop_reel, args=(i, stop_times[i]), daemon=True).start()

    while any(spins):
        for i in range(5):
            if spins[i] > 0:
                symbol = random.choice(symbols)
                reels[i].configure(image=symbol)
                reel_values[i] = symbol
        time.sleep(0.1)

    running = False
    check_win()

def check_win():
    global coin_balance, selected_bet
    spin_sound.stop()

    won = False
    multiplier = 3

    if all(symbol == reel_values[0] for symbol in reel_values):
        result_label.configure(text="🎉 JACKPOT! 🎉", text_color="green")
        coin_balance += selected_bet * multiplier
        won = True
    elif reel_values[1] == reel_values[2] == reel_values[3]:
        result_label.configure(text="🎉 3 SIMBOLI CENTRALI! 🎉", text_color="green")
        coin_balance += selected_bet * multiplier
        won = True
    elif reel_values[0] == reel_values[4]:
        result_label.configure(text="🎉 ESTERNI UGUALI! 🎉", text_color="green")
        coin_balance += selected_bet * multiplier
        won = True
    else:
        result_label.configure(text="Riprova!", text_color="red")

    if won:
        pygame.mixer.Sound.play(win_sound)
        update_coin_label()

    remove_coins(coin_balance)
    reset_lever()

# Lever behavior
def lever_pulled(event):
    threading.Thread(target=spin_reels, daemon=True).start()

def reset_lever():
    lever.set(100)

# Lever (slider)
lever_frame = ctk.CTkFrame(main_frame)
lever_frame.grid(row=0, column=1, padx=20, pady=20)

lever = ctk.CTkSlider(lever_frame, from_=0, to=100, command=lever_pulled, orientation="vertical")
lever.pack(expand=True, fill="y")

# Main loop
root.mainloop()
