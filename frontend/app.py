import streamlit as st
from api_client import send_message

st.set_page_config(page_title="Orientatore AI", page_icon="🎓", layout="wide")

# Sidebar: Visualizzazione dello Stato (Huyen: Transparency & Inspection - Pag. 289)
st.sidebar.title("👤 Profilo Studente")
st.sidebar.info("L'agente aggiorna questi dati in tempo reale analizzando la conversazione.")

if "profile" not in st.session_state:
    st.session_state.profile = {}

# Mostriamo i dati estratti nel tempo (Huyen: Data Structural Integrity - Pag. 303)
for key, value in st.session_state.profile.items():
    if value:
        # Trasformiamo la lista in stringa se necessario (es. per interessi)
        val_display = ", ".join(value) if isinstance(value, list) else value
        st.sidebar.write(f"**{key.capitalize()}:** {val_display}")

st.title("�� Orientatore Post-Diploma")
st.caption("AI Agent basato su Framework LangGraph & Groq")

# Inizializzazione cronologia
if "messages" not in st.session_state:
    st.session_state.messages = []

# Visualizzazione messaggi precedenti
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Utente
if prompt := st.chat_input("Scrivi qui le tue aspirazioni..."):
    # Mostra messaggio utente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chiamata al backend con il TERZO PARAMETRO (st.session_state.profile)
    with st.chat_message("assistant"):
        with st.spinner("L'orientatore sta pensando..."):
            # CORREZIONE QUI: aggiunto st.session_state.profile
            data = send_message(prompt, st.session_state.messages, st.session_state.profile)
            
            response = data["response"]
            st.session_state.profile = data["profile"]
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
    # Refresh per aggiornare la sidebar con i nuovi dati estratti
    st.rerun()
