"""Client Streamlit Cloud : fichier audio → API listen (VM).

Source de vérité dans le repo privé. Copie publique :
`make sync-streamlit-cloud` → `piafzam-streamlit/app.py`.
Aucun import `piafzam` : ce fichier doit rester copiable tel quel.
"""

from __future__ import annotations

import os

import requests
import streamlit as st

# On n'affiche une espèce que si BirdNET est assez sûr
MIN_SHOW = 0.10
DEFAULT_API = "https://piafzam.duckdns.org"

# page_config d'abord (Cloud refuse toute commande Streamlit avant).
st.set_page_config(page_title="PIAFZAM", page_icon="🪶", layout="centered")


def _secret(name: str, default: str = "") -> str:
    """Lit Streamlit secrets, sinon l'env, sinon le défaut."""
    try:
        value = st.secrets[name]
    except Exception:
        value = os.environ.get(name, default)
    return str(value or default).strip()


API = _secret("PIAFZAM_API", DEFAULT_API).rstrip("/")
DEMO_KEY = _secret("PIAFZAM_DEMO_KEY")
HEADERS = {"X-Demo-Key": DEMO_KEY} if DEMO_KEY else {}

st.markdown(
    """
    <div style="position:fixed;left:0;right:0;bottom:0.45rem;z-index:999;
                text-align:center;font-size:0.7rem;letter-spacing:0.18em;
                opacity:0.38;">
      <a href="https://piafzam.duckdns.org/" target="_top"
         style="color:inherit;text-decoration:none;">PIAFZAM 2.0</a>
    </div>
    """,
    unsafe_allow_html=True,
)
st.title("PIAFZAM")
st.caption("Quel oiseau chante dans cet enregistrement ?")

# 1. Upload
fichier = st.file_uploader(
    "Fichier audio",
    type=["wav", "mp3", "ogg", "flac", "m4a"],
)
if fichier is None:
    st.stop()

st.audio(fichier)

# 2. Appel API
if not st.button("Analyser", type="primary"):
    st.stop()

error = None
preds = []
with st.spinner("Analyse en cours…"):
    try:
        response = requests.post(
            f"{API}/listen/predict",
            files={"audio": (fichier.name, fichier.getvalue())},
            headers=HEADERS,
            timeout=120,
        )
        response.raise_for_status()
        preds = response.json().get("predictions") or []
    except requests.HTTPError:
        detail = response.text
        try:
            detail = response.json().get("detail", detail)
        except Exception:
            pass
        error = detail
    except Exception as exc:
        error = str(exc)

if error:
    st.error(error)
    st.stop()

# 3. Résultats (seuil MIN_SHOW)
shown = [p for p in preds if float(p.get("confidence") or 0) >= MIN_SHOW]
if not shown:
    st.warning("Rien de clair. Réessaie.")
    st.stop()

for pred in shown:
    name = pred.get("common") or pred.get("species") or pred.get("scientific") or ""
    conf = float(pred.get("confidence") or 0)
    st.subheader(f"{name} ({conf:.0%})")
