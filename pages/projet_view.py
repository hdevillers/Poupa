import models
from models import *
from hydralit import HydraHeadApp
import streamlit as st


class ProjetPage(HydraHeadApp):

    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        st.header("Créer un projet")
        with st.form("form projet"):
            input_titre = st.text_input("Titre*")
            input_directeur = st.text_input("Directeur/rice du projet*", value=st.session_state['login'])

            list_of_users = User.get_users()
            dico_users = {}
            for user in list_of_users:
                dico_users[user.login] = str(user)
            select_participants = st.multiselect("Ajouter des participants", format_func=lambda o: o[1])

            if st.form_submit_button:
                if input_titre == '' or input_directeur == '':
                    st.error("Les champs obligatoires n'ont pas tous été remplis")
                else:
                    participants = []
                    for participant in select_participants:
                        participants.append(participant[0])

