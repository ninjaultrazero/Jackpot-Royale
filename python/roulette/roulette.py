import tkinter as tk
from tkinter import messagebox
import random
import os
import pygame
from PIL import Image, ImageTk
import json
import sys

pathFile = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'login_and_main')))
from coin_manager import get_balance, remove_coins
ctk.set_appearance_mode("dark")
saldo = get_balance()
pygame.mixer.init()
roulette_numbers = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6,
    27, 13, 36, 11, 30, 8, 23, 10, 5, 24,
    16, 33, 1, 20, 14, 31, 9, 22, 18, 29,
    7, 28, 12, 35, 3, 26
]
black_numbers = {15, 4, 2, 17, 6, 13, 11, 8, 10, 24, 33, 20, 31, 22, 29, 28, 35, 26}
red_numbers = {32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3}

def play_sound():
    sound_path = os.path.join(pathFile, "suono.mp3")
    if os.path.exists(sound_path):
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    else:
        messagebox.showwarning("Attenzione", "Suono non trovato. Il gioco continuer\u00e0 senza audio.")

root = tk.Tk()
root.title("Roulette Game")
root.geometry("1280x800")
root.configure(bg="black")

main_frame = tk.Frame(root, bg="black")
main_frame.pack(fill="both", expand=True)

left_frame = tk.Frame(main_frame, bg="black")
left_frame.pack(side="left", padx=20, pady=20)

canvas = tk.Canvas(left_frame, width=400, height=400, bg="green")
canvas.pack()

roulette_display = None
original_image = None
resized_image = None
roulette_img = None

image_path = os.path.join(pathFile, "ruota.png")
if os.path.exists(image_path):
    original_image = Image.open(image_path)
    resized_image = original_image.resize((300, 300), Image.LANCZOS)
    roulette_img = ImageTk.PhotoImage(resized_image)
    roulette_display = canvas.create_image(200, 200, image=roulette_img)
else:
    messagebox.showwarning("Attenzione", "Immagine della roulette non trovata.")

details_frame = tk.Frame(main_frame, bg="black")
details_frame.pack(side="top", padx=20, pady=20)

puntata = 0

saldo_label = tk.Label(details_frame, text=f"Saldo: {saldo} FUN", font=("Helvetica", 16), fg="white", bg="black")
saldo_label.pack()

puntata_label = tk.Label(details_frame, text=f"Puntata totale: {puntata} FUN", font=("Helvetica", 16), fg="white", bg="black")
puntata_label.pack()

bet_frame = tk.Frame(left_frame, bg="black")
bet_frame.pack(pady=10)

bet_options = [1, 5, 10, 25, 50, 100]
selected_bet = tk.IntVar(value=bet_options[0])

for bet in bet_options:
    bet_button = tk.Button(bet_frame, text=f"{bet} FUN", width=6, bg="gray", fg="white", command=lambda b=bet: selected_bet.set(b))
    bet_button.pack(side="left", padx=5)

right_frame = tk.Frame(main_frame, bg="black")
right_frame.pack(side="right", padx=20, pady=20)

table_frame = tk.Frame(right_frame, bg="black")
table_frame.pack()

selected_numbers = {}

number_buttons = []

# Add 0 first as a large button
zero_button = tk.Button(table_frame, text="0", width=6, height=6, bg="green", fg="white", command=lambda: place_bet(0))
zero_button.grid(row=0, column=0, rowspan=3, padx=5, pady=5)
number_buttons.append(zero_button)

def place_bet(num):
    global selected_numbers, saldo, puntata
    bet_amount = selected_bet.get()
    if len(selected_numbers) < 17:
        if saldo >= bet_amount:
            saldo -= bet_amount
            puntata += bet_amount
            selected_numbers[num] = selected_numbers.get(num, 0) + bet_amount
            saldo_label.config(text=f"Saldo: {saldo} FUN")
            puntata_label.config(text=f"Puntata totale: {puntata} FUN")
            for btn in number_buttons:
                if btn["text"] == str(num):
                    btn.config(bg="green")
                    btn.config(state="disabled")
        else:
            messagebox.showwarning("Saldo Insufficiente", "Non hai abbastanza FUN per piazzare questa puntata!")

# Add numbers 1-36 in classic roulette layout
layout = [
    [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
    [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
    [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
]

for row_index, row in enumerate(layout):
    for col_index, num in enumerate(row):
        color = "red" if num in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else "black"
        btn = tk.Button(table_frame, text=str(num), width=4, height=2, bg=color, fg="white", command=lambda n=num: place_bet(n))
        btn.grid(row=row_index, column=col_index+1, padx=2, pady=2)
        number_buttons.append(btn)
special_bets_frame_top = tk.Frame(right_frame, bg="black")
special_bets_frame_top.pack(pady=10)

special_bets_frame_bottom = tk.Frame(right_frame, bg="black")
special_bets_frame_bottom.pack(pady=10)

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

def gira_ruota():
	play_sound()
	rotate_roulette()
	numero = random.choice(roulette_numbers)
	root.after(5000, lambda: numero_uscito_label.config(text=f"Numero uscito: {numero}"))
	root.after(5000, lambda: check_winnings(numero))

def check_winnings(num):
	global saldo, puntata, selected_numbers, selected_red, selected_black, selected_even, selected_odd, selected_low, selected_high
	vincita_totale = 0

	if num in selected_numbers:
		vincita_totale += selected_numbers[num] * 35

	if num != 0:
		if num in red_numbers:
			vincita_totale += selected_red.get() * 2
			
		elif num in black_numbers:
			vincita_totale += selected_black.get() * 2

		if num % 2 == 0:
			vincita_totale += selected_even.get() * 2
		else:
			vincita_totale += selected_odd.get() * 2

		if 1 <= num <= 18:
			vincita_totale += selected_low.get() * 2
		elif 19 <= num <= 36:
			vincita_totale += selected_high.get() * 2

	if vincita_totale > 0:
		saldo += vincita_totale
		risultato_label.config(text=f"Vincita! Hai vinto {vincita_totale} FUN!", fg="yellow")
		remove_coins(saldo+vincita_totale)
	else:
		risultato_label.config(text="Sconfitta! Non hai vinto questa volta!", fg="red")

	remove_coins(saldo)
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

	for btn in number_buttons:
		num = int(btn["text"])
		btn.config(bg="green" if num == 0 else ("red" if num in red_numbers else "black"))
		btn.config(state="active")

	red_button.config(bg="red")
	black_button.config(bg="black")
	even_button.config(bg="gray")
	odd_button.config(bg="gray")
	low_button.config(bg="gray")
	high_button.config(bg="gray")

button_frame = tk.Frame(left_frame, bg="black")
button_frame.pack(pady=10)

gira_button = tk.Button(button_frame, text="Gira", command=gira_ruota, width=10, bg="gold")
gira_button.pack(side="left", padx=10)

numero_uscito_label = tk.Label(left_frame, text="Numero uscito: ", font=("Helvetica", 16), fg="white", bg="black")
numero_uscito_label.pack()

risultato_label = tk.Label(right_frame, text="", font=("Helvetica", 16), fg="white", bg="black")
risultato_label.pack(side="bottom", pady=10)

def avvia_roulette():
    roulette_path = os.path.join(os.path.dirname(__file__), "..", "roulette_game", "roulette.py")
    os.execl(sys.executable, sys.executable, roulette_path)

def torna_alla_home():
    main_path = os.path.join(pathFile, "..", "login_and_main", "main.py")
    os.execl(sys.executable, sys.executable, main_path)


home_button = tk.Button(button_frame, text="Torna alla Home", command=torna_alla_home, width=15, bg="gray", fg="white")
home_button.pack(side="left", padx=10)
root.mainloop()
