import pytest
from backend.app.tools.search import web_search_tool

def test_web_search_returns_results():
    """Verifica che il tool di ricerca restituisca dei risultati per una query standard"""
    results = web_search_tool("ITS Meccatronica Veneto", max_results=2)
    
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
    assert "link" in results[0]
    assert "snippet" in results[0]

def test_web_search_empty_query():
    """Verifica il comportamento con una query vuota (non dovrebbe crashare)"""
    results = web_search_tool("", max_results=1)
    assert isinstance(results, list)

def test_web_search_content():
    """Verifica che i risultati contengano link validi (stringhe che iniziano con http)"""
    results = web_search_tool("Università di Pisa", max_results=1)
    if results:
        assert results[0]["link"].startswith("http")
