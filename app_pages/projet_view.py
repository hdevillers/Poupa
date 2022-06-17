import models
from models import *
from hydralit import HydraHeadApp
import streamlit as st


class AddProjectPage(HydraHeadApp):

    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        st.header("Projets")
        with st.sidebar:
            with st.form("form projet"):
                input_titre = st.text_input("Titre*", max_chars=30)
                input_directeur = st.warning(f"Directeur/rice du projet : {st.session_state['login']}")

                list_of_users = User.get_users()
                dico_users = {}
                for user in list_of_users:
                    dico_users[user.login] = str(user)
                select_participants = st.multiselect("Ajouter des participants", list(dico_users.items()),
                                                     format_func=lambda o: o[1])
                if st.form_submit_button("Créer"):
                    if input_titre == '' or input_directeur == '':
                        st.error("Les champs obligatoires n'ont pas tous été remplis")
                    else:
                        if input_directeur not in User.get_users('login', input_directeur):
                            st.error("Directeur ou directrice inconnue")
                        else:
                            participants = []
                            for participant in select_participants:
                                participants.append(participant[0])

                            p = Projet(input_titre, input_directeur, participants)
                            p.create_projet()

        st.subheader("Vos projets")
        projets = Projet.get_projets("directeur", st.session_state["login"])
        i = 0
        for projet in projets:
            with st.expander(f"{projet.titre}"):
                st.write("**Participants**:")
                participants = projet.get_participants()
                for participant in participants:
                    st.write(str(participant))
                with st.form(f"add_participant {i}"):
                    i += 1
                    list_of_users = projet.get_other_users()
                    dico_users = {}
                    if list_of_users is not None:
                        for user in list_of_users:
                            dico_users[user.login] = str(user)
                    select_participants = st.multiselect("Ajouter des participants", list(dico_users.items()),
                                                         key=i, format_func=lambda o: o[1])
                    if st.form_submit_button("Ajouter participant.e.s"):
                        for participant in select_participants:
                            projet.add_participant(participant[0])
                for experience in projet.get_project_experiences():
                    experience.str_exp_and_cpt()
