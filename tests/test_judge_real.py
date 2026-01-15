import pytest
from backend.app.agent.judge import judge_response

def test_eval_real_response():
    profilo = {"localita": "Milano", "interessi": ["Cybersecurity"]}
    query = "Qual è il sito di Cyberlys?"
    # Inseriamo la risposta che l'agente ti ha dato correttamente prima
    risposta_agente = "Il sito ufficiale di Cyberlys è https://www.cyberlys.it/. Si trovano a Milano e si occupano di consulenza."
    
    report = judge_response(profilo, query, risposta_agente)
    
    print(f"\n[REPORT REALE]: Voto Fedeltà {report.punteggio_fedelta}/5")
    print(f"Analisi: {report.analisi_critica}")
    assert report.punteggio_fedelta >= 4
