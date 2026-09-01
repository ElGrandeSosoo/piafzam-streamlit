# piafzam-streamlit

App : **https://piafzam-app.streamlit.app/**

Front Streamlit public (même fichier que `piafzam/demo/app.py`) :
spectrogramme PNG/JPG → `POST /predict`. **Pas de modèle ici.**

L’API, c’est `piafzam.api.fast` (`make api`), comme taxifare.
Pas [piafzam.duckdns.org](https://piafzam.duckdns.org/) (ça, c’est l’écoute BirdNET).

Après un changement dans le projet privé : `make sync-streamlit-cloud`,
puis commit / push ici.

## Streamlit Cloud

1. [https://piafzam-app.streamlit.app/](https://piafzam-app.streamlit.app/)
   — ce repo, fichier `app.py`.
2. Secret obligatoire :

```toml
PIAFZAM_API = "https://…  # URL publique de `make api` / piafzam.api.fast"
```

Sans ce secret, le front vise `http://127.0.0.1:8000` et l’analyse échoue.

## Local

```bash
pip install -r requirements.txt
# dans un autre terminal, dans le projet privé : make api
streamlit run app.py
```
