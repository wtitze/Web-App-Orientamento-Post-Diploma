import pytest
from backend.app.agent.parser import extract_profile_logic
from backend.app.agent.state import StudentProfile
from langchain_core.messages import HumanMessage, AIMessage

class MockLLM:
    """Simula il comportamento del modello per il test di struttura"""
    def with_structured_output(self, schema):
        return self
    def invoke(self, prompt):
        # Simula il ritorno di un profilo aggiornato
        return StudentProfile(scuola="Liceo", localita="Milano")

def test_profile_extraction():
    messages = [HumanMessage(content="Ciao, faccio il liceo e vivo a Milano")]
    current_profile = StudentProfile()
    mock_llm = MockLLM()
    
    new_profile = extract_profile_logic(messages, current_profile, mock_llm)
    
    assert new_profile.scuola == "Liceo"
    assert new_profile.localita == "Milano"
