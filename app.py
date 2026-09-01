"""Frontend Streamlit — même contrat que `taxifare-website` au bootcamp.

Pas de TensorFlow. On appelle `piafzam.api.fast` en HTTP (`POST /predict`).
Local : `make api` puis `make demo`. Cloud : le même fichier, secret `PIAFZAM_API`.
"""

from __future__ import annotations

import os
from pathlib import Path

import requests
import streamlit as st

# page_config d'abord (Cloud refuse toute commande Streamlit avant).
# page_title = titre de la carte Slack / Discord (Streamlit Cloud).
_ICON = Path(__file__).with_name("icon.png")
st.set_page_config(
    page_title="Piafzam — quel oiseau est sur ce spectrogramme ?",
    page_icon=str(_ICON) if _ICON.is_file() else "🪶",
    layout="centered",
)

# dotenv optionnel : en local on lit .env ; sur Cloud le paquet n'est pas installé.
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# On n'affiche une espèce que si le CNN est assez sûr
MIN_SHOW = 0.10

# url = 'https://taxifare.lewagon.ai/predict'
# Local : http://127.0.0.1:8000 — Cloud : secret console PIAFZAM_API (pas de toml dans le repo)
_secret_api = ""
try:
    # Streamlit Cloud : secret console. En local, pas de secrets.toml → on ignore.
    if st.secrets.load_if_toml_exists():
        _secret_api = str(st.secrets.get("PIAFZAM_API") or "")
except Exception:
    _secret_api = ""
API = str(_secret_api or os.environ.get("PIAFZAM_API") or "http://127.0.0.1:8000").strip().rstrip("/")
PREDICT_URL = f"{API}/predict"

# Lien discret vers l'écoute micro (front FastAPI), hors de cette démo spectro.
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
st.caption("Quel oiseau est sur ce spectrogramme ?")

# 1. Contrôleurs (upload) — PNG / JPG, pas d'audio
fichier = st.file_uploader(
    "Spectrogramme",
    type=["png", "jpg", "jpeg"],
)
if fichier is None:
    st.stop()

st.image(fichier)

# 2. Appel API → POST /predict (pas de model.keras dans le front)
if not st.button("Analyser", type="primary"):
    st.stop()

error = None
preds = []
with st.spinner("Analyse en cours…"):
    try:
        # Le champ "spectro" est le contrat de piafzam.api.fast (UploadFile).
        response = requests.post(
            PREDICT_URL,
            files={"spectro": (fichier.name, fichier.getvalue())},
            timeout=120,
        )
        response.raise_for_status()
        preds = response.json().get("predictions") or []
    except requests.HTTPError:
        # 4xx/5xx : on tente le champ FastAPI "detail", sinon le corps brut.
        detail = response.text
        try:
            detail = response.json().get("detail", detail)
        except Exception:
            pass
        error = detail
    except requests.RequestException as exc:
        # Timeout, DNS, connexion refusée : l'API n'est pas joignable.
        hint = ""
        if "127.0.0.1" in API or "localhost" in API:
            hint = " Lance `make api` dans un autre terminal."
        error = f"API injoignable ({API}).{hint} {exc}"

if error:
    st.error(error)
    st.stop()

# 3. Nom d'espèce + %
shown = [p for p in preds if float(p.get("confidence") or 0) >= MIN_SHOW]
if not shown:
    st.warning("Rien de clair. Réessaie.")
    st.stop()

for pred in shown:
    name = pred.get("species") or ""
    conf = float(pred.get("confidence") or 0)
    st.subheader(f"{name} ({conf:.0%})")
