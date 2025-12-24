import streamlit as st
from api_client import send_message

# Configurazione pagina con icona standard (usiamo il codice testo dell'emoji per maggiore compatibilità)
st.set_page_config(
    page_title="Orientatore AI", 
    page_icon=":mortar_board:", # Codice standard Streamlit per il tocco accademico
    layout="wide"
)

# Sidebar: Visualizzazione dello Stato
st.sidebar.title("👤 Profilo Studente")
st.sidebar.info("Dati estratti in tempo reale:")

if "profile" not in st.session_state:
    st.session_state.profile = {}

# Mostriamo i dati nel tempo
for key, value in st.session_state.profile.items():
    if value:
        val_display = ", ".join(value) if isinstance(value, list) else value
        st.sidebar.write(f"**{key.replace('_', ' ').capitalize()}:** {val_display}")

# Intestazione con Logo e Titolo
st.markdown("# 🎓 Orientatore Post-Diploma")
st.caption("AI Agent basato su Framework LangGraph & Groq (Llama 3.3)")

# Inizializzazione cronologia
if "messages" not in st.session_state:
    st.session_state.messages = []

# Visualizzazione messaggi precedenti
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Utente
if prompt := st.chat_input("Scrivi qui le tue aspirazioni..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("L'orientatore sta analizzando le tue opzioni..."):
            data = send_message(prompt, st.session_state.messages, st.session_state.profile)
            response = data["response"]
            st.session_state.profile = data["profile"]
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
    st.rerun()
