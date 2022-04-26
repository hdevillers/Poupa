import random
import models
from models import *
import multipage_streamlit as mt


def app():
    st.title('Résultat')
    if "experience" not in st.session_state:
        st.warning(f"**Renseignez une experience pour voir les résultats**")
        return

    experience = st.session_state["experience"]

    experience.dessiner_courbes()
    col1, col2 = st.columns(2)
    with col1:
        download = st.button("Télécharger les résultats")
        if download:
            experience.generate_pdf()
    with col2:
        archiver = st.button("Enregistrer")
        if archiver:
            experience.create_experience()
            for cpt in st.session_state['capteurs']:
                cpt.create_capteur()
