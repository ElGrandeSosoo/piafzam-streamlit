"""Frontend Streamlit — même contrat que `taxifare-website` au bootcamp.

Pas de TensorFlow. On appelle `piafzam.api.fast` en HTTP (`POST /predict`).
Local : `make api` puis `make demo`. Cloud : le même fichier, secret `PIAFZAM_API`.
"""

from __future__ import annotations

import os

import requests
import streamlit as st

# page_config d'abord (Cloud refuse toute commande Streamlit avant).
st.set_page_config(page_title="PIAFZAM", page_icon="🪶", layout="centered")
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
    if st.secrets.load_if_toml_exists():
        _secret_api = str(st.secrets.get("PIAFZAM_API") or "")
except Exception:
    _secret_api = ""
API = str(_secret_api or os.environ.get("PIAFZAM_API") or "http://127.0.0.1:8000").strip().rstrip("/")
PREDICT_URL = f"{API}/predict"

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
        response = requests.post(
            PREDICT_URL,
            files={"spectro": (fichier.name, fichier.getvalue())},
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
    except requests.RequestException as exc:
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
