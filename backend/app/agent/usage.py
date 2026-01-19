import json
import os

# Percorso assoluto per il file delle statistiche nella root del progetto
USAGE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "usage_stats.json")
DEFAULT_TOKENS = 100000

def get_remaining_tokens():
    if not os.path.exists(USAGE_FILE):
        return DEFAULT_TOKENS
    try:
        with open(USAGE_FILE, "r") as f:
            data = json.load(f)
            return data.get("remaining", DEFAULT_TOKENS)
    except:
        return DEFAULT_TOKENS

def update_remaining_tokens(value):
    try:
        with open(USAGE_FILE, "w") as f:
            json.dump({"remaining": int(value)}, f)
    except Exception as e:
        print(f"Errore salvataggio usage: {e}")
