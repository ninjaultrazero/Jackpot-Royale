import json
import os
from session import get_logged_user  # Usa la funzione per ottenere l'utente loggato

BASE_DIR = os.path.dirname(__file__)
COINS_PATH = os.path.join(BASE_DIR, "users.json")

def get_balance():
    email = get_logged_user()
    if not email:
        raise ValueError("Nessun utente loggato.")
    
    with open(COINS_PATH, "r") as file:
        users = json.load(file)

    for user in users:
        if user["email"] == email:
            return user["balance"]
    
    raise ValueError("Utente non trovato.")

def set_balance(new_balance):
    email = get_logged_user()
    if not email:
        raise ValueError("Nessun utente loggato.")
    
    with open(COINS_PATH, "r") as file:
        users = json.load(file)

    user_found = False
    for user in users:
        if user["email"] == email:
            user["balance"] = new_balance
            user_found = True
            break

    if not user_found:
        raise ValueError("Utente non trovato.")
    
    # Stampa di debug
    print(f"Aggiornato saldo dell'utente {email} a {new_balance}")
    
    with open(COINS_PATH, "w") as file:
        json.dump(users, file, indent=4)

    # Stampa di conferma
    print(f"File JSON aggiornato: {json.dumps(users, indent=4)}")


def add_coins(amount):
    current = get_balance()
    if current is not None:
        set_balance(current + amount)

def remove_coins(amount):
    current = get_balance()
    if current is not None and current >= amount:
        set_balance(amount)
        return True
    return False
