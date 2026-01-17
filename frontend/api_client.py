import requests

BACKEND_URL = "http://localhost:8000"

def send_message(message, history, profile, phase, completion):
    try:
        payload = {
            "message": message, 
            "history": history, 
            "profile": profile,
            "current_phase": phase,
            "phase_completion": completion
        }
        response = requests.post(f"{BACKEND_URL}/chat", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"response": f"Errore connessione: {e}", "profile": profile}
