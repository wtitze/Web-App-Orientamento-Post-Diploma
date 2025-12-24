import pytest
from backend.app.tools.scraper import scrape_website_tool

def test_scraper_success():
    """
    Verifica che lo scraper legga correttamente una pagina.
    Usiamo un sito standard per i test di scraping.
    """
    url = "https://www.example.com"
    content = scrape_website_tool(url)
    
    assert isinstance(content, str)
    assert len(content) > 10
    assert "Example Domain" in content

def test_scraper_real_site():
    """Test su un sito universitario per verificare l'estrazione"""
    url = "https://www.unimi.it/it/corsi/orientamento"
    content = scrape_website_tool(url)
    
    # Se il sito è giù o blocca, il test non deve fallire il codice, 
    # ma verifichiamo che la risposta sia coerente
    assert isinstance(content, str)
    if "Errore" not in content:
        assert len(content) > 50
