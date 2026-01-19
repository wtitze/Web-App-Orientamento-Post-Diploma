import os
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'), override=True)

class PhaseReport(BaseModel):
    percentage: float = Field(description="0-100")
    can_move_to_next: bool = Field(description="True se >= 80%")
    feedback: str = Field(description="Cosa manca")

def audit_phase_logic(profile_dict: dict, phase: int):
    # Il Giudice usa Gemini Flash per efficienza (o Groq 70B se preferisci potenza)
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0, google_api_key=os.getenv("GOOGLE_API_KEY"))
    structured_llm = llm.with_structured_output(PhaseReport)
    
    from backend.app.agent.prompts import JUDGE_PROMPT
    prompt = f"{JUDGE_PROMPT}\nFase: {phase}\nProfilo attuale: {profile_dict}"
    
    try:
        res = structured_llm.invoke(prompt)
        return res
    except:
        return PhaseReport(percentage=0, can_move_to_next=False, feedback="Errore Audit")
