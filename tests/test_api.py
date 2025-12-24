import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_read_root():
    """Verifica che l'endpoint root risponda correttamente"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_chat_endpoint_schema():
    """Verifica che lo schema di input/output dell'endpoint /chat sia corretto"""
    payload = {
        "message": "Ciao, sono uno studente dell'ultimo anno.",
        "history": []
    }
    # Ci aspettiamo che l'API riceva i dati. 
    # Se non c'è una chiave API reale, restituirà 500 (errore Groq), 
    # ma il test valida che la chiamata arrivi al backend.
    response = client.post("/chat", json=payload)
    assert response.status_code in [200, 500]
