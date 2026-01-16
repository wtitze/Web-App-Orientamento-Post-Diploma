import os
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'), override=True)

class EvaluationReport(BaseModel):
    risposta_pertinente: bool
    violazione_protocollo: bool
    analisi_critica: str
    model_used: str = ""

def judge_response(profile_dict: dict, query: str, assistant_response: str):
    prompt = f"Ispettore: Valuta.\nProfilo: {profile_dict}\nDomanda: {query}\nRisposta: {assistant_response}"
    
    try:
        # Primario: Groq Llama 8B
        llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
        report = llm.with_structured_output(EvaluationReport).invoke(prompt)
        report.model_used = "Groq (Llama 8B)"
        return report
    except Exception:
        # Fallback: Gemini Stable Flash
        print("Fallback Giudice a Gemini...")
        llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)
        report = llm.with_structured_output(EvaluationReport).invoke(prompt)
        report.model_used = "Gemini (Stable Flash)"
        return report
