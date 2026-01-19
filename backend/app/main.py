import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from backend.app.agent.flow import app_graph
from backend.app.agent.state import StudentProfile
from backend.app.agent.usage import get_remaining_tokens
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'), override=True)
app = FastAPI()

class ChatInput(BaseModel):
    message: str
    history: List[Dict[str, str]] = []
    profile: Dict[str, Any] = {}

@app.get("/stats")
async def get_stats():
    """Restituisce i token reali dal file usage_stats.json (Huyen pag. 289)"""
    return {"groq_tokens_left": get_remaining_tokens()}

@app.post("/chat")
async def chat_endpoint(input_data: ChatInput):
    try:
        current_profile = StudentProfile(**input_data.profile)
        full_history = []
        for msg in input_data.history:
            role = HumanMessage if msg["role"] == "user" else AIMessage
            full_history.append(role(content=msg["content"]))
        full_history.append(HumanMessage(content=input_data.message))
        
        inputs = {
            "messages": full_history,
            "profile": current_profile,
            "groq_tokens_left": get_remaining_tokens(),
            "gemini_requests_left": 1500,
            "last_model_used": "-",
            "current_phase": 1,
            "phase_completion": 0.0,
            "iteration_count": 0,
            "next_action": "continue",
            "judge_feedback": None
        }
        
        result = await app_graph.ainvoke(inputs, {"configurable": {"thread_id": "session_lean"}})
        
        final_text = ""
        for m in reversed(result["messages"]):
            if isinstance(m, AIMessage):
                final_text = m.content
                break
        
        return {
            "response": final_text,
            "profile": result["profile"].model_dump(),
            "groq_tokens_left": get_remaining_tokens(),
            "last_model_used": result.get("last_model_used", "Groq")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
