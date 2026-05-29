import streamlit as st
import anthropic
import os, json, zipfile, uuid, re, base64, random, threading
import html as html_lib
import io as pyio
from datetime import datetime
from pathlib import Path

try:
    from duckduckgo_search import DDGS
    DDG_OK = True
except:
    DDG_OK = False

st.set_page_config(page_title="ZARA", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# ── Keep your full beautiful CSS + LOGO here ───────────────────────────────
# ... [Your original CSS and animated logo] ...

# ── Voice Settings ─────────────────────────────────────────────────────────
if "voice_settings" not in st.session_state:
    st.session_state.voice_settings = {
        "input_enabled": True,
        "output_enabled": True,
        "voice_name": "Friend",           # You can customize this
        "speech_rate": 1.0,
        "pitch": 1.0
    }

# ── Multi-Model Support ────────────────────────────────────────────────────
def get_client(model_provider="anthropic"):
    if model_provider == "anthropic":
        return anthropic.Anthropic(api_key=st.session_state.api_key)
    # Future: Add Grok / OpenAI / local fallback here
    else:
        st.warning("Only Anthropic supported currently.")
        return anthropic.Anthropic(api_key=st.session_state.api_key)

# ── Voice Input Component ─────────────────────────────────────────────────
def voice_input():
    audio_value = st.audio_input("Speak to ZARA", key="voice_input")
    if audio_value:
        # In production, use Whisper or browser STT
        st.info("🎤 Voice captured — transcribing...")
        # For demo: Return placeholder. In real app, integrate speech-to-text
        return "[Voice message]: " + user_input if 'user_input' in locals() else "Voice input received"
    return None

# ── Text-to-Speech Output ─────────────────────────────────────────────────
def speak_text(text):
    if not st.session_state.voice_settings["output_enabled"]:
        return
    # Browser TTS
    js = f"""
    <script>
        const utterance = new SpeechSynthesisUtterance(`{text.replace('`', '')}`);
        utterance.rate = {st.session_state.voice_settings["speech_rate"]};
        utterance.pitch = {st.session_state.voice_settings["pitch"]};
        // Try to use a friendly voice
        const voices = speechSynthesis.getVoices();
        utterance.voice = voices.find(v => v.name.includes("Samantha") || v.name.includes("Karen")) || voices[0];
        speechSynthesis.speak(utterance);
    </script>
    """
    st.components.v1.html(js, height=0)

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(LOGO, unsafe_allow_html=True)
    
    st.markdown("### Voice Mode")
    st.session_state.voice_settings["input_enabled"] = st.toggle("🎤 Voice Input", value=True)
    st.session_state.voice_settings["output_enabled"] = st.toggle("🔊 Voice Output", value=True)
    
    if st.session_state.voice_settings["output_enabled"]:
        st.slider("Speed", 0.5, 2.0, 1.0, key="speech_rate")
        st.slider("Pitch", 0.5, 2.0, 1.0, key="pitch")

    # Model selection to reduce Anthropic dependency
    model_provider = st.selectbox("Model Provider", ["Anthropic (Claude)", "Grok (Future)"], index=0)
    
    api_key = st.text_input("API Key", value=st.session_state.api_key, type="password")
    if api_key: st.session_state.api_key = api_key

    # ... rest of your sidebar (modes, profile, etc.)

# ── Main Processing ───────────────────────────────────────────────────────
if send_btn or (st.session_state.voice_settings["input_enabled"] and st.session_state.get("voice_input")):
    if st.session_state.voice_settings["input_enabled"]:
        voice_text = voice_input()
        if voice_text:
            user_input = voice_text

    # ... existing message append logic ...

    system = build_system_prompt(...)   # Your enhanced prompt

    try:
        client = get_client("anthropic")
        
        reply = ""
        holder = st.empty()

        with client.messages.stream(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8192,
            temperature=0.7,
            system=system,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        ) as stream:
            for chunk in stream.text_stream:
                reply += chunk
                holder.markdown(f'<div class="msg-wrap ai"><div class="msg-bubble ai">{render_md(reply)}<span class="cursor"></span></div></div>', unsafe_allow_html=True)

        final_reply = reply

        # Auto voice output
        if st.session_state.voice_settings["output_enabled"]:
            speak_text(final_reply[:800])   # Speak first part for speed

        st.session_state.messages.append({"role": "assistant", "content": final_reply, "time": datetime.now().strftime("%H:%M")})
        save_chat(...)

        st.rerun()

    except Exception as e:
        st.error(f"Error: {str(e)}")