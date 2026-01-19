from backend.app.agent.state import StudentProfile
from backend.app.agent.prompts import PROFILE_EXTRACTOR_PROMPT

def extract_profile_logic(messages, current_profile, llm_proxy_func, state):
    last_user_msg = next((m.content for m in reversed(messages) if m.type == "human"), "")
    if len(last_user_msg) < 4: return current_profile, 0

    prompt = f"{PROFILE_EXTRACTOR_PROMPT}\nPROFILO ATTUALE: {current_profile.model_dump()}\nTESTO DA ANALIZZARE: {last_user_msg}"
    try:
        new_data, _, used_tokens = llm_proxy_func(state, prompt, task_type="weak", schema=StudentProfile)
        
        updated = current_profile.model_dump()
        
        # Merge intelligente: evita duplicati e non sovrascrive con None
        for k, v in new_data.model_dump().items():
            if k == "competenze_tecniche":
                # Unisce le liste e rimuove i duplicati (case-insensitive)
                combined = updated[k] + [item for item in v if item.lower() not in [x.lower() for x in updated[k]]]
                updated[k] = combined
            elif v is not None and v != "" and v != []:
                updated[k] = v
                
        return StudentProfile(**updated), used_tokens
    except:
        return current_profile, 0
