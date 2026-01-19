import pytest
from backend.app.agent.state import StudentProfile, AgentState

def test_student_profile_new_schema():
    """Verifica che il profilo contenga l'indirizzo di studio e non la scuola"""
    profile = StudentProfile(
        indirizzo_studio="Informatica",
        residenza_citta="Milano",
        aspirazioni="Voglio lavorare"
    )
    # Verifica presenza campi corretti
    assert profile.indirizzo_studio == "Informatica"
    assert profile.residenza_citta == "Milano"
    
    # Verifica assenza campi vecchi o parassiti (Huyen, pag. 303)
    # Se scriviamo profile.scuola_nome dovrebbe dare errore di attributo
    with pytest.raises(AttributeError):
        _ = profile.scuola_nome

def test_fuel_gauge_initialization():
    """Verifica che i serbatoi partano dai valori massimi"""
    state: AgentState = {
        "messages": [],
        "profile": StudentProfile(),
        "current_phase": 1,
        "phase_completion": 0.0,
        "groq_tokens_left": 100000,
        "gemini_requests_left": 1500,
        "model_parser": "-",
        "model_orientatore": "-",
        "model_giudice": "-",
        "iteration_count": 0,
        "judge_feedback": None
    }
    assert state["groq_tokens_left"] == 100000
    assert state["gemini_requests_left"] == 1500
    assert state["current_phase"] == 1

def test_profile_serialization():
    """Verifica che Pydantic V2 converta correttamente in dizionario per l'IA"""
    profile = StudentProfile(indirizzo_studio="Meccanica", budget_spese_formazione=100.0)
    dump = profile.model_dump()
    assert dump["indirizzo_studio"] == "Meccanica"
    assert dump["budget_spese_formazione"] == 100.0
