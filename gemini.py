import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Gemini Pro Advanced Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ===================== API KEY (SAFE WAY) =====================
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("API Key missing! Add GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("# Gemini Pro Advanced")
    st.markdown("### University Project 2025")
    st.markdown("**Features:**")
    st.success("Multi-turn Chat\nChat Export\nModel Selection\nUrdu + English\nClean UI")
    
    # Updated Model Options (2025 Stable)
    model_option = st.selectbox(
        "Select Model",
        [
            "gemini-2.0-flash",  # Fast & Recommended
            "gemini-2.5-flash-lite",  # Cost-effective
            "gemini-2.5-pro"  # Powerful
        ],
        index=0
    )
    
    # Creativity Slider
    temperature = st.slider("Creativity", 0.0, 1.0, 0.7, 0.1)
    
    # Clear Chat Button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.success("Chat cleared!")
        st.rerun()
    
    # Export Chat Button
    if st.button("Download Chat (JSON)"):
        if "messages" in st.session_state and st.session_state.messages:
            st.download_button(
                label="Click to Download",
                data=json.dumps(st.session_state.messages, indent=2, ensure_ascii=False),
                file_name=f"gemini_chat_{datetime.now().strftime('%Y-%m-%d_%H%M')}.json",
                mime="application/json"
            )

# ===================== CHAT START =====================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Salam! Main **Gemini Pro Advanced Assistant** hun.\n"
                   "University project ke liye banaya gaya hun.\n\n"
                   "Mujhse coding, assignment, research, ya koi bhi sawal pooch sakte ho!\n"
                   "English aur Urdu dono mein baat kar sakta hun 🤖"
    }]

# ===================== MODEL SETTINGS =====================
model = genai.GenerativeModel(
    model_name=model_option,
    generation_config={
        "temperature": temperature,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 2048,  # Safe for 2025 models
    }
)

# ===================== BEAUTIFUL UI =====================
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
    .title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.6);
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #ddd;
        font-style: italic;
        margin-bottom: 30px;
    }
    .st-emojize .css-1e6qvis { font-size: 2rem; }
</style>
""", unsafe_allow_html=True)
st.markdown('<h1 class="title">Gemini Pro Advanced</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by Google Gemini • Made for University Project</p>', unsafe_allow_html=True)

# ===================== SHOW OLD MESSAGES =====================
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message["content"])

# ===================== USER INPUT =====================
if prompt := st.chat_input("Yahan message likhein... (Urdu + English)"):
    # User ka message save + dikhao
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # AI se jawab lo
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Jawab soch raha hun..."):
            try:
                # Fixed Chat History
                chat_history = []
                for msg in st.session_state.messages[:-1]:
                    role = "user" if msg["role"] == "user" else "model"
                    chat_history.append({
                        "role": role,
                        "parts": [msg["content"]]
                    })
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(prompt)
                reply = response.text
                # AI ka jawab save karo
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.markdown(reply)
            except Exception as e:
                st.error("Kuch galat ho gaya. Dobara try karein!")
                st.write("Error:", str(e))  # Debug ke liye, production mein hata do            
