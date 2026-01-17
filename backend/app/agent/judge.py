import os
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'), override=True)

class PhaseReport(BaseModel):
    percentage: float = Field(description="Percentuale 0-100")
    can_move_to_next: bool = Field(description="True se >= 80%")
    feedback_for_agent: str = Field(description="Cosa manca")

def audit_phase_logic(profile_dict: dict, current_phase: int, last_msg: str):
    # Usiamo l'alias 'gemini-flash-latest' che abbiamo verificato essere stabile
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest", 
        temperature=0, 
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    structured_judge = llm.with_structured_output(PhaseReport)
    
    from backend.app.agent.prompts import JUDGE_PROMPT
    
    prompt = f"""
    {JUDGE_PROMPT}
    
    FASE ATTUALE: {current_phase}
    PROFILO ATTUALE: {profile_dict}
    ULTIMA RISPOSTA AGENTE: {last_msg}
    """
    
    try:
        return structured_judge.invoke(prompt)
    except Exception as e:
        print(f"   [Judge] ERRORE: {e}")
        return PhaseReport(percentage=0, can_move_to_next=False, feedback_for_agent="Errore tecnico nel giudice.")
