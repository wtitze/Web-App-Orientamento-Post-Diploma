from backend.app.agent.state import StudentProfile
from backend.app.agent.prompts import PROFILE_EXTRACTOR_PROMPT

def extract_profile_logic(messages: list, current_profile: StudentProfile, llm_proxy_func) -> StudentProfile:
    # Analizziamo solo gli ultimi scambi per non confondere il parser
    history_text = ""
    for m in messages[-4:]:
        role = "Studente" if m.type == "human" else "Orientatore"
        history_text += f"{role}: {m.content}\n"
    
    prompt = f"{PROFILE_EXTRACTOR_PROMPT}\n\n[DIALOGO ATTUALE]:\n{history_text}\n\n[PROFILO ATTUALE]: {current_profile.model_dump()}"
    
    try:
        new_data, _ = llm_proxy_func(prompt, structured_schema=StudentProfile)
        
        updated = current_profile.model_dump()
        for k, v in new_data.model_dump().items():
            # Logica Sticky: non sovrascrivere dati certi con None
            if v is not None and v != "" and v != []:
                updated[k] = v
        
        # Logica speciale per il percorso: se dice 'voglio lavorare', percorso_scelto = 'Lavoro'
        txt = history_text.lower()
        if "lavorare" in txt or "lavoro" in txt: updated["percorso_scelto"] = "Lavoro"
        elif "università" in txt or "laurea" in txt: updated["percorso_scelto"] = "Università"
        elif "its" in txt: updated["percorso_scelto"] = "ITS"
            
        return StudentProfile(**updated)
    except:
        return current_profile
