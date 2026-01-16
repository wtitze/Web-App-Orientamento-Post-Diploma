from typing import Annotated, TypedDict, List, Optional
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class StudentProfile(BaseModel):
    scuola: Optional[str] = None
    indirizzo: Optional[str] = None
    localita: Optional[str] = None
    interessi: List[str] = []
    aspirazioni: Optional[str] = None
    budget_limitato: bool = False
    mobilita: Optional[str] = None

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    profile: StudentProfile
    next_steps: List[str]
    search_results: List[dict]
    # Usiamo questo campo per salvare il nome del modello usato
    model_used: Optional[str]
