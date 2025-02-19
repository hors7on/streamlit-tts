import streamlit as st
from gtts import gTTS
import io

st.title("Text-to-Speech App")

text_input = st.text_area("Írd be a szöveget, amit hanggá szeretnél alakítani")
slow_mode = st.checkbox("Lassított beszéd", value=False)  # alapértelmezetten normál sebesség

if st.button("Átalakítás"):
    if not text_input:
        st.warning("Kérlek, adj meg egy szöveget!")
    else:
        tts = gTTS(text_input, lang='hu', slow=slow_mode)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.audio(audio_bytes, format="audio/mp3")
