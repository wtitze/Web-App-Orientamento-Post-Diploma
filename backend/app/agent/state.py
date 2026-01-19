from typing import Annotated, TypedDict, List, Optional
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class StudentProfile(BaseModel):
    diploma_conseguito: Optional[str] = None
    competenze_tecniche: List[str] = [] # Solo linguaggi/tool noti
    residenza_attuale: Optional[str] = None
    disponibilita_trasferimento: Optional[float] = None
    obiettivo_post_diploma: Optional[str] = None
    settore_di_interesse: Optional[str] = None
    raggio_mobilita: Optional[str] = None # Default rimosso

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    profile: StudentProfile
    current_phase: int
    phase_completion: float
    groq_tokens_left: int
    gemini_requests_left: int
    last_model_used: str
    iteration_count: int
    judge_feedback: Optional[str]
