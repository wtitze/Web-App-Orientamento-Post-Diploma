import os
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class EvaluationReport(BaseModel):
    risposta_pertinente: bool = Field(description="False se l'agente ha ignorato la domanda o ha dato consigli senza avere i dati necessari")
    violazione_protocollo: bool = Field(description="True se l'agente ha dato link o consigli senza prima chiedere città/scuola")
    analisi_critica: str = Field(description="Spiegazione tecnica del fallimento ingegneristico")

def judge_response(profile_dict: dict, query: str, assistant_response: str) -> EvaluationReport:
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, api_key=api_key)
    structured_judge = llm.with_structured_output(EvaluationReport)

    prompt = f"""
    Sei un Ispettore di Processo per sistemi IA. Devi verificare se l'Agente Orientatore ha violato le regole di AI Engineering.

    PROFILO STUDENTE: {profile_dict}
    DOMANDA UTENTE: {query}
    RISPOSTA AGENTE: {assistant_response}

    REGOLE DA VERIFICARE:
    1. Se l'agente ha fornito link o aziende ma nel PROFILO STUDENTE la 'scuola' o la 'localita' sono assenti o nulle, è una VIOLAZIONE GRAVE.
    2. L'agente non deve mai indovinare la città (es. Milano) se l'utente non l'ha detta.
    3. Se l'agente ha violato queste regole, segna violazione_protocollo=True e risposta_pertinente=False.

    Sii estremamente pignolo e severo.
    """
    return structured_judge.invoke(prompt)
