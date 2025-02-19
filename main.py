import streamlit as st
from gtts import gTTS
import io
import time

# Ha nincs még queue, inicializáljuk
if 'audio_queue' not in st.session_state:
    st.session_state.audio_queue = []
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False

def generate_audio(text, slow):
    tts = gTTS(text, lang='hu', slow=slow)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

def on_enter():
    # Ha Enter lenyomásával aktiválódik a callback, hozzáadjuk az új audio-t a queue-hoz.
    if st.session_state.input_text.strip():
        audio = generate_audio(st.session_state.input_text, st.session_state.slow)
        st.session_state.audio_queue.append(audio)
        st.session_state.input_text = ""  # Töröljük a mezőt

# Szövegbevitel on_change callback-kel
st.text_input("Írd be a szöveget", key="input_text", on_change=on_enter)

# Lassított beszéd kapcsoló (alapértelmezett normál sebesség)
st.checkbox("Lassított beszéd", key="slow", value=False)

# Ha nincs lejátszás folyamatban, és van audio a queue-ban, akkor játsszuk le a következőt
if not st.session_state.is_playing and st.session_state.audio_queue:
    current_audio = st.session_state.audio_queue.pop(0)
    st.session_state.is_playing = True
    st.audio(current_audio, format="audio/mp3")
    
    # Egyszerűsített várakozás – itt egy fix 3 másodperces késleltetés (a valóságban érdemes lenne a szöveg hosszától függően számolni)
    time.sleep(3)
    st.session_state.is_playing = False
    st.experimental_rerun()

# JavaScript snippet, ami automatikusan fókuszálja a szövegmezőt az újrainduláskor
st.markdown("""
<script>
  const input = window.parent.document.querySelector('input[type="text"]');
  if(input){
      input.focus();
  }
</script>
""", unsafe_allow_html=True)
