import customtkinter as ctk
from PIL import Image, ImageTk
import os
import random
import subprocess
pathFile = os.path.dirname(os.path.abspath(__file__))  # Percorso della cartella corrente

# Classe per l'animazione delle monete che cadono
class FallingCoin:
	def __init__(self, root):
		self.root = root
		self.coins = []
		self.speed = 5  # Velocità di caduta delle monete

	def create_coin(self):
		x = random.randint(0, self.root.winfo_width())  # Posizione casuale sull'asse X
		y = 0  # Inizia dall'alto
		coin_label = ctk.CTkLabel(self.root, text="💰", font=("Helvetica", 24), text_color="gold", bg_color="transparent")
		coin_label.place(x=x, y=y)
		self.coins.append((coin_label, x, y))

	def move_coins(self):
		for i, (coin_label, x, y) in enumerate(self.coins):
			if y < self.root.winfo_height():  # Se la moneta non ha raggiunto il fondo
				y += self.speed  # Muovi la moneta verso il basso
				coin_label.place(x=x, y=y)
				self.coins[i] = (coin_label, x, y)
			else:
				coin_label.destroy()  # Rimuovi la moneta quando raggiunge il fondo
				self.coins.pop(i)
		self.root.after(50, self.move_coins)  # Richiama la funzione ogni 50ms

	def start_coin_animation(self):
		self.create_coin()  # Crea una nuova moneta
		self.root.after(1000, self.start_coin_animation)  # Crea una nuova moneta ogni secondo
		self.move_coins()  # Avvia il movimento delle monete

def open_roulette_window():
	roulette_path=os.path.join(pathFile, "../roulette/roulette.py")
	subprocess.run(['python', roulette_path])

def open_slot_machine_window():
	roulette_path=os.path.join(pathFile, "../slot_machine/slot.py")
	subprocess.run(['python', roulette_path])

def open_blackjack_window():
	roulette_path=os.path.join(pathFile, "../black_jack/blackJack.py")
	subprocess.run(['python', roulette_path])

def start_casino():
	# Configurazione finestra principale
	ctk.set_appearance_mode("dark")
	ctk.set_default_color_theme("dark-blue")
	root = ctk.CTk()
	root.geometry("1200x600")  # Dimensione maggiore per il debug
	root.title("Jackpot Royale")
	root.state('zoomed')  # Mantiene la finestra massimizzata
	root.resizable(False, False)
	coins = 1000

	# Carica e imposta lo sfondo
	bg_image = ctk.CTkImage(light_image=Image.open(f"{pathFile}/immagini/casino_bg.png"), dark_image=Image.open(f"{pathFile}/immagini/casino_bg.png"), size=(1920, 1080))
	bg_label = ctk.CTkLabel(root, image=bg_image, text="")
	bg_label.place(relwidth=1, relheight=1)

	# Titolo del casinò
	casino_name = ctk.CTkLabel(root, text="Jackpot Royale", font=("Helvetica", 36, "bold"), text_color="white")
	casino_name.pack(pady=20)

	# Etichetta delle monete in alto a destra
	coin_frame = ctk.CTkFrame(root, fg_color="black", corner_radius=10, border_width=2, border_color="gold")
	coin_frame.place(relx=0.95, rely=0.05, anchor="ne")
	coin_label = ctk.CTkLabel(coin_frame, text=f"💰 {coins}", font=("Helvetica", 18, "bold"), text_color="gold")
	coin_label.pack(padx=10, pady=5)

	# Crea un frame per i bottoni più in basso
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

	button_style = {"font": ("Helvetica", 16, "bold"), "text_color": "white", "fg_color": "gray", "corner_radius": 12, "hover_color": "#4d4d4d"}

	roulette_button = ctk.CTkButton(button_frame, image=roulette_photo, text="Roulette", **button_style, command=open_roulette_window)
	roulette_button.grid(row=0, column=0, padx=15, pady=15)

	slot_button = ctk.CTkButton(button_frame, image=slot_photo, text="Slot Machine", **button_style, command=open_slot_machine_window)
	slot_button.grid(row=0, column=1, padx=15, pady=15)

	blackjack_button = ctk.CTkButton(button_frame, image=blackjack_photo, text="Blackjack", **button_style, command=open_blackjack_window)
	blackjack_button.grid(row=0, column=2, padx=15, pady=15)

	# Avvia l'animazione delle monete
	falling_coin = FallingCoin(root)
	falling_coin.start_coin_animation()

	root.mainloop()

if __name__ == "__main__":
	start_casino()