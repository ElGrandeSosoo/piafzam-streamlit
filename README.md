<!-- Repo public Streamlit Cloud : client HTTP uniquement, aucun modèle Keras ici. -->
# Piafzam

Envoie un spectrogramme : Piafzam identifie l’espèce d’oiseau (35 espèces européennes).

App : **https://piafzam-app.streamlit.app/**

Front Streamlit public (même fichier que `piafzam/demo/app.py`) :
spectrogramme PNG/JPG → `POST /predict`. **Pas de modèle ici.**

L’écoute en direct (micro) : **https://piafzam.duckdns.org/**

Après un changement dans le projet privé : `make sync-streamlit-cloud`,
puis commit / push ici.

Le secret `PIAFZAM_API` est uniquement dans la console Streamlit Cloud
(App settings → Secrets). Rien dans ce repo.

Le titre de la carte Slack / Discord vient de `page_title` dans `app/Hello.py`.
La description est ce premier paragraphe. L’image est une capture de
l’app (Streamlit Cloud, jusqu’à 24 h).

## Local

```bash
pip install -r requirements.txt
# dans un autre terminal, dans le projet privé : make api
streamlit run app/Hello.py
```
