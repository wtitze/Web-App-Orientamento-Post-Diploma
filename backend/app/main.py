import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from backend.app.agent.flow import app_graph
from backend.app.agent.state import StudentProfile
from backend.app.agent.judge import judge_response
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

class ChatInput(BaseModel):
    message: str
    history: List[Dict[str, str]] = []
    profile: Dict[str, Any] = {}

@app.post("/chat")
async def chat_endpoint(input_data: ChatInput):
    try:
        current_profile = StudentProfile(**input_data.profile)
        full_history = []
        for msg in input_data.history:
            if msg["role"] == "user":
                full_history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                full_history.append(AIMessage(content=msg["content"]))
        full_history.append(HumanMessage(content=input_data.message))
        
        inputs = {"messages": full_history, "profile": current_profile}
        config = {"configurable": {"thread_id": "session_1"}}
        
        # 1. Esecuzione Orientatore
        result = await app_graph.ainvoke(inputs, config)
        final_response = result["messages"][-1].content
        
        # 2. Esecuzione Giudice (Mandatoria)
        evaluation = judge_response(result["profile"].model_dump(), input_data.message, final_response)
        
        # LOG DI DEBUG NEL TERMINALE
        print(f"GIUDICE DICE: {evaluation.punteggio_fedelta}/5")

        return {
            "response": final_response,
            "profile": result["profile"].model_dump(),
            "judge_report": evaluation.model_dump()
        }
    except Exception as e:
        print(f"ERRORE BACKEND: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
