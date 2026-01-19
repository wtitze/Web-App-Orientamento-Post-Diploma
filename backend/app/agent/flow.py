import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, AIMessage
from backend.app.agent.usage import get_remaining_tokens, update_remaining_tokens
from backend.app.agent.state import AgentState, StudentProfile
from backend.app.agent.prompts import SYSTEM_PROMPT

load_dotenv(os.path.join(os.getcwd(), '.env'), override=True)

groq_strong = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"), temperature=0.1)
gemini_fallback = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.1)

def universal_proxy(state, prompt, task_type="strong", schema=None):
    tokens_left = get_remaining_tokens()
    try:
        if tokens_left < 1500: raise Exception("Fuel Low")
        model = groq_strong
        if schema: model = model.with_structured_output(schema)
        res = model.invoke(prompt)
        used = res.usage_metadata.get("total_tokens", 500) if hasattr(res, "usage_metadata") else 500
        update_remaining_tokens(tokens_left - used)
        return res, "Groq", used
    except:
        model = gemini_fallback
        if schema: model = model.with_structured_output(schema)
        res = model.invoke(prompt)
        return res, "Gemini", 0

def profile_node(state: AgentState):
    from backend.app.agent.parser import extract_profile_logic
    new_profile, tokens = extract_profile_logic(state["messages"], state["profile"], universal_proxy, state)
    return {"profile": new_profile}

def analyzer_node(state: AgentState):
    p = state['profile']
    # --- GROUNDING ESTREMO ---
    # Costruiamo una stringa di "Dati Proibiti" (Huyen pag. 253)
    known = []
    if p.residenza_attuale: known.append(f"Città: {p.residenza_attuale}")
    if p.diploma_conseguito: known.append(f"Diploma: {p.diploma_conseguito}")
    if p.settore_di_interesse: known.append(f"Settore: {p.settore_di_interesse}")
    
    info_context = " | ".join(known) if known else "Nessuna info."
    instruction = f"\n\n[MEMORIA DI SISTEMA - NON CHIEDERE QUESTI DATI]: {info_context}\n\nSe i dati sopra sono completi, proponi azioni o approfondisci i sogni."
    
    full_prompt = SYSTEM_PROMPT + instruction
    res, m_name, used = universal_proxy(state, [SystemMessage(content=full_prompt)] + state["messages"][-3:])
    return {"messages": [res], "last_model_used": m_name}

workflow = StateGraph(AgentState)
workflow.add_node("update_profile", profile_node)
workflow.add_node("analyzer", analyzer_node)
workflow.set_entry_point("update_profile")
workflow.add_edge("update_profile", "analyzer")
workflow.add_edge("analyzer", END)
app_graph = workflow.compile()
