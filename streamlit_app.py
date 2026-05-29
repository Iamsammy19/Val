import streamlit as st
import anthropic
import os
import json
import zipfile
import uuid
import re
import base64
import random
import threading
import html as html_lib
import io as pyio
from datetime import datetime
from pathlib import Path

try:
    from duckduckgo_search import DDGS
    DDG_OK = True
except ImportError:
    DDG_OK = False

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="ZARA — Personal AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ====================== CSS (Your Original Beautiful Design) ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=DM+Mono:wght@300;400&display=swap');

:root {
  --gold: #C9A84C; --dark: #0A0A0A; --text: #E8E0D0; --muted: #7A7060;
}

html, body, [class*="css"] {
  background-color: var(--dark) !important;
  color: var(--text) !important;
  font-family: 'DM Mono', monospace;
}

.msg-bubble {
  max-width: 72%; padding: 14px 18px; border-radius: 2px; line-height: 1.7; font-size: 14px;
}
.msg-bubble.user { background: #1C1810; border-right: 2px solid var(--gold); }
.msg-bubble.ai { background: #101018; border-left: 2px solid #3A3A6A; }

.thinking-wrap {
  display: flex; align-items: center; gap: 12px; padding: 12px 20px;
  background: #101018; border-left: 3px solid #3A3A6A; border-radius: 2px;
  max-width: 280px;
}
</style>
""", unsafe_allow_html=True)

# ====================== ANIMATED LOGO ======================
LOGO = """
<div style="text-align:center; padding:20px 0 30px;">
  <div style="position:relative; width:90px; height:90px; margin:0 auto 12px;">
    <div style="position:absolute; inset:0; border:2px solid #C9A84C; border-radius:50%; animation: spin 3s linear infinite;"></div>
    <div style="position:absolute; inset:12px; border:2px solid #C9A84C; border-radius:50%; animation: spin 2s linear infinite reverse;"></div>
    <div style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center;">
      <span style="font-size:42px; color:#C9A84C;">⚡</span>
    </div>
  </div>
  <div style="font-family:'Cormorant Garamond', serif; font-size:32px; font-weight:600; letter-spacing:6px; color:#C9A84C;">ZARA</div>
  <div style="font-size:9px; color:#7A7060; letter-spacing:2px; text-transform:uppercase;">v5.7 • Personal AI</div>
</div>
"""

# ====================== SESSION STATE ======================
for key in ["messages", "profile", "tasks", "notes", "feedback", "rlhf"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ["messages", "tasks", "notes"] else {} if key in ["profile", "rlhf"] else {}

if "mode" not in st.session_state: st.session_state.mode = "💬 General"
if "api_key" not in st.session_state: st.session_state.api_key = os.getenv("ANTHROPIC_API_KEY", "")
if "chat_id" not in st.session_state: st.session_state.chat_id = str(uuid.uuid4())
if "voice_settings" not in st.session_state:
    st.session_state.voice_settings = {"input_enabled": True, "output_enabled": True}

# ====================== MODES ======================
MODES = {
    "💬 General": {"icon": "💬", "color": "#6A8FA0", "system": "You are ZARA..."},
    "🎨 UI/UX Design": {"icon": "🎨", "color": "#7A5A8A", "system": "You are a senior UI/UX designer..."},
    "💻 Full-Stack Dev": {"icon": "💻", "color": "#4A6A8A", "system": "You are a principal full-stack engineer..."},
    # Add other modes as needed
}

# ====================== HELPER FUNCTIONS ======================
def save_chat(cid, msgs, mode):
    Path("zara_history").mkdir(exist_ok=True)
    (Path("zara_history") / f"{cid}.json").write_text(json.dumps({
        "id": cid, "mode": mode, "messages": msgs, "updated": datetime.now().isoformat()
    }, indent=2))

def web_search(query):
    if not DDG_OK: return ""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=4))
            return "\n".join([f"{r.get('title')}: {r.get('body')[:200]}" for r in results])
    except:
        return ""

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown(LOGO, unsafe_allow_html=True)
    
    st.markdown("### Voice")
    st.session_state.voice_settings["input_enabled"] = st.toggle("🎤 Voice Input", True)
    st.session_state.voice_settings["output_enabled"] = st.toggle("🔊 Voice Output", True)

    st.markdown("### API")
    key = st.text_input("Anthropic API Key", value=st.session_state.api_key, type="password")
    if key: st.session_state.api_key = key

    st.markdown("### Mode")
    mode = st.radio("Mode", list(MODES.keys()), index=list(MODES.keys()).index(st.session_state.mode))
    if mode != st.session_state.mode:
        st.session_state.mode = mode
        st.rerun()

# ====================== MAIN CHAT ======================
_, col, _ = st.columns([1, 8, 1])
with col:
    st.markdown(f'<div style="text-align:center; font-size:42px; color:#C9A84C; margin-bottom:8px;">ZARA</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center; font-size:11px; color:#7A7060;">{st.session_state.mode}</div>', unsafe_allow_html=True)

    # Display messages
    for msg in st.session_state.messages:
        cls = "user" if msg["role"] == "user" else "ai"
        st.markdown(f'<div class="msg-wrap {cls}"><div class="msg-bubble {cls}">{msg["content"]}</div></div>', unsafe_allow_html=True)

    # Input
    user_input = st.text_input("Message ZARA", key="chat_input", placeholder="Speak or type...")
    send = st.button("Send")

    if send and user_input.strip():
        if not st.session_state.api_key:
            st.error("Please enter your Anthropic API key")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": user_input, "time": datetime.now().strftime("%H:%M")})

        try:
            client = anthropic.Anthropic(api_key=st.session_state.api_key)
            reply = ""
            with st.spinner("Thinking..."):
                response = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=4096,
                    system="You are ZARA, a highly intelligent personal AI assistant.",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    stream=True
                )
                for chunk in response:
                    if chunk.type == "content_block_delta":
                        reply += chunk.delta.text
                        # Simple live update
                        st.markdown(f"**ZARA:** {reply}")

            st.session_state.messages.append({"role": "assistant", "content": reply, "time": datetime.now().strftime("%H:%M")})

        except Exception as e:
            st.error(f"Error: {e}")

        st.rerun()

# Auto voice output (basic)
if st.session_state.voice_settings["output_enabled"] and st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    try:
        st.components.v1.html(f"""
        <script>
            const utterance = new SpeechSynthesisUtterance(`{st.session_state.messages[-1]["content"]}`);
            speechSynthesis.speak(utterance);
        </script>
        """, height=0)
    except:
        pass