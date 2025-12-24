from ddgs import DDGS
from typing import List, Dict

def web_search_tool(query: str, max_results: int = 5) -> List[Dict]:
    """
    Esegue una ricerca su DuckDuckGo e restituisce i risultati più rilevanti.
    Ideale per trovare bandi ITS, università e aziende locali.
    """
    results = []
    try:
        with DDGS() as ddgs:
            # region='it-it' forza la ricerca in italiano per trovare ITS e aziende locali
            ddgs_gen = ddgs.text(query, region='it-it', safesearch='off', timelimit='y', max_results=max_results)
            for r in ddgs_gen:
                results.append({
                    "title": r.get("title"),
                    "link": r.get("href"),
                    "snippet": r.get("body")
                })
    except Exception as e:
        print(f"Errore durante la ricerca: {e}")
    
    return results

if __name__ == "__main__":
    # Test rapido manuale
    print(web_search_tool("Migliori ITS informatica Milano 2025"))
