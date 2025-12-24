# AI Career Orienter: Agente IA di Orientamento Post-Diploma

Progetto basato sui principi di **AI Engineering (Chip Huyen, Cap. 6)** per l'orientamento degli studenti verso Lavoro, ITS o Università.

## 🚀 Stato del Progetto
- [x] **Memory Management (State):** Persistenza del profilo tra i turni della chat (Huyen pag. 302).
- [x] **Tool Inventory:** Ricerca live (DDG) e Deep Scraper (BS4) con formattazione dei link ottimizzata (Huyen pag. 279).
- [x] **Agentic Flow:** Implementato pattern ReAct con limiti di ricorsione per prevenire loop infiniti (Huyen pag. 291).
- [x] **Model Update:** Utilizzo di `llama-3.3-70b-versatile` per ragionamento e pianificazione avanzata.
- [x] **Frontend & Backend:** Web App completa con visualizzazione dello stato in tempo reale.

## 🛠 Setup e Installazione
1. **Dipendenze:** `pip install -r backend/requirements.txt && pip install -r frontend/requirements.txt`
2. **API Key:** Inserire `GROQ_API_KEY` in `backend/.env`.

## 🧠 Innovazioni Architetturali (Framework Huyen)
- **Tool Reliability (Pag. 299):** Gestione dei blocchi (User-Agent) e dei fallimenti di recupero tramite formattazione esplicita dei link.
- **Decoupling Planning (Pag. 282):** Separazione netta tra l'analisi del profilo studente e l'azione di ricerca web.
- **Reflection Loop (Pag. 293):** L'agente verifica i fatti tramite lo scraper prima di fornire una risposta definitiva.

## 🧪 Validazione
Eseguire i test per verificare l'integrità del sistema:
```bash
PYTHONPATH=. python3 -m pytest tests/
```
