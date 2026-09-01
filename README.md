# piafzam-streamlit

App : **https://piafzam-app.streamlit.app/**

Client Streamlit public : fichier audio → API BirdNET déjà en ligne.

**Ce repo ne contient pas le modèle.** L’analyse tourne sur
[piafzam.duckdns.org](https://piafzam.duckdns.org/)
(`POST /listen/predict`). Le code source (page listen, BirdNET, jobs)
reste dans le projet privé.

`app.py` est une copie de `piafzam/demo/cloud_app.py`. Après un
changement : dans le projet privé, `make sync-streamlit-cloud`, puis
commit / push ici.

## Streamlit Cloud

1. [https://piafzam-app.streamlit.app/](https://piafzam-app.streamlit.app/)
   — [share.streamlit.io](https://share.streamlit.io) → ce repo, fichier `app.py`.
2. Secrets :

```toml
PIAFZAM_API = "https://piafzam.duckdns.org"
PIAFZAM_DEMO_KEY = "même valeur que LISTEN_DEMO_KEY sur la VM"
```

3. La VM listen doit être allumée (idle-stop 1 h). La clé saute le
   quota 12 requêtes / IP / minute (tous les visiteurs Cloud partagent
   une IP).

## Local

```bash
pip install -r requirements.txt
streamlit run app.py
```
