# piafzam-streamlit

App : **https://piafzam-app.streamlit.app/**

Front Streamlit public (même fichier que `piafzam/demo/app.py`) :
spectrogramme PNG/JPG → `POST /predict`. **Pas de modèle ici.**

Après un changement dans le projet privé : `make sync-streamlit-cloud`,
puis commit / push ici.

Le secret `PIAFZAM_API` est uniquement dans la console Streamlit Cloud
(App settings → Secrets). Rien dans ce repo.

## Local

```bash
pip install -r requirements.txt
# dans un autre terminal, dans le projet privé : make api
streamlit run app.py
```
