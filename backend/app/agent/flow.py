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
from backend.app.agent.judge import audit_phase_logic

load_dotenv(os.getcwd(), override=True)

groq_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1, request_timeout=15)
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest", 
    temperature=0.1, 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def universal_call(prompts, structured_schema=None):
    try:
        model = groq_llm
        if structured_schema: model = model.with_structured_output(structured_schema)
        return model.invoke(prompts), "Groq (Llama 70B)"
    except Exception as e:
        print(f"--- FALLBACK ATTIVATO ---")
        model = gemini_llm
        if structured_schema: model = model.with_structured_output(structured_schema)
        return model.invoke(prompts), "Gemini (Flash Latest)"

def profile_node(state: AgentState):
    # Applichiamo la logica Sticky del parser (definita nel file parser.py aggiornato)
    new_profile = extract_profile_logic(state["messages"], state["profile"], universal_call)
    return {"profile": new_profile}

def analyzer_node(state: AgentState):
    phase = state.get("current_phase", 1)
    feedback = f"\n[FEEDBACK GIUDICE]: {state.get('judge_feedback')}" if state.get('judge_feedback') else ""
    full_prompt = SYSTEM_PROMPT + f"\n\nFASE ATTUALE: {phase}{feedback}\nPROFILO: {state['profile'].model_dump()}"
    res, m_name = universal_call([SystemMessage(content=full_prompt)] + state["messages"][-5:])
    return {"messages": [res], "model_used": m_name}

def judge_node(state: AgentState):
    report = audit_phase_logic(state['profile'].model_dump(), state['current_phase'], state['messages'][-1].content)
    current_p = state['current_phase']
    new_p = current_p
    if report.can_move_to_next and current_p < 4:
        new_p = current_p + 1
    return {
        "phase_completion": report.percentage,
        "current_phase": new_p,
        "judge_feedback": report.feedback_for_agent
    }

workflow = StateGraph(AgentState)
workflow.add_node("update_profile", profile_node)
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("judge", judge_node)
workflow.set_entry_point("update_profile")
workflow.add_edge("update_profile", "analyzer")
workflow.add_edge("analyzer", "judge")
workflow.add_edge("judge", END)
app_graph = workflow.compile()
