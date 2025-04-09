import customtkinter as ctk
import pygame
import random
from PIL import Image, ImageTk
import threading
import time
import os

# Configura Pygame per l'animazione e i suoni
pygame.init()
pygame.mixer.init()

pathFile = os.path.dirname(os.path.abspath(__file__))  # Percorso della cartella corrente
# Carica i suoni
spin_sound = pygame.mixer.Sound(os.path.join(pathFile, "spin.mp3"))  # Aggiungi un file audio
win_sound = pygame.mixer.Sound(os.path.join(pathFile, "win.mp3"))  # Aggiungi un file audio

# Simboli della slot machine
symbols = ["🍒", "🔔", "🍋", "⭐", "🍉", "7", "💎"]

# Creazione della finestra principale
root = ctk.CTk()
root.title("Slot Machine")
root.geometry("600x400")
ctk.set_appearance_mode("dark")
# Frame principale
frame = ctk.CTkFrame(root)
frame.pack(pady=20)

# Creazione dei rulli
reels = [ctk.CTkLabel(frame, text=random.choice(symbols), font=("Arial", 50)) for _ in range(5)]
for reel in reels:
	reel.pack(side="left", padx=10)

# Funzione per far girare i rulli con animazione
running = False

def spin_reels():
    global running
    running = True
    spin_sound.play(0,10)  # Loop the spin sound

    # Number of rotations for each reel (they should all have enough rotations for a smooth animation)
    spins = [random.randint(10, 20) for _ in range(5)]  
    
    # Time delays for each reel to stop (first stops at 0.5s, second at 1.0s, etc.)
    stop_times = [1, 3, 4, 5, 7]  # Times when each reel will stop (in seconds)

    # Function to stop the reel after a certain delay
    def stop_reel(index, delay):
        time.sleep(delay)  # Wait for the specified time before stopping the reel
        spins[index] = 0  # Stop this reel

    # Start spinning all reels simultaneously
    for i in range(5):
        threading.Thread(target=stop_reel, args=(i, stop_times[i]), daemon=True).start()

    # Spin the reels until they stop
    while any(spins):  # Continue spinning until all reels stop
        for i in range(5):
            if spins[i] > 0:
                reels[i].configure(text=random.choice(symbols))  # Update the reel with a random symbol
        time.sleep(0.1)  # Slower speed for the rotation

    running = False
    check_win()

# Funzione per controllare la vittoria
def check_win():
	spin_sound.stop()  # Stop the spin sound	
	symbols_on_reels = [reel.cget("text") for reel in reels]
	
	# 1. 5 simboli uguali
	if symbols_on_reels.count(symbols_on_reels[0]) == 5:
		pygame.mixer.Sound.play(win_sound)
		result_label.configure(text="🎉 HAI VINTO! 🎉", text_color="green")
	
	# 2. 3 simboli uguali sui 3 rulli centrali
	elif symbols_on_reels[1] == symbols_on_reels[2] == symbols_on_reels[3]:
		pygame.mixer.Sound.play(win_sound)
		result_label.configure(text="🎉 Combinazione vincente sui 3 rulli centrali! 🎉", text_color="green")
	
	# 3. 2 simboli uguali sui rulli esterni
	elif symbols_on_reels[0] == symbols_on_reels[4]:
		pygame.mixer.Sound.play(win_sound)
		result_label.configure(text="🎉 Combinazione vincente sui rulli esterni! 🎉", text_color="green")
	
	# 4. Combinazione di simboli speciali (ad esempio "7" e "🍒")
	elif symbols_on_reels[0] == "7" and symbols_on_reels[4] == "🍒":
		pygame.mixer.Sound.play(win_sound)
		result_label.configure(text="🎉 Combinazione vincente!7 e 🍒! 🎉", text_color="green")
	
	# Se non c'è nessuna combinazione vincente
	else:
		result_label.configure(text="Riprova!", text_color="red")
	
	switch.configure(state="normal")
	switch.deselect()

# Funzione per avviare la slot machine
def start_spin():
	switch.configure(state="disabled")
	if not running:
		result_label.configure(text="")
		threading.Thread(target=spin_reels, daemon=True).start()

# Bottone per avviare la slot machine
spin_button = ctk.CTkButton(root, text="SPIN", command=start_spin)
spin_button.pack(pady=20)

# Etichetta per mostrare il risultato
result_label = ctk.CTkLabel(root, text="", font=("Arial", 20))
result_label.pack(pady=10)

switch_var = ctk.StringVar(value="off")
switch = ctk.CTkSwitch(root, text="Gira", command=start_spin,variable=switch_var, onvalue="on", offvalue="off")
switch.pack(pady=20)

# Avvia l'app
root.mainloop()
