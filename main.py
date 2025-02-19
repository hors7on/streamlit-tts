import streamlit as st
from gtts import gTTS
import io

st.title("Text-to-Speech App")

def generate_audio():
    if st.session_state.input_text.strip():
        tts = gTTS(st.session_state.input_text, lang='hu', slow=st.session_state.slow_mode)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.session_state.audio_bytes = audio_bytes
        st.session_state.input_text = ""  # törli a bevitelt

# Az enter lenyomására automatikusan lefut a callback
st.text_input("Írd be a szöveget", key="input_text", on_change=generate_audio)
st.checkbox("Lassított beszéd", key="slow_mode", value=False)

if "audio_bytes" in st.session_state:
    st.audio(st.session_state.audio_bytes, format="audio/mp3")
