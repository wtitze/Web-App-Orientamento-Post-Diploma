import os
from typing import Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from backend.app.agent.state import AgentState, StudentProfile
from backend.app.agent.prompts import SYSTEM_PROMPT
from backend.app.agent.parser import extract_profile_logic
from backend.app.tools.search import web_search_tool
from backend.app.tools.scraper import scrape_website_tool

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1, api_key=api_key)

def profile_node(state: AgentState):
    updated_profile = extract_profile_logic(state["messages"], state["profile"], llm)
    return {"profile": updated_profile}

def analyzer_node(state: AgentState):
    profile_info = f"\n[DATI SIDEBAR]: {state['profile'].model_dump()}"
    full_prompt = SYSTEM_PROMPT + profile_info
    # Passiamo solo gli ultimi messaggi per evitare confusione cronologica
    response = llm.invoke([{"role": "system", "content": full_prompt}] + state["messages"][-6:])
    return {"messages": [response]}

def router_logic(state: AgentState) -> Literal["call_search", "call_scraper", "continue"]:
    last_msg = state["messages"][-1].content
    if "AZIONE: RICERCA" in last_msg: return "call_search"
    if "AZIONE: LEGGI" in last_msg: return "call_scraper"
    return "continue"

def search_node(state: AgentState):
    last_msg = state["messages"][-1].content
    query = last_msg.split("AZIONE: RICERCA")[-1].strip(" []")
    results = web_search_tool(query, max_results=5)
    
    # Etichettatura temporale chiara per evitare bug di cronologia
    obs = f"[RISULTATI ATTUALI PER LA TUA AZIONE DI RICERCA]:\n"
    for i, r in enumerate(results, 1):
        obs += f"\n- {r['title']}\n  Link: {r['link']}\n"
    
    return {"messages": [SystemMessage(content=obs)]}

def scraper_node(state: AgentState):
    last_msg = state["messages"][-1].content
    url = last_msg.split("AZIONE: LEGGI")[-1].strip(" []")
    content = scrape_website_tool(url)
    obs = f"[RISULTATI ATTUALI - CONTENUTO SITO]: {content[:1000]}"
    return {"messages": [SystemMessage(content=obs)]}

workflow = StateGraph(AgentState)
workflow.add_node("update_profile", profile_node)
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("search_tool", search_node)
workflow.add_node("scraper_tool", scraper_node)
workflow.set_entry_point("update_profile")
workflow.add_edge("update_profile", "analyzer")
workflow.add_conditional_edges("analyzer", router_logic, {"call_search": "search_tool", "call_scraper": "scraper_tool", "continue": END})
workflow.add_edge("search_tool", "analyzer")
workflow.add_edge("scraper_tool", "analyzer")
app_graph = workflow.compile()
