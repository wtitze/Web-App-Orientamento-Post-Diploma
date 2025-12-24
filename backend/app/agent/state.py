from typing import Annotated, TypedDict, List, Optional
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class StudentProfile(BaseModel):
    scuola: Optional[str] = Field(None, description="Nome della scuola")
    indirizzo: Optional[str] = Field(None, description="Indirizzo di studi specifico, es: Meccanica, Classico, ecc.")
    localita: Optional[str] = Field(None, description="Città o zona")
    interessi: List[str] = Field(default_factory=list)
    aspirazioni: Optional[str] = Field(None)
    budget_limitato: bool = Field(False)
    mobilita: Optional[str] = Field(None)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    profile: StudentProfile
    next_steps: List[str]
    search_results: List[dict]
    recommendation: Optional[str]
