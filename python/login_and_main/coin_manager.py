import json
import os

# Ottieni il path assoluto del file JSON
BASE_DIR = os.path.dirname(__file__)
COINS_PATH = os.path.join(BASE_DIR, "users.json")

def get_coins():
    with open(COINS_PATH, "r") as file:
        data = json.load(file)
    return data[2]["balance"]

def set_coins(new_amount):
    with open(COINS_PATH, "w") as file:
        json.dump({"coins": new_amount}, file)

def add_coins(amount):
    coins = get_coins()
    set_coins(coins + amount)

def remove_coins(amount):
    coins = get_coins()
    if coins >= amount:
        set_coins(coins - amount)
        return True
    return False
