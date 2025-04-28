import customtkinter as ctk
import pygame
import random
from PIL import Image, ImageTk
import threading
import time
import os
from customtkinter import CTkImage
import tkinter.messagebox as msgbox
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'login_and_main')))
from coin_manager import get_balance, remove_coins


# Inizializzazione di pygame solo per font e suoni
pygame.mixer.init()
pygame.font.init()

# Percorso base delle immagini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMMAGINI_PATH = os.path.join(BASE_DIR, "immagini")

# Mappature semi e rank
SUIT_FOLDER_MAP = {
    '♥': ('cuori', 'C'),
    '♠': ('picche', 'P'),
    '♦': ('quadri', 'Q'),
    '♣': ('fiori', 'F'),
}
RANK_MAP = {
    'A': '1',
    'J': 'J',
    'Q': 'Q',
    'K': 'K'
}

def get_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♠', '♥', '♦', '♣']
    return [(rank, suit) for rank in ranks for suit in suits]

def card_value(card):
    rank, _ = card
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)

def hand_value(hand):
    value = sum(card_value(card) for card in hand)
    aces = sum(1 for card in hand if card[0] == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def load_card_images():
    images = {}
    for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
        for suit_symbol in ['♠', '♥', '♦', '♣']:
            folder, suit_letter = SUIT_FOLDER_MAP[suit_symbol]
            rank_number = RANK_MAP.get(rank, rank)
            filename = f"{rank_number}{suit_letter}.png"
            image_path = os.path.join(IMMAGINI_PATH, folder, filename)

            card_name = f"{rank}_{suit_symbol}"
            if os.path.exists(image_path):
                img = Image.open(image_path).resize((60, 90))
                images[card_name] = ImageTk.PhotoImage(img)
            else:
                print(f"Warning: Missing image: {image_path}")
    return images

class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.geometry("800x600")
        # Ottieni il saldo iniziale
        try:
            self.player_coins = get_balance()
        except ValueError as e:
            msgbox.showerror("Errore", str(e))
            sys.exit()
        self.bet = 100  # Puoi farlo modificabile poi

        self.deck = get_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.card_images = load_card_images()

        # Font Pygame per "Blackjack" scritto grande
        self.blackjack_font = pygame.font.SysFont('comicsansms', 60)

        # Etichetta principale (Blackjack scritta grande simulata)
        self.blackjack_label = ctk.CTkLabel(self.root, text="BLACKJACK", font=("Comic Sans MS", 50, "bold"), text_color="gold")
        self.blackjack_label.pack(pady=10)

        self.coins_label = ctk.CTkLabel(self.root, text=f"Monete: {self.player_coins}", font=("Arial", 18))
        self.coins_label.pack(pady=5)

        self.bet_label = ctk.CTkLabel(self.root, text=f"Puntata: {self.bet}", font=("Arial", 18))
        self.bet_label.pack(pady=5)

        self.player_score_label = ctk.CTkLabel(self.root, text="Punteggio Giocatore: 0", font=("Arial", 18))
        self.player_score_label.pack(pady=5)

        self.dealer_score_label = ctk.CTkLabel(self.root, text="Punteggio Banco: ?", font=("Arial", 18))
        self.dealer_score_label.pack(pady=5)

        self.player_hand_frame = ctk.CTkFrame(self.root)
        self.player_hand_frame.pack(pady=10)

        self.dealer_hand_frame = ctk.CTkFrame(self.root)
        self.dealer_hand_frame.pack(pady=10)

        self.button_frame = ctk.CTkFrame(self.root)
        self.button_frame.pack(pady=20)

        self.hit_button = ctk.CTkButton(self.button_frame, text="Hit", command=self.hit)
        self.hit_button.pack(side="left", padx=20)

        self.stand_button = ctk.CTkButton(self.button_frame, text="Stand", command=self.stand)
        self.stand_button.pack(side="left", padx=20)

        self.reset_button = ctk.CTkButton(self.button_frame, text="Reset", command=self.reset_game)
        self.reset_button.pack(side="left", padx=20)

        self.reset_game()

    def reset_game(self):
        self.deck = get_deck()
        random.shuffle(self.deck)
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

        self.update_ui()
        self.hit_button.configure(state="normal")
        self.stand_button.configure(state="normal")

    def update_ui(self):
        for widget in self.player_hand_frame.winfo_children():
            widget.destroy()
        for widget in self.dealer_hand_frame.winfo_children():
            widget.destroy()

        for card in self.player_hand:
            card_name = f"{card[0]}_{card[1]}"
            card_image = self.card_images.get(card_name)
            card_label = ctk.CTkLabel(self.player_hand_frame, image=card_image)
            card_label.image = card_image
            card_label.pack(side="left", padx=5)

        for i, card in enumerate(self.dealer_hand):
            if i == 0:
                card_name = f"{card[0]}_{card[1]}"
                card_image = self.card_images.get(card_name)
                card_label = ctk.CTkLabel(self.dealer_hand_frame, image=card_image)
                card_label.image = card_image
                card_label.pack(side="left", padx=5)
            else:
                back_label = ctk.CTkLabel(self.dealer_hand_frame, text="🂠", font=("Arial", 30))
                back_label.pack(side="left", padx=5)

        self.player_score_label.configure(text=f"Punteggio Giocatore: {hand_value(self.player_hand)}")
        self.dealer_score_label.configure(text=f"Punteggio Banco: ?")
        self.coins_label.configure(text=f"Monete: {self.player_coins}")
        self.bet_label.configure(text=f"Puntata: {self.bet}")

    def hit(self):
        self.player_hand.append(self.deck.pop())
        self.update_ui()

        if hand_value(self.player_hand) > 21:
            msgbox.showinfo("Bust!", "Hai sballato! Il banco vince.")
            self.player_coins -= self.bet
            self.end_game()

    def stand(self):
        while hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())

        self.show_full_dealer_hand()

        player_score = hand_value(self.player_hand)
        dealer_score = hand_value(self.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            msgbox.showinfo("Vittoria!", "Hai vinto!")
            self.player_coins += self.bet
        elif dealer_score == player_score:
            msgbox.showinfo("Pareggio", "Pareggio!")
            # Nessuna variazione monete
        else:
            msgbox.showinfo("Banco Vince", "Il banco vince.")
            self.player_coins -= self.bet
        
        remove_coins(self.player_coins)
        self.end_game()

    def show_full_dealer_hand(self):
        for widget in self.dealer_hand_frame.winfo_children():
            widget.destroy()

        for card in self.dealer_hand:
            card_name = f"{card[0]}_{card[1]}"
            card_image = self.card_images.get(card_name)
            card_label = ctk.CTkLabel(self.dealer_hand_frame, image=card_image)
            card_label.image = card_image
            card_label.pack(side="left", padx=5)

        self.dealer_score_label.configure(text=f"Punteggio Banco: {hand_value(self.dealer_hand)}")

    def end_game(self):
        self.hit_button.configure(state="disabled")
        self.stand_button.configure(state="disabled")
        self.coins_label.configure(text=f"Monete: {self.player_coins}")

def main():
    root = ctk.CTk()
    app = BlackjackApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
