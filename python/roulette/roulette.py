import tkinter as tk
from tkinter import messagebox
import random
import os
import pygame
from PIL import Image, ImageTk
import json

pathFile = os.path.dirname(os.path.abspath(__file__))  # Percorso della cartella corrente
# Funzione per leggere il saldo dal file JSON
def get_balance():
	with open('users.json', 'r') as file:
		data = json.load(file)
		return data.get('balance', 0)
# Funzione per aggiornare il saldo nel file JSON
def update_balance(new_balance):
	with open('users.json', 'r+') as file:
		data = json.load(file)
		data['balance'] = new_balance
		file.seek(0)
		json.dump(data, file, indent=4)
		file.truncate()
coin_balance = get_balance()  # Leggi il saldo iniziale

# Inizializza Pygame per il suono
pygame.mixer.init()

def play_sound():
	sound_path = os.path.join(pathFile, "suono.mp3")  # Assicurati di avere un file audio adeguato
	if os.path.exists(sound_path):
		pygame.mixer.music.load(sound_path)
		pygame.mixer.music.play()
	else:
		messagebox.showwarning("Attenzione", "Suono non trovato. Il gioco continuerà senza audio.")

# Finestra principale
root = tk.Tk()
root.title("Roulette Game")
root.geometry("1280x800")
root.configure(bg="black")

# Contenitore principale
main_frame = tk.Frame(root, bg="black")
main_frame.pack(fill="both", expand=True)

# Tavolo da gioco e tabella
left_frame = tk.Frame(main_frame, bg="black")
left_frame.pack(side="left", padx=20, pady=20)

# Tavolo da gioco (Roulette)
canvas = tk.Canvas(left_frame, width=400, height=400, bg="green")
canvas.pack()

# Variabili globali
roulette_display = None
original_image = None
resized_image = None
roulette_img = None

# Caricamento immagine della roulette e ridimensionamento

image_path = os.path.join(pathFile, "ruota.png")
if os.path.exists(image_path):
	original_image = Image.open(image_path)
	resized_image = original_image.resize((300, 300), Image.LANCZOS)
	roulette_img = ImageTk.PhotoImage(resized_image)
	roulette_display = canvas.create_image(200, 200, image=roulette_img)
else:
	messagebox.showwarning("Attenzione", "Immagine della roulette non trovata. Il gioco continuerà senza di essa.")

# Sezione saldo e puntate (spostata in alto a destra)
details_frame = tk.Frame(main_frame, bg="black")
details_frame.pack(side="top", padx=20, pady=20)

# Importa la variabile globale per il saldo delle monete


saldo = coin_balance
puntata = 0

saldo_label = tk.Label(details_frame, text=f"Saldo: {saldo} FUN", font=("Helvetica", 16), fg="white", bg="black")
saldo_label.pack()

puntata_label = tk.Label(details_frame, text=f"Puntata totale: {puntata} FUN", font=("Helvetica", 16), fg="white", bg="black")
puntata_label.pack()

# Sezione selezione puntata (fiches)
bet_frame = tk.Frame(left_frame, bg="black")
bet_frame.pack(pady=10)

bet_options = [1, 5, 10, 25, 50, 100]
selected_bet = tk.IntVar(value=bet_options[0])

for bet in bet_options:
	bet_button = tk.Button(bet_frame, text=f"{bet} FUN", width=6, bg="gray", fg="white",
						   command=lambda b=bet: selected_bet.set(b))
	bet_button.pack(side="left", padx=5)

# Creazione tabellone numerico
right_frame = tk.Frame(main_frame, bg="black")
right_frame.pack(side="right", padx=20, pady=20)

table_frame = tk.Frame(right_frame, bg="black")
table_frame.pack()

selected_numbers = {}

def place_bet(num):
	global selected_numbers, saldo, puntata
	bet_amount = selected_bet.get()
	if len(selected_numbers)<17:
		if saldo >= bet_amount:
			saldo -= bet_amount
			puntata += bet_amount
			selected_numbers[num] = selected_numbers.get(num, 0) + bet_amount
			saldo_label.config(text=f"Saldo: {saldo} FUN")
			puntata_label.config(text=f"Puntata totale: {puntata} FUN")
			# Evidenzia il bottone selezionato
			for btn in number_buttons:
				if btn["text"] == str(num):
					btn.config(bg="green")
					btn.config(state="disabled")
	else:
		messagebox.showwarning("Saldo Insufficiente", "Non hai abbastanza FUN per piazzare questa puntata!")

# Creazione bottoni per i numeri della roulette
number_buttons = []
for i in range(3):
	for j in range(12):
		num = i * 12 + j
		if num > 36:
			break
		btn = tk.Button(table_frame, text=str(num), width=4, height=2, bg="red" if num % 2 else "black", fg="white",
						 command=lambda n=num: place_bet(n))
		btn.grid(row=i, column=j, padx=2, pady=2)
		number_buttons.append(btn)

# Aggiunta bottoni per scommesse speciali
special_bets_frame_top = tk.Frame(right_frame, bg="black")
special_bets_frame_top.pack(pady=10)

special_bets_frame_bottom = tk.Frame(right_frame, bg="black")
special_bets_frame_bottom.pack(pady=10)

# Variabili per le scommesse speciali
selected_red = tk.IntVar(value=0)
selected_black = tk.IntVar(value=0)
selected_even = tk.IntVar(value=0)
selected_odd = tk.IntVar(value=0)
selected_low = tk.IntVar(value=0)
selected_high = tk.IntVar(value=0)

def place_special_bet(bet_type):
	global saldo, puntata
	bet_amount = selected_bet.get()
	if saldo >= bet_amount:
		saldo -= bet_amount
		puntata += bet_amount
		if bet_type == "red":
			selected_red.set(selected_red.get() + bet_amount)
			red_button.config(bg="green")
		elif bet_type == "black":
			selected_black.set(selected_black.get() + bet_amount)
			black_button.config(bg="green")
		elif bet_type == "even":
			selected_even.set(selected_even.get() + bet_amount)
			even_button.config(bg="green")
		elif bet_type == "odd":
			selected_odd.set(selected_odd.get() + bet_amount)
			odd_button.config(bg="green")
		elif bet_type == "low":
			selected_low.set(selected_low.get() + bet_amount)
			low_button.config(bg="green")
		elif bet_type == "high":
			selected_high.set(selected_high.get() + bet_amount)
			high_button.config(bg="green")
		saldo_label.config(text=f"Saldo: {saldo} FUN")
		puntata_label.config(text=f"Puntata totale: {puntata} FUN")
	else:
		messagebox.showwarning("Saldo Insufficiente", "Non hai abbastanza FUN per piazzare questa puntata!")

# Bottoni per scommesse speciali
red_button = tk.Button(special_bets_frame_top, text="Rosso", width=10, bg="red", fg="white", command=lambda: place_special_bet("red"))
red_button.pack(side="left", padx=5)

black_button = tk.Button(special_bets_frame_top, text="Nero", width=10, bg="black", fg="white", command=lambda: place_special_bet("black"))
black_button.pack(side="left", padx=5)

even_button = tk.Button(special_bets_frame_top, text="Pari", width=10, bg="gray", fg="white", command=lambda: place_special_bet("even"))
even_button.pack(side="left", padx=5)

odd_button = tk.Button(special_bets_frame_bottom, text="Dispari", width=10, bg="gray", fg="white", command=lambda: place_special_bet("odd"))
odd_button.pack(side="left", padx=5)

low_button = tk.Button(special_bets_frame_bottom, text="1-18", width=10, bg="gray", fg="white", command=lambda: place_special_bet("low"))
low_button.pack(side="left", padx=5)

high_button = tk.Button(special_bets_frame_bottom, text="19-36", width=10, bg="gray", fg="white", command=lambda: place_special_bet("high"))
high_button.pack(side="left", padx=5)

# Effetto di rotazione della roulette senza ingrandimento
from PIL import Image  
BICUBIC = Image.Resampling.BICUBIC  

def rotate_roulette(angle=0, speed=50):
	global roulette_img, resized_image
	if roulette_display is None or resized_image is None:
		return
	if speed <= 0:
		return

	rotated_image = resized_image.rotate(angle, resample=BICUBIC, expand=False)
	roulette_img = ImageTk.PhotoImage(rotated_image)
	canvas.itemconfig(roulette_display, image=roulette_img)

	new_speed = max(speed - 1, 0)
	root.after(50, lambda: rotate_roulette(angle + new_speed, new_speed))

# Funzione per girare la ruota con animazione
def gira_ruota():
	play_sound()
	rotate_roulette()
	numero = random.randint(0, 36)
	root.after(5000, lambda: numero_uscito_label.config(text=f"Numero uscito: {numero}"))
	root.after(5000, lambda: check_winnings(numero))

# Controllo vincite
def check_winnings(num):
	global saldo, puntata, selected_numbers, selected_red, selected_black, selected_even, selected_odd, selected_low, selected_high
	vincita_totale = 0

	# Controllo vincite sui numeri
	if num in selected_numbers:
		vincita_totale += selected_numbers[num] * 35

	# Controllo vincite su rosso/nero
	if (num != 0 and num % 2 == 1 and selected_red.get() > 0) or (num != 0 and num % 2 == 0 and selected_black.get() > 0):
		vincita_totale += selected_red.get() * 2 if num % 2 == 1 else selected_black.get() * 2

	# Controllo vincite su pari/dispari
	if (num != 0 and num % 2 == 0 and selected_even.get() > 0) or (num != 0 and num % 2 == 1 and selected_odd.get() > 0):
		vincita_totale += selected_even.get() * 2 if num % 2 == 0 else selected_odd.get() * 2

	# Controllo vincite su metà numeri
	if (num >= 1 and num <= 18 and selected_low.get() > 0) or (num >= 19 and num <= 36 and selected_high.get() > 0):
		vincita_totale += selected_low.get() * 2 if num <= 18 else selected_high.get() * 2

	if vincita_totale > 0:
		saldo += vincita_totale
		risultato_label.config(text=f"Vincita! Hai vinto {vincita_totale} FUN!", fg="yellow")
	else:
		risultato_label.config(text="Sconfitta! Non hai vinto questa volta!", fg="red")

	# Reset delle scommesse
	puntata = 0
	selected_numbers = {}
	selected_red.set(0)
	selected_black.set(0)
	selected_even.set(0)
	selected_odd.set(0)
	selected_low.set(0)
	selected_high.set(0)
	saldo_label.config(text=f"Saldo: {saldo} FUN")
	puntata_label.config(text=f"Puntata totale: {puntata} FUN")
	# Ripristina il colore dei bottoni
	for btn in number_buttons:
		num = int(btn["text"])
		btn.config(bg="red" if num % 2 else "black")
	red_button.config(bg="red")
	black_button.config(bg="black")
	even_button.config(bg="gray")
	odd_button.config(bg="gray")
	low_button.config(bg="gray")
	high_button.config(bg="gray")

	for btn in number_buttons:
		btn.config(state="active")
		

# Pulsanti di controllo
button_frame = tk.Frame(left_frame, bg="black")
button_frame.pack(pady=10)

gira_button = tk.Button(button_frame, text="Gira", command=gira_ruota, width=10, bg="gold")
gira_button.pack(side="left", padx=10)

# Label per il numero uscito (a sinistra)
numero_uscito_label = tk.Label(left_frame, text="Numero uscito: ", font=("Helvetica", 16), fg="white", bg="black")
numero_uscito_label.pack()

# Label per il risultato (a destra, sotto i bottoni speciali)
risultato_label = tk.Label(right_frame, text="", font=("Helvetica", 16), fg="white", bg="black")
risultato_label.pack(side="bottom", pady=10)

# Avvia il loop principale
root.mainloop()