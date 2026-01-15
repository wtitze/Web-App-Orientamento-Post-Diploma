import streamlit as st
from api_client import send_message

st.set_page_config(page_title="Orientatore AI + Judge", page_icon=":mortar_board:", layout="wide")

# Pulsante di Reset Totale
if st.sidebar.button("🗑️ Ricomincia da zero"):
    st.session_state.messages = []
    st.session_state.profile = {}
    st.session_state.last_report = None
    st.rerun()

st.sidebar.title("👤 Profilo Studente")
if "profile" not in st.session_state: st.session_state.profile = {}
for key, value in st.session_state.profile.items():
    if value:
        val_display = ", ".join(value) if isinstance(value, list) else value
        st.sidebar.write(f"**{key.replace('_', ' ').capitalize()}:** {val_display}")

st.title("🎓 Orientatore con Supervisione IA")

if "messages" not in st.session_state: st.session_state.messages = []
if "last_report" not in st.session_state: st.session_state.last_report = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Scrivi qui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("L'orientatore sta verificando i dati..."):
            data = send_message(prompt, st.session_state.messages, st.session_state.profile)
            st.markdown(data["response"])
            st.session_state.last_report = data.get("judge_report")
            st.session_state.profile = data["profile"]
            st.session_state.messages.append({"role": "assistant", "content": data["response"]})
    st.rerun()

if st.session_state.last_report:
    with st.expander("🔍 VALUTAZIONE TECNICA DELLA RISPOSTA", expanded=True):
        r = st.session_state.last_report
        c1, c2 = st.columns(2)
        c1.metric("Fedeltà ai vincoli", f"{r.get('punteggio_fedelta', 0)}/5")
        c2.metric("Efficienza", f"{r.get('punteggio_efficienza', 0)}/5")
        st.info(f"**Analisi del Giudice:** {r.get('analisi_critica', 'N/A')}")
