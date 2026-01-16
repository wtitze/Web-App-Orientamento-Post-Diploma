import streamlit as st
from api_client import send_message

st.set_page_config(page_title="Orientatore AI + Dual Model", page_icon=":mortar_board:", layout="wide")

if st.sidebar.button("🗑️ Reset Sessione"):
    st.session_state.messages = []
    st.session_state.profile = {}
    st.session_state.last_report = None
    st.rerun()

st.sidebar.title("👤 Profilo")
if "profile" not in st.session_state: st.session_state.profile = {}
for k, v in st.session_state.profile.items():
    if v: st.sidebar.write(f"**{k.capitalize()}:** {v}")

st.title("🎓 Orientatore con Fallback Gemini")

if "messages" not in st.session_state: st.session_state.messages = []
if "last_report" not in st.session_state: st.session_state.last_report = None
if "orientatore_model" not in st.session_state: st.session_state.orientatore_model = ""

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Scrivi qui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("L'orientatore sta elaborando..."):
            data = send_message(prompt, st.session_state.messages, st.session_state.profile)
            st.markdown(data["response"])
            st.session_state.last_report = data.get("judge_report")
            st.session_state.orientatore_model = data.get("orientatore_model")
            st.session_state.profile = data["profile"]
            st.session_state.messages.append({"role": "assistant", "content": data["response"]})
    st.rerun()

if st.session_state.last_report:
    r = st.session_state.last_report
    with st.expander("🔍 INFO TECNICHE E QUALITÀ", expanded=True):
        st.write(f"🧠 **Modello Orientatore:** {st.session_state.orientatore_model}")
        st.write(f"⚖️ **Modello Giudice:** {r.get('model_used')}")
        st.divider()
        if r.get("violazione_protocollo"):
            st.error(f"Violazione Protocollo: {r.get('analisi_critica')}")
        else:
            c1, c2 = st.columns(2)
            c1.metric("Fedeltà", f"{r.get('punteggio_fedelta')}/5")
            c2.metric("Efficienza", f"{r.get('punteggio_efficienza', 0)}/5")
            st.info(f"**Analisi del Giudice:** {r.get('analisi_critica')}")
