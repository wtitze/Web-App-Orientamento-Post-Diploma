import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from backend.app.agent.flow import app_graph
from backend.app.agent.state import StudentProfile
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
        
        # --- CORREZIONE MEMORIA (Huyen Pag. 302) ---
        # Ricostruiamo la cronologia completa dai messaggi passati dal frontend
        full_history = []
        for msg in input_data.history:
            if msg["role"] == "user":
                full_history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                full_history.append(AIMessage(content=msg["content"]))
        
        # Aggiungiamo l'ultimo messaggio dell'utente
        full_history.append(HumanMessage(content=input_data.message))
        
        # Passiamo TUTTA la storia al grafo
        inputs = {
            "messages": full_history,
            "profile": current_profile 
        }
        
        config = {"configurable": {"thread_id": "session_1"}}
        result = await app_graph.ainvoke(inputs, config)
        
        return {
            "response": result["messages"][-1].content,
            "profile": result["profile"].model_dump()
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
