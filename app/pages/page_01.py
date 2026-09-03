import streamlit as st
import requests
import pandas as pd
from datetime import date, time
import numpy as np


# spell = st.secrets['spell']
# key = st.secrets.some_magic_api.key


st.title("PIAFZAM 🕊️")
st.caption("Quelle espèce d'oiseau est en train de chanter 🎵 ?")

# 1. Enregistrement audio
audio_value = st.audio_input("Record high quality audio", sample_rate=44100)

# 2. Sauvegarde dans la session state pour ne pas le perdre au clic
if audio_value is not None:
    st.session_state["recorded_audio"] = audio_value

# 3. Si un audio est présent en mémoire
if "recorded_audio" in st.session_state:
    current_audio = st.session_state["recorded_audio"]
    st.audio(current_audio)

    # Préparation du fichier
    file_type = (
        current_audio.type if hasattr(current_audio, "type") else "audio/wav"
    )
    file_extension = file_type.split("/")[-1]


    files = {
        "file": (
            f"recording.{file_extension}",
            current_audio.getvalue(),
            file_type,
        )
    }

    url = st.secrets["api_url"]  # Vérifiez votre URL API

    # 4. Le bouton s'appuie sur la mémoire de session
    if st.button("Analyser l'audio"):
        with st.spinner("Analyse en cours..."):
            try:
                response = requests.post(url, files=files)

                if response.status_code == 200:
                    prediction = response.json()
                    st.success("Analyse terminée !")

                    st.markdown(f"### 🕊️ Cet oiseau est un : **{prediction['species']}**")
                    st.markdown(f"#### Plus communément appelé : *{prediction['scientific']}*")
                else:
                    st.error(f"Erreur API ({response.status_code}) : {response.text}")

            except Exception as e:
                st.error(f"Impossible de contacter l'API : {e}")
