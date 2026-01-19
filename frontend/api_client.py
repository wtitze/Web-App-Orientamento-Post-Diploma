import requests

BACKEND_URL = "http://localhost:8000"

def send_message(message, history, profile, phase, groq_fuel, gemini_fuel):
    try:
        payload = {
            "message": message, 
            "history": history, 
            "profile": profile,
            "current_phase": phase,
            "groq_tokens_left": groq_fuel,
            "gemini_requests_left": gemini_fuel
        }
        response = requests.post(f"{BACKEND_URL}/chat", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"response": f"Errore connessione: {e}", "profile": profile}
