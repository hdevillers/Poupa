import streamlit as st

import models


def app():
    st.header("Bienvenu !")
    all_exp = models.get_all("experiences")
    for experience in all_exp:
        with st.container():
            st.subheader(experience[0])
            list_cpt = models.get_by("capteurs", "id_experience", experience[0])
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            list_cols = [col1, col2, col3, col4]
            i = 0
            for capteur in list_cpt:
                with list_cols[i]:
                    st.write(f"**{str(capteur[0])}**")
                    st.write(f"farine utilisé = {capteur[2]}")
                    st.write(f"levain utilisé = {capteur[3]}")
                i += 1

