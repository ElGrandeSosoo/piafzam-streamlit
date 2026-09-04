"""URL d'inférence : secret `api_url` avec ou sans suffixe `/predict`."""

from __future__ import annotations

import os


def predict_url(raw: str | None = None) -> str:
    if raw is None:
        try:
            import streamlit as st

            raw = str(st.secrets.get("api_url") or "")
        except Exception:
            raw = ""
        raw = raw or os.environ.get("PIAFZAM_API") or "http://127.0.0.1:8000"
    raw = str(raw).strip().rstrip("/")
    if raw.endswith("/predict"):
        return raw
    return f"{raw}/predict"
