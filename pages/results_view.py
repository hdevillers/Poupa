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
    download = st.button("Télécharger les résultats")
    if download:
        experience.generate_pdf()
