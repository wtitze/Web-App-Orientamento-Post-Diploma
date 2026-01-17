from typing import Annotated, TypedDict, List, Optional
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class StudentProfile(BaseModel):
    scuola: Optional[str] = None
    indirizzo: Optional[str] = None
    localita: Optional[str] = None
    sogni_aspirazioni: Optional[str] = None
    budget_mensile_max: Optional[float] = None
    mobilita_estesa: Optional[str] = None
    interessi_pratici: List[str] = []
    percorso_scelto: Optional[str] = None

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    profile: StudentProfile
    current_phase: int
    phase_completion: float
    judge_feedback: Optional[str]
    model_used: str
    iteration_count: int
