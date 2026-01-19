# 🎓 AI Career Orienter: Architettura Agentica "Lean" & Resiliente

Questo progetto implementa un **Agente IA di Orientamento Post-Diploma** basato sui principi di **AI Engineering** (Chip Huyen, Capitolo 6). L'obiettivo è guidare gli studenti verso il lavoro, gli ITS o l'Università minimizzando il consumo di token e garantendo l'affidabilità dei dati.

## 🧠 Filosofia Progettuale (Framework Huyen)

A differenza dei chatbot tradizionali, questo sistema adotta un'architettura **multi-agente a controllo deterministico**, focalizzata su tre pilastri:

1.  **Context Efficiency (Pag. 218):** Invece di inviare tutta la cronologia della chat, il sistema usa uno **Stato Strutturato** (Pydantic) e invia solo gli ultimi messaggi. Questo riduce drasticamente il consumo di token e previene la confusione del modello.
2.  **Model Tiering (Pag. 265):** Utilizziamo modelli "Deboli" (Llama 8B) per compiti deterministici come l'estrazione dati (Parser) e modelli "Forti" (Llama 70B/Gemini Flash) per il ragionamento strategico (Orientatore).
3.  **Reliability & Fallback (Pag. 299):** Implementazione di una strategia di **High Availability**. Se Groq raggiunge i limiti di quota (Error 429), il sistema commuta istantaneamente su Google Gemini Flash senza interrompere l'esperienza utente.

## 🏗️ Architettura del Sistema

L'applicazione è strutturata in 4 livelli funzionali:

*   **Layer 1: Frontend (Streamlit):** Interfaccia utente trasparente che mostra in tempo reale il profilo estratto e il "livello di carburante" (token/richieste rimanenti).
*   **Layer 2: API Gateway (FastAPI):** Gestisce le sessioni e funge da ponte tra UI e logica agentica.
*   **Layer 3: Core Logic (LangGraph):** Orchestratore dei nodi (Parser -> Analyzer). Implementa la logica **Sticky Memory** per evitare la perdita di dati.
*   **Layer 4: Resources (Groq/Gemini/Tools):** Accesso ai modelli di fondazione e strumenti di ricerca web (DuckDuckGo).

## ⛽ Resource Management & Observability

Seguendo il concetto di **Observability** (pag. 289), il sistema include un monitoraggio real-time delle risorse:
*   **Fuel Gauge:** Visualizzazione del consumo cumulativo dei token Groq, persistente nel backend tramite `usage_stats.json`.
*   **Status Persistence:** I dati rimangono salvati anche in caso di riavvio del server o ricaricamento della pagina.

## 🛠️ Setup e Installazione

1.  **Installazione dipendenze:**
    ```bash
    pip install -r backend/requirements.txt && pip install -r frontend/requirements.txt
    ```
2.  **Variabili d'Ambiente:** Configura il file `.env` nella root con:
    *   `GROQ_API_KEY`
    *   `GOOGLE_API_KEY`
3.  **Avvio Backend:**
    ```bash
    PYTHONPATH=. python3 backend/app/main.py
    ```
4.  **Avvio Frontend:**
    ```bash
    streamlit run frontend/app.py
    ```

## 🛡️ Sicurezza e Integrità
- **Data Structural Integrity (Pag. 303):** Uso di Pydantic per validare ogni informazione estratta dallo studente.
- **Grounding:** L'agente è istruito a non richiedere dati già presenti nel profilo, eliminando le domande ridondanti.

---
*Progetto sviluppato come caso studio didattico per il corso di AI Engineering.*
