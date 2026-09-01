"""Client Streamlit Cloud : micro/fichier → API listen (VM).

Source de vérité dans le repo privé. Copie publique :
`make sync-streamlit-cloud` → `piafzam-streamlit/app.py`.
Aucun import `piafzam` : ce fichier doit rester copiable tel quel.
"""

from __future__ import annotations

import os

import requests
import streamlit as st

MIN_SHOW = 0.10
DEFAULT_API = "https://piafzam.duckdns.org"


def _secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets[name]
    except Exception:
        value = os.environ.get(name, default)
    return str(value or default).strip()


API = _secret("PIAFZAM_API", DEFAULT_API).rstrip("/")
DEMO_KEY = _secret("PIAFZAM_DEMO_KEY")
HEADERS = {"X-Demo-Key": DEMO_KEY} if DEMO_KEY else {}

st.set_page_config(page_title="piafzam")
st.title("piafzam")

blob = st.audio_input("enregistre un truc")
fichier = st.file_uploader("ou un fichier", type=["wav", "mp3", "ogg", "flac", "m4a"])
data = None
name = "clip.wav"
if blob is not None:
    data = blob.getvalue()
elif fichier is not None:
    data = fichier.getvalue()
    name = fichier.name or name

if data and st.button("analyser"):
    try:
        response = requests.post(
            f"{API}/listen/predict",
            files={"audio": (name, data)},
            headers=HEADERS,
            timeout=120,
        )
        response.raise_for_status()
    except requests.HTTPError:
        detail = response.text
        try:
            detail = response.json().get("detail", detail)
        except Exception:
            pass
        st.error(detail)
        st.stop()
    except Exception as error:
        st.error(str(error))
        st.stop()

    shown = [
        pred
        for pred in response.json().get("predictions") or []
        if float(pred.get("confidence") or 0) >= MIN_SHOW
    ]
    if not shown:
        st.warning("rien de clair. réessaie.")
    else:
        for pred in shown:
            scientific = pred.get("scientific") or ""
            common = pred.get("common") or scientific
            conf = float(pred.get("confidence") or 0)
            st.subheader(f"{common} ({conf:.0%})")
            st.write(scientific)
            slug = scientific.lower().replace(" ", "_")
            if slug:
                photo = requests.get(
                    f"{API}/listen/photos/{slug}",
                    headers=HEADERS,
                    timeout=10,
                )
                if photo.ok:
                    st.image(photo.content, width=280)
            wiki = scientific.replace(" ", "_")
            xc = scientific.replace(" ", "-")
            st.write(
                f"[wiki](https://fr.wikipedia.org/wiki/{wiki}) · "
                f"[xeno-canto](https://xeno-canto.org/species/{xc}) · "
                f"[inat](https://www.inaturalist.org/taxa?q={scientific})"
            )
