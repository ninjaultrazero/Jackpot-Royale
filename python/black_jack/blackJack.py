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

pygame.mixer.init()
pygame.font.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMMAGINI_PATH = os.path.join(BASE_DIR, "immagini")

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
        self.root.geometry("900x650")
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(bg="#14452F")

        try:
            self.player_coins = get_balance()
        except ValueError as e:
            msgbox.showerror("Errore", str(e))
            sys.exit()

        self.bet = 100
        self.deck = get_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.card_images = load_card_images()

        self.build_ui()
        self.reset_game()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self.root, text="BLACKJACK", font=("Arial", 48, "bold"), text_color="gold")
        self.title_label.pack(pady=10)

        self.status_frame = ctk.CTkFrame(self.root, fg_color="#1A3B2A")
        self.status_frame.pack(pady=10)

        self.coins_label = ctk.CTkLabel(self.status_frame, text=f"Monete: {self.player_coins}", font=("Arial", 18))
        self.coins_label.grid(row=0, column=0, padx=20, pady=5)

        self.bet_label = ctk.CTkLabel(self.status_frame, text=f"Puntata: {self.bet}", font=("Arial", 18))
        self.bet_label.grid(row=0, column=1, padx=20, pady=5)

        self.player_score_label = ctk.CTkLabel(self.status_frame, text="Punteggio Giocatore: 0", font=("Arial", 18))
        self.player_score_label.grid(row=1, column=0, padx=20, pady=5)

        self.dealer_score_label = ctk.CTkLabel(self.status_frame, text="Punteggio Banco: ?", font=("Arial", 18))
        self.dealer_score_label.grid(row=1, column=1, padx=20, pady=5)

        self.table_frame = ctk.CTkFrame(self.root, fg_color="#20603D")
        self.table_frame.pack(pady=10)

        self.dealer_hand_frame = ctk.CTkFrame(self.table_frame)
        self.dealer_hand_frame.pack(pady=5)

        self.player_hand_frame = ctk.CTkFrame(self.table_frame)
        self.player_hand_frame.pack(pady=5)

        self.button_frame = ctk.CTkFrame(self.root, fg_color="#1A3B2A")
        self.button_frame.pack(pady=20)

        self.hit_button = ctk.CTkButton(self.button_frame, text="Hit", width=100, command=self.hit)
        self.hit_button.pack(side="left", padx=20)

        self.stand_button = ctk.CTkButton(self.button_frame, text="Stand", width=100, command=self.stand)
        self.stand_button.pack(side="left", padx=20)

        self.reset_button = ctk.CTkButton(self.button_frame, text="Reset", width=100, command=self.reset_game)
        self.reset_button.pack(side="left", padx=20)
        
        self.home_button = ctk.CTkButton(self.button_frame, text="Torna alla Home", command=self.torna_alla_home)
        self.home_button.pack(side="left", padx=20)

        # Add betting buttons
        self.bet_button_frame = ctk.CTkFrame(self.root, fg_color="#1A3B2A")
        self.bet_button_frame.pack(pady=20)

        self.bet_1_button = ctk.CTkButton(self.bet_button_frame, text="1", width=100, command=lambda: self.update_bet(1))
        self.bet_1_button.pack(side="left", padx=10)

        self.bet_25_button = ctk.CTkButton(self.bet_button_frame, text="25", width=100, command=lambda: self.update_bet(25))
        self.bet_25_button.pack(side="left", padx=10)

        self.bet_50_button = ctk.CTkButton(self.bet_button_frame, text="50", width=100, command=lambda: self.update_bet(50))
        self.bet_50_button.pack(side="left", padx=10)

        self.bet_100_button = ctk.CTkButton(self.bet_button_frame, text="100", width=100, command=lambda: self.update_bet(100))
        self.bet_100_button.pack(side="left", padx=10)

    def update_bet(self, amount):
        if self.player_coins >= amount:
            self.bet = amount
            self.bet_label.configure(text=f"Puntata: {self.bet}")
        else:
            msgbox.showerror("Errore", "Non hai abbastanza monete per questa puntata.")

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
            card_label = ctk.CTkLabel(self.player_hand_frame, image=card_image, text="")  # empty text to avoid extra space
            card_label.image = card_image
            card_label.pack(side="left", padx=5)

        for i, card in enumerate(self.dealer_hand):
            if i == 0:
                card_name = f"{card[0]}_{card[1]}"
                card_image = self.card_images.get(card_name)
                card_label = ctk.CTkLabel(self.dealer_hand_frame, image=card_image, text="")  # empty text to avoid extra space
                card_label.image = card_image
                card_label.pack(side="left", padx=5)
            else:
                back_label = ctk.CTkLabel(self.dealer_hand_frame, text="🂠", font=("Arial", 32))
                back_label.pack(side="left", padx=5)

        self.player_score_label.configure(text=f"Punteggio Giocatore: {hand_value(self.player_hand)}")
        self.dealer_score_label.configure(text="Punteggio Banco: ?")
        self.coins_label.configure(text=f"Monete: {self.player_coins}")
        self.bet_label.configure(text=f"Puntata: {self.bet}")

    def hit(self):
        self.player_hand.append(self.deck.pop())
        self.update_ui()
        if hand_value(self.player_hand) > 21:
            msgbox.showinfo("Bust!", "Hai sballato! Il banco vince.")
            self.player_coins -= self.bet
            self.coins_label.configure(text=f"Monete: {self.player_coins}")  # Update coins here
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
        else:
            msgbox.showinfo("Banco Vince", "Il banco vince.")
            self.player_coins -= self.bet

        self.coins_label.configure(text=f"Monete: {self.player_coins}")  # Update coins here
        remove_coins(self.player_coins)
        self.end_game()

    def show_full_dealer_hand(self):
        for widget in self.dealer_hand_frame.winfo_children():
            widget.destroy()
        for card in self.dealer_hand:
            card_name = f"{card[0]}_{card[1]}"
            card_image = self.card_images.get(card_name)
            card_label = ctk.CTkLabel(self.dealer_hand_frame, image=card_image, text="")  # empty text to avoid extra space
            card_label.image = card_image
            card_label.pack(side="left", padx=5)
        self.dealer_score_label.configure(text=f"Punteggio Banco: {hand_value(self.dealer_hand)}")

    def end_game(self):
        self.hit_button.configure(state="disabled")
        self.stand_button.configure(state="disabled")
        self.coins_label.configure(text=f"Monete: {self.player_coins}")
    def torna_alla_home(self):
        home_path = os.path.join(os.path.dirname(__file__), '..', 'login_and_main', 'main.py')
        os.execl(sys.executable, sys.executable, home_path)

def main():
    root = ctk.CTk()
    app = BlackjackApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
