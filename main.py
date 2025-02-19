import streamlit as st
import openai
import requests
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

# Pydub requires ffmpeg or avplay to be installed
# Ensure ffmpeg is installed on your system

st.title("OpenAI Szöveg-Beszéd Streamlit Alkalmazás")

# API kulcs megadása
api_key = st.text_input("Add meg az OpenAI API kulcsodat:", type="password")

# Szöveg bevitele
text = st.text_area("Írd be a konvertálni kívánt szöveget:")

# Gomb a hang generálásához
if st.button("Hang generálása"):
    if not api_key:
        st.error("Kérlek, add meg az API kulcsodat!")
    elif not text:
        st.error("Kérlek, írj be szöveget!")
    else:
        # OpenAI API kulcs beállítása
        openai.api_key = api_key

        # API hívás a szöveg-beszéd konvertáláshoz
        try:
            response = openai.Audio.create(
                model="tts-1",
                input=text,
                voice="alloy"
            )

            # Az audio tartalom elérése
            audio_content = response['audio']

            # Az audio lejátszása
            audio = AudioSegment.from_file(BytesIO(audio_content), format="mp3")
            play(audio)

            # Az audio fájl letöltési lehetőségének biztosítása
            st.audio(audio_content, format='audio/mp3')
            st.success("A hang sikeresen legenerálva és lejátszva.")
        except Exception as e:
            st.error(f"Hiba történt a hang generálása során: {e}")
