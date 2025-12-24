import pytest
from backend.app.agent.flow import app_graph

def test_full_graph_structure():
    """Verifica che tutti i nodi professionali siano nel grafo"""
    nodes = app_graph.nodes
    expected = ["update_profile", "analyzer", "search_tool", "scraper_tool"]
    for node in expected:
        assert node in nodes

def test_router_branching():
    """Verifica che il router riconosca i diversi intenti di ricerca"""
    from backend.app.agent.flow import router_logic
    from langchain_core.messages import AIMessage
    from backend.app.agent.state import StudentProfile

    def create_state(text):
        return {"messages": [AIMessage(content=text)], "profile": StudentProfile()}

    assert router_logic(create_state("Ora ricerca ITS a Roma")) == "call_search"
    assert router_logic(create_state("Devo approfondisci link: http://test.it")) == "call_scraper"
    assert router_logic(create_state("Ecco il tuo consiglio...")) == "continue"
