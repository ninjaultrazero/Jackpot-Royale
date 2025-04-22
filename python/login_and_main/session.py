import json
import os

SESSION_FILE = os.path.join(os.path.dirname(__file__), "session.json")

def set_logged_user(email):
    with open(SESSION_FILE, "w") as f:
        json.dump({"logged_user": email}, f)

def get_logged_user():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        data = json.load(f)
        return data.get("logged_user")

def clear_logged_user():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
