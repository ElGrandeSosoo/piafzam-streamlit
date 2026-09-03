"""Frontend Streamlit — point d'entrée multipage."""

import streamlit as st

st.set_page_config(page_title="Piafzam", page_icon="app/icon.png")

pg = st.navigation(
    [
        st.Page("app/Hello.py", title="Piafzam", default=True),
        st.Page("app/pages/page_01.py", title="Micro"),
        st.Page("app/pages/page_02.py", title="Fichier"),
    ]
)
pg.run()
