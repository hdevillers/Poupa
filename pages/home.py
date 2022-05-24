import streamlit as st
import models
from hydralit import HydraHeadApp


class HomePage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        if self.session_state.allow_access > 1:
            st.subheader("Experiences")
            all_exp = models.Experience.get_experiences('operateur', st.session_state['login'])
            for experience in all_exp:
                with st.container():
                    if experience.projet is None:
                        experience.str_exp_and_cpt()
            st.subheader("Projets")
            projets = models.Projet.get_projects_from_participant(st.session_state['login'])
            for projet in projets:
                st.write(str(projet))
                experience_of_user = projet.get_project_experiences()
                for experience in experience_of_user:
                    experience.str_exp_and_cpt()
        else:
            st.warning(f"Vous êtes connecté(e) en **mode visiteur**, vous n'avez donc **pas accés** à la base de "
                       f"données, les farines, levains et levures que vous créérez **seront perdus** si vous vous "
                       f"deconnectez ou quittez l'application ")
