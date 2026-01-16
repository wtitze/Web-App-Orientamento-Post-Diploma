from backend.app.agent.state import StudentProfile
from backend.app.agent.prompts import PROFILE_EXTRACTOR_PROMPT

def extract_profile_logic(messages: list, current_profile: StudentProfile, llm_proxy_func) -> StudentProfile:
    """
    Analizza la conversazione e aggiorna il profilo strutturato.
    Utilizza la funzione proxy per gestire il fallback tra modelli.
    """
    profile_context = f"Profilo attuale: {current_profile.model_dump()}"
    history_text = "\n".join([f"{getattr(m, 'type', 'msg')}: {m.content}" for m in messages[-5:]])
    
    prompt = f"{PROFILE_EXTRACTOR_PROMPT}\n\n{profile_context}\n\nNuovi messaggi:\n{history_text}"
    
    try:
        # Chiamiamo la funzione universale chiedendo un output strutturato
        updated_profile, _ = llm_proxy_func(prompt, structured_schema=StudentProfile)
        return updated_profile
    except Exception as e:
        print(f"Errore critico estrazione profilo: {e}")
        return current_profile
