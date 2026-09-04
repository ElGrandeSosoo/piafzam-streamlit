from pathlib import Path
import sys

import streamlit as st
import requests
import pandas as pd
from datetime import date, time
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from api_url import predict_url


# spell = st.secrets['spell']
# key = st.secrets.some_magic_api.key


st.title("PIAFZAM 🕊️")
st.caption("Quelle espèce d'oiseau est en train de chanter 🎵 ?")


# 1. Composant d'upload de fichier
uploaded_audio = st.file_uploader(
    "Choisissez un fichier audio depuis votre ordinateur",
    type=["wav", "mp3", "ogg", "m4a", "flac"],
    key="fichier_uploader",
)

# 2. Gestion de la session_state (clé distincte de l'onglet Piafzam)
if uploaded_audio is not None:
    st.session_state["fichier_uploaded_audio"] = uploaded_audio
elif "fichier_uploaded_audio" in st.session_state and uploaded_audio is None:
    del st.session_state["fichier_uploaded_audio"]

# 3. Traitement et envoi à l'API
if "fichier_uploaded_audio" in st.session_state:
    current_audio = st.session_state["fichier_uploaded_audio"]

    # Lecteur audio
    st.audio(current_audio)

    # Récupération du nom et du type MIME
    file_name = current_audio.name
    file_type = (
        current_audio.type if current_audio.type else "audio/wav"
    )

    # Dictionnaire multipart envoyé à FastAPI
    files = {
        "file": (
            file_name,
            current_audio.getvalue(),  # Envoie des octets (bytes)
            file_type,
        )
    }

    url = predict_url()

    # 4. Bouton de prédiction
    if st.button("Analyser l'audio", key="fichier_analyze"):
        with st.spinner("Analyse du fichier audio en cours..."):
            try:
                response = requests.post(url, files=files)

                if response.status_code == 200:
                    prediction = response.json()
                    st.success("Analyse terminée !")

                    # Affichage des résultats
                    st.markdown(f"### 🕊️ Cet oiseau est un : **{prediction['species']}**")
                    st.markdown(f"#### Plus communément appelé : *{prediction['scientific']}*")

                else:
                    st.error(
                        f"Erreur API ({response.status_code}) : {response.text}"
                    )

            except Exception as e:
                st.error(f"Impossible de contacter l'API : {e}")
