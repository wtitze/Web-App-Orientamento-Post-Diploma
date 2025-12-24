import requests

BACKEND_URL = "http://localhost:8000"

def send_message(message, history, profile):
    try:
        # Inviamo anche il profilo attuale
        payload = {"message": message, "history": history, "profile": profile}
        response = requests.post(f"{BACKEND_URL}/chat", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"response": f"Errore: {e}", "profile": profile}
