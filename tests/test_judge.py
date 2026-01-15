import pytest
from backend.app.agent.judge import judge_response

def test_eval_wrong_location():
    """Testa se il giudice rileva un errore di località (Vincolo violato)"""
    profilo = {"localita": "Pisa", "aspirazioni": "Lavoro"}
    query = "Cerco un lavoro vicino a me"
    # Risposta volutamente sbagliata per testare il giudice
    risposta_agente = "Ti consiglio l'azienda TechSpa che si trova a Milano."
    
    report = judge_response(profilo, query, risposta_agente)
    
    print(f"\n[REPORT]: Fedeltà {report.punteggio_fedelta}/5 - Critica: {report.analisi_critica}")
    assert report.punteggio_fedelta <= 2

def test_eval_hallucination():
    """Testa se il giudice rileva link inventati"""
    profilo = {"localita": "Torino"}
    query = "Sito di un'azienda tech a Torino"
    risposta_agente = "Puoi guardare il sito www.azienda-totalmente-inventata-123.it"
    
    report = judge_response(profilo, query, risposta_agente)
    
    assert report.allucinazione_rilevata == True
