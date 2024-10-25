import streamlit as st

import os

st.set_page_config(
    page_title="Técnicas e Competências de Engenharia de Software praticadas no Estágio do PCS",
    page_icon=":📈:",
)
pg = st.navigation(
    {
        "Home": [st.Page("index.py", title="Sobre o projeto", default=True)],
        "2024": [
            st.Page("pages/a3a2Q.py", title="3º Ano - 2º Quadrimestre"),
            st.Page("pages/a5a2Q.py", title="5º Ano - 2º Quadrimestre"),
        ],
    }
)
st.header(
    "Técnicas e Competências de Engenharia de Software praticadas no Estágio do PCS"
)
pg.run()
