import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from backend.app.agent.flow import app_graph
from backend.app.agent.state import StudentProfile
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'), override=True)
app = FastAPI()

class ChatInput(BaseModel):
    message: str
    history: List[Dict[str, str]] = []
    profile: Dict[str, Any] = {}
    current_phase: int = 1
    phase_completion: float = 0.0

@app.post("/chat")
async def chat_endpoint(input_data: ChatInput):
    try:
        # Inizializziamo lo stato con i dati persistenti
        current_profile = StudentProfile(**input_data.profile)
        
        full_history = []
        for msg in input_data.history:
            role = HumanMessage if msg["role"] == "user" else AIMessage
            full_history.append(role(content=msg["content"]))
        full_history.append(HumanMessage(content=input_data.message))
        
        # Stato iniziale per LangGraph
        inputs = {
            "messages": full_history,
            "profile": current_profile,
            "current_phase": input_data.current_phase,
            "phase_completion": input_data.phase_completion,
            "iteration_count": 0,
            "judge_feedback": None,
            "model_used": ""
        }
        
        # Esecuzione del Grafo
        config = {"configurable": {"thread_id": "session_phases"}}
        result = await app_graph.ainvoke(inputs, config)
        
        # Estraiamo la risposta pulita
        final_text = ""
        for m in reversed(result["messages"]):
            if isinstance(m, AIMessage) and "AZIONE:" not in m.content.upper():
                final_text = m.content
                break
        
        return {
            "response": final_text or "L'orientatore sta elaborando la strategia...",
            "profile": result["profile"].model_dump(),
            "current_phase": result.get("current_phase", 1),
            "phase_completion": result.get("phase_completion", 0.0),
            "judge_feedback": result.get("judge_feedback"),
            "model_used": result.get("model_used", "N/A")
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
