from typing import Optional
from langchain_groq import ChatGroq
from backend.app.agent.state import StudentProfile
from backend.app.agent.prompts import PROFILE_EXTRACTOR_PROMPT

def extract_profile_logic(messages: list, current_profile: StudentProfile, llm: ChatGroq) -> StudentProfile:
    """
    Analizza la conversazione e aggiorna il profilo strutturato dello studente.
    Utilizza model_dump() per compatibilità con Pydantic V2.
    """
    # model_dump() sostituisce il vecchio dict() in Pydantic V2
    profile_context = f"Profilo attuale: {current_profile.model_dump()}"
    
    # Prepariamo il modello per l'output strutturato
    structured_llm = llm.with_structured_output(StudentProfile)
    
    # Prendiamo gli ultimi messaggi per il contesto
    history_text = "\n".join([f"{getattr(m, 'type', 'messaggio')}: {m.content}" for m in messages[-5:]])
    
    prompt = f"{PROFILE_EXTRACTOR_PROMPT}\n\n{profile_context}\n\nNuovi messaggi:\n{history_text}"
    
    try:
        updated_profile = structured_llm.invoke(prompt)
        return updated_profile
    except Exception as e:
        print(f"Errore nell'estrazione profilo: {e}")
        return current_profile
