import streamlit as st
from api_client import send_message

st.set_page_config(page_title="Orientatore Pro", page_icon=":mortar_board:", layout="wide")

if "messages" not in st.session_state: st.session_state.messages = []
if "profile" not in st.session_state: st.session_state.profile = {}
if "current_phase" not in st.session_state: st.session_state.current_phase = 1
if "phase_completion" not in st.session_state: st.session_state.phase_completion = 0.0
if "model_used" not in st.session_state: st.session_state.model_used = "-"

with st.sidebar:
    st.title("🎓 Stato")
    phases = ["Discovery", "Mapping", "Execution", "Decision"]
    st.write(f"**Fase:** {phases[st.session_state.current_phase-1]}")
    st.progress(st.session_state.phase_completion / 100)
    st.caption(f"Progresso: {st.session_state.phase_completion}%")
    st.divider()
    st.subheader("👤 Profilo")
    for k, v in st.session_state.profile.items():
        if v: st.write(f"**{k.capitalize()}:** {v}")
    if st.button("🗑️ Reset"):
        st.session_state.clear()
        st.rerun()

st.title("Orientatore Post-Diploma")
st.caption(f"Cervello: {st.session_state.model_used}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Rispondi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Validazione..."):
            data = send_message(prompt, st.session_state.messages, st.session_state.profile, st.session_state.current_phase, st.session_state.phase_completion)
            st.markdown(data["response"])
            st.session_state.profile = data["profile"]
            st.session_state.current_phase = data["current_phase"]
            st.session_state.phase_completion = data["phase_completion"]
            st.session_state.model_used = data["model_used"]
            st.session_state.messages.append({"role": "assistant", "content": data["response"]})
    st.rerun()
