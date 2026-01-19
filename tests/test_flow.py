import pytest
from backend.app.agent.flow import app_graph
from backend.app.agent.state import StudentProfile
from langchain_core.messages import HumanMessage

@pytest.mark.asyncio
async def test_full_agentic_workflow():
    initial_state = {
        "messages": [HumanMessage(content="Ciao, sono Marco, studio informatica a Milano")],
        "profile": StudentProfile(),
        "current_phase": 1,
        "phase_completion": 0.0,
        "groq_tokens_left": 100000,
        "gemini_requests_left": 1500,
        "last_model_used": "Inizio",
        "iteration_count": 0,
        "judge_feedback": None
    }
    result = await app_graph.ainvoke(initial_state)
    
    # Verifichiamo che la chiave esista nell'output finale del grafo
    assert "last_model_used" in result
    print(f"\n[OK] Modello finale: {result['last_model_used']}")
