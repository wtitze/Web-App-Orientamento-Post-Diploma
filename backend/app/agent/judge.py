import os
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class EvaluationReport(BaseModel):
    punteggio_fedelta: int = Field(description="Voto 1-5 sul rispetto dei vincoli")
    punteggio_efficienza: int = Field(description="Voto 1-5 sulla proattività (ha usato i tool quando richiesto?)")
    analisi_critica: str = Field(description="Analisi dettagliata, inclusa la segnalazione di ridondanze")
    ridondanza_rilevata: bool = Field(description="True se l'agente ripete il profilo inutilmente")
    allucinazione_rilevata: bool = Field(description="True se inventa dati")

def judge_response(profile_dict: dict, query: str, assistant_response: str) -> EvaluationReport:
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=api_key)
    structured_judge = llm.with_structured_output(EvaluationReport)

    prompt = f"""
    Sei un Supervisore della Qualità. Valuta la risposta dell'Agente Orientatore.

    PROFILO STUDENTE: {profile_dict}
    DOMANDA UTENTE: {query}
    RISPOSTA AGENTE: {assistant_response}

    PENALITÀ CRITICHE:
    1. RIDONDANZA: Se l'agente ripete il profilo (Scuola, Indirizzo, ecc.) nella risposta, penalizza pesantemente e segna ridondanza_rilevata=True.
    2. PIGRIZIA: Se l'utente ha detto 'sì' a una ricerca e l'agente ha risposto solo con chiacchiere senza attivare 'AZIONE: RICERCA', dai 1 in efficienza.
    3. COERENZA: Deve rispettare i 60 minuti di treno da Milano.

    Sii estremamente severo sulla ripetitività.
    """
    return structured_judge.invoke(prompt)
