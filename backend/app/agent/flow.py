import os
from typing import Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from backend.app.agent.state import AgentState, StudentProfile
from backend.app.agent.prompts import SYSTEM_PROMPT
from backend.app.agent.parser import extract_profile_logic
from backend.app.tools.search import web_search_tool
from backend.app.tools.scraper import scrape_website_tool

# Caricamento esplicito .env dalla root (Huyen pag. 235)
load_dotenv(os.path.join(os.getcwd(), '.env'), override=True)

# Inizializzazione modelli
groq_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest", 
    temperature=0.1,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def universal_llm_call(prompt_list, structured_schema=None):
    """Il PROXY: gestisce il fallback globale (Huyen pag. 299)"""
    try:
        model = groq_llm
        if structured_schema:
            model = model.with_structured_output(structured_schema)
        return model.invoke(prompt_list), "Groq (Llama 3.3)"
    except Exception as e:
        if "429" in str(e) or "rate_limit" in str(e).lower():
            print("--- FALLBACK GLOBALE: Passaggio a Gemini (Stable) ---")
            model = gemini_llm
            if structured_schema:
                model = model.with_structured_output(structured_schema)
            try:
                response = model.invoke(prompt_list)
                return response, "Gemini (Stable Flash)"
            except Exception as gem_e:
                print(f"ERRORE CRITICO ANCHE SU GEMINI: {gem_e}")
                return AIMessage(content="Servizi AI sovraccarichi. Riprova tra poco."), "ERRORE"
        raise e

def profile_node(state: AgentState):
    updated_profile = extract_profile_logic(state["messages"], state["profile"], universal_llm_call)
    return {"profile": updated_profile}

def analyzer_node(state: AgentState):
    profile_info = f"\n[DATI SIDEBAR]: {state['profile'].model_dump()}"
    instruction = "\nRispondi all'utente o usa 'AZIONE: RICERCA [query]'. Sii breve."
    full_prompt = [{"role": "system", "content": SYSTEM_PROMPT + profile_info + instruction}] + state["messages"][-4:]
    response, model_name = universal_llm_call(full_prompt)
    return {"messages": [response], "model_used": model_name}

def router_logic(state: AgentState) -> Literal["call_search", "call_scraper", "finish"]:
    """Logica di Routing Corretta (Huyen pag. 283)"""
    last_msg = state["messages"][-1].content
    if "AZIONE: RICERCA" in last_msg:
        return "call_search"
    if "AZIONE: LEGGI" in last_msg:
        return "call_scraper"
    # IMPORTANTE: Restituiamo una stringa presente nel dizionario sotto
    return "finish"

def search_node(state: AgentState):
    query = state["messages"][-1].content.split("AZIONE: RICERCA")[-1].strip(" []")
    results = web_search_tool(query, max_results=5)
    obs = f"[RISULTATI RICERCA]:\n" + "\n".join([f"- {r['title']}: {r['link']}" for r in results])
    return {"messages": [SystemMessage(content=obs)]}

def scraper_node(state: AgentState):
    url = state["messages"][-1].content.split("AZIONE: LEGGI")[-1].strip(" []")
    content = scrape_website_tool(url)
    return {"messages": [SystemMessage(content=f"[CONTENUTO SITO]: {content[:800]}")]}

workflow = StateGraph(AgentState)
workflow.add_node("update_profile", profile_node)
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("search_tool", search_node)
workflow.add_node("scraper_tool", scraper_node)

workflow.set_entry_point("update_profile")
workflow.add_edge("update_profile", "analyzer")

# CORREZIONE MAPPATURA: Il router deve puntare a chiavi esistenti
workflow.add_conditional_edges(
    "analyzer",
    router_logic,
    {
        "call_search": "search_tool",
        "call_scraper": "scraper_tool",
        "finish": END  # 'finish' ora mappa correttamente a END
    }
)

workflow.add_edge("search_tool", "analyzer")
workflow.add_edge("scraper_tool", "analyzer")
app_graph = workflow.compile()
