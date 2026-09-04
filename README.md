# Piafzam

Front Streamlit HTTP-only (pas de Keras) : audio (fichier ou micro) → `POST /predict`.

App : **https://piafzam-app.streamlit.app/**

Trois onglets (`app/Hello.py`) : **Piafzam**, **Micro**, **Fichier**.

Secret `api_url` (base Cloud Run **ou** `…/predict`) : console Streamlit Cloud,
ou `.streamlit/secrets.toml` en local. Rien de secret dans ce repo.

## Local (ce repo)

```bash
pip install -r requirements.txt
# API du projet privé dans un autre terminal : make api
streamlit run app/Hello.py
```

## Local (projet privé)

```bash
make api    # :8000
make demo   # :8501 → piafzam/demo/app/Hello.py
```
