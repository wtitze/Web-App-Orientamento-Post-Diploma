import pytest
from backend.app.agent.state import StudentProfile
from backend.app.agent.parser import extract_profile_logic
from langchain_core.messages import HumanMessage

# Mock del proxy per simulare l'IA che estrae solo una parte dei dati
def mock_llm_proxy(state, prompt, task_type="weak", schema=None):
    # Simuliamo che l'IA abbia trovato solo la città
    return StudentProfile(residenza_citta="Milano"), "Mock", 100

def test_parser_sticky_memory():
    """
    Verifica che il parser aggiunga nuovi dati senza cancellare i vecchi.
    Huyen (pag. 303): Mantenimento dell'integrità strutturale.
    """
    # 1. Lo stato attuale ha già l'indirizzo di studio
    current_profile = StudentProfile(indirizzo_studio="Informatica")
    
    # 2. L'utente dice dove vive
    messages = [HumanMessage(content="Abito a Milano")]
    state = {"groq_tokens_left": 100000}
    
    # 3. Chiamata al parser (usando il mock che restituisce 'Milano')
    updated_profile, tokens = extract_profile_logic(messages, current_profile, mock_llm_proxy, state)
    
    # VERIFICA: La città deve essere stata aggiunta
    assert updated_profile.residenza_citta == "Milano"
    # VERIFICA: L'indirizzo di studio NON deve essere sparito (Sticky Logic)
    assert updated_profile.indirizzo_studio == "Informatica"
    assert tokens == 100

def test_parser_ignores_noise():
    """Verifica che messaggi irrilevanti non modifichino il profilo"""
    current_profile = StudentProfile(indirizzo_studio="Meccanica")
    messages = [HumanMessage(content="Ciao!")] # Messaggio corto
    state = {}
    
    # In questo caso il parser dovrebbe restituire il profilo originale senza chiamare l'IA
    updated_profile, tokens = extract_profile_logic(messages, current_profile, None, state)
    
    assert updated_profile.indirizzo_studio == "Meccanica"
    assert tokens == 0
