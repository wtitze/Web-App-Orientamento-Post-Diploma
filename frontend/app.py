import streamlit as st
import requests
from api_client import send_message

st.set_page_config(page_title="Orientatore Pro", page_icon=":mortar_board:", layout="wide")

# --- FUNZIONE PER RECUPERARE STATS INIZIALI ---
def fetch_initial_stats():
    try:
        res = requests.get("http://localhost:8000/stats")
        return res.json().get("groq_tokens_left", 100000)
    except:
        return 100000

if "messages" not in st.session_state: st.session_state.messages = []
if "profile" not in st.session_state: st.session_state.profile = {}
# Carica i token reali all'avvio
if "groq_fuel" not in st.session_state: st.session_state.groq_fuel = fetch_initial_stats()
if "last_model" not in st.session_state: st.session_state.last_model = "-"

with st.sidebar:
    st.title("📊 Monitor Risorse")
    st.write(f"⛽ Groq: {st.session_state.groq_fuel:,} token")
    st.progress(max(0.0, min(st.session_state.groq_fuel / 100000, 1.0)))
    
    st.divider()
    st.subheader("👤 Profilo Studente")
    display_data = {k: v for k, v in st.session_state.profile.items() if v and v != "None" and v != []}
    if display_data:
        for k, v in display_data.items():
            st.write(f"**{k.replace('_', ' ').capitalize()}:** {v}")
    else:
        st.info("Inizia a parlare...")

    if st.button("🗑️ Reset Totale"):
        st.session_state.clear()
        st.rerun()

st.title("🎓 Orientatore IA")
st.caption(f"Cervello attivo: {st.session_state.last_model}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Scrivi qui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        data = send_message(prompt, st.session_state.messages, st.session_state.profile, 1, 0, 0)
        st.markdown(data["response"])
        st.session_state.profile = data["profile"]
        st.session_state.groq_fuel = data["groq_tokens_left"]
        st.session_state.last_model = data["last_model_used"]
        st.session_state.messages.append({"role": "assistant", "content": data["response"]})
    st.rerun()
