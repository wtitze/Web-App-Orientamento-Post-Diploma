import pytest
from backend.app.agent.state import StudentProfile, AgentState

def test_student_profile_creation():
    """Verifica che il profilo dello studente venga creato correttamente"""
    profile = StudentProfile(
        scuola="Liceo Scientifico",
        localita="Pisa",
        interessi=["Informatica", "Gaming"],
        aspirazioni="Voglio lavorare nel software"
    )
    assert profile.scuola == "Liceo Scientifico"
    assert "Informatica" in profile.interessi
    assert profile.budget_limitato is False # Valore di default

def test_agent_state_initialization():
    """Verifica che lo stato dell'agente accetti i dati previsti"""
    initial_profile = StudentProfile()
    state: AgentState = {
        "messages": [("user", "Ciao!")],
        "profile": initial_profile,
        "next_steps": ["intervista_iniziale"],
        "search_results": [],
        "recommendation": None
    }
    assert len(state["messages"]) == 1
    assert state["next_steps"][0] == "intervista_iniziale"

def test_profile_update():
    """Simula l'aggiornamento del profilo durante la conversazione"""
    profile = StudentProfile()
    profile.scuola = "ITI Informatica"
    profile.interessi.append("Robotica")
    
    assert profile.scuola == "ITI Informatica"
    assert "Robotica" in profile.interessi