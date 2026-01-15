import requests

BACKEND_URL = "http://localhost:8000"

def send_message(message, history, profile):
    try:
        payload = {"message": message, "history": history, "profile": profile}
        response = requests.post(f"{BACKEND_URL}/chat", json=payload)
        response.raise_for_status()
        return response.json() # Restituisce tutto il dizionario incluso judge_report
    except Exception as e:
        print(f"Errore API Client: {e}")
        return {"response": f"Errore: {e}", "profile": profile, "judge_report": None}
