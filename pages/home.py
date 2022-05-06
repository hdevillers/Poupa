import streamlit as st
import pages.connexion
import models
from hydralit import HydraHeadApp


class HomePage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        # st.header("Bienvenu " + st.session_state['prenom_nom'])
        # all_exp = models.get_by("experiences", "operateur", st.session_state['login'])
        all_exp = models.Experience.get_experiences('operateur', st.session_state['login'])
        for experience in all_exp:
            with st.container():
                st.subheader(experience.get_id())
                list_cpt = models.Capteur.get_capteurs("id_experience", experience.get_id())
                col1, col2 = st.columns(2)
                col3, col4 = st.columns(2)
                list_cols = [col1, col2, col3, col4]
                i = 0
                for capteur in list_cpt:
                    with list_cols[i]:
                        st.write(str(capteur))
                    i += 1
