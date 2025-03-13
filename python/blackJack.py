import customtkinter as ctk
import os
import random
from tkinter import PhotoImage

pathFile = os.path.dirname(os.path.abspath(__file__))  # Percorso della cartella corrente

# Classe per il gioco Blackjack
class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        
        self.player_hand = []
        self.dealer_hand = []
        self.deck = []
        self.player_credit = 100  # Credito iniziale del giocatore
        
        self.create_ui()
        self.start_game()

    def create_ui(self):
        # Sfondo verde per il tavolo da gioco
        self.root.configure(bg="green")

        # Frame per le carte del giocatore e del mazziere
        self.player_frame = ctk.CTkFrame(self.root, bg_color="green")
        self.player_frame.pack(side="top", pady=20)

        self.dealer_frame = ctk.CTkFrame(self.root, bg_color="green")
        self.dealer_frame.pack(side="top", pady=20)

        # Credito del giocatore in alto a destra
        self.credit_label = ctk.CTkLabel(self.root, text=f"Credito: {self.player_credit}€", font=("Helvetica", 16), text_color="white", bg_color="green")
        self.credit_label.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)  # Usa x e y per posizionamento con offset

        # Bottoni per le azioni
        self.hit_button = ctk.CTkButton(self.root, text="Hit", command=self.hit, width=10)
        self.hit_button.pack(side="left", padx=20, pady=10)

        self.stand_button = ctk.CTkButton(self.root, text="Stand", command=self.stand, width=10)
        self.stand_button.pack(side="left", padx=20, pady=10)

        self.new_game_button = ctk.CTkButton(self.root, text="New Game", command=self.new_game, width=12)
        self.new_game_button.pack(side="left", padx=20, pady=10)

        self.bet_button = ctk.CTkButton(self.root, text="Place Bet", command=self.place_bet, width=12)
        self.bet_button.pack(side="left", padx=20, pady=10)

    def load_deck(self):
        # Caricamento delle immagini delle carte
        suits = ['CUORI', 'FIORI', 'PICCHE', 'QUADRI']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        # Costruzione del mazzo con il percorso delle immagini
        return [f"img carte/{suit}/{rank}{suit[0]}.png" for suit in suits for rank in ranks]

    def update_display(self):
        # Rimuove le vecchie carte dai frame
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()

        # Visualizza le carte del giocatore
        for card in self.player_hand:
            img = PhotoImage(file=os.path.join(pathFile, card))  # Usa il percorso corretto per il file immagine
            label = ctk.CTkLabel(self.player_frame, image=img, text="")
            label.image = img  # Mantieni una referenza all'immagine
            label.pack(side="left", padx=5)

        # Visualizza le carte del mazziere
        for card in self.dealer_hand:
            img = PhotoImage(file=os.path.join(pathFile, card))  # Usa il percorso corretto per il file immagine
            label = ctk.CTkLabel(self.dealer_frame, image=img, text="")
            label.image = img  # Mantieni una referenza all'immagine
            label.pack(side="left", padx=5)

    def deal_cards(self):
        # Distribuisci 2 carte al giocatore e al mazziere
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.update_display()

    def hit(self):
        # Aggiungi una carta al giocatore
        if len(self.deck) > 0:
            self.player_hand.append(self.deck.pop())
            self.update_display()

    def stand(self):
        # Gestisce il turno del mazziere
        while self.calculate_hand_value(self.dealer_hand) < 17:
            if len(self.deck) > 0:
                self.dealer_hand.append(self.deck.pop())
        self.update_display()

        # Concludi la partita
        self.end_game()

    def place_bet(self):
        # Per semplicità, facciamo un betting fisso (modifica a piacere)
        bet = 10  # Sostituisci con un valore di scommessa
        if self.player_credit >= bet:
            self.player_credit -= bet
            self.credit_label.config(text=f"Credito: {self.player_credit}€")
            self.start_game()
        else:
            self.show_message("Non hai abbastanza credito!")

    def new_game(self):
        self.start_game()

    def start_game(self):
        # Avvia il gioco e distribuisci le carte
        self.deck = self.load_deck()
        random.shuffle(self.deck)
        self.deal_cards()

    def calculate_hand_value(self, hand):
        # Calcola il valore della mano (semplificato)
        value = 0
        ace_count = 0
        for card in hand:
            rank = card.split('/')[-1][0]  # Estrai il rango (ad esempio, "2", "J", "K")
            if rank in ['J', 'Q', 'K']:
                value += 10
            elif rank == 'A':
                ace_count += 1
                value += 11  # Trattiamo l'asso come 11
            else:
                value += int(rank)
        
        # Se ci sono assi e il valore è maggiore di 21, trattiamo l'asso come 1
        while value > 21 and ace_count:
            value -= 10
            ace_count -= 1
        return value

    def end_game(self):
        # Determina il vincitore e aggiorna il credito
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)

        if player_value > 21:
            self.show_message("Hai sballato! Hai perso.")
        elif dealer_value > 21 or player_value > dealer_value:
            self.show_message("Hai vinto!")
            self.player_credit += 20  # Aggiungi un premio
        elif player_value < dealer_value:
            self.show_message("Il mazziere ha vinto!")
        else:
            self.show_message("Pareggio!")
        
        # Mostra il nuovo credito
        self.credit_label.config(text=f"Credito: {self.player_credit}€")

    def show_message(self, message):
        # Mostra un messaggio a schermo
        message_label = ctk.CTkLabel(self.root, text=message, font=("Helvetica", 16), text_color="yellow", bg_color="green")
        message_label.place(relx=0.5, rely=0.5, anchor="center")
        self.root.after(2000, message_label.destroy)  # Rimuovi il messaggio dopo 2 secondi

# Configurazione dell'interfaccia Tkinter
root = ctk.CTk()
game = BlackjackGame(root)
root.mainloop()
