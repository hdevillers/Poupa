import random

import streamlit

import models
from models import *
from hydralit import HydraHeadApp

test = True


class ExperiencePage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):

        with open("css\\experience.css", "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        st.title("Créer une experience")
        with st.form("form experience"):
            st.subheader("Informations de l'experience")
            list_of_poupa = models.get_all("boitiers")
            list_id_poupa = []
            for poupa in list_of_poupa:
                list_id_poupa.append(poupa[0])

            selectbox_boitiers = st.selectbox("Numéro du boitier utilisé*", list_id_poupa)
            if test:
                file_input = st.text_input('Fichier de données*', value='PP03-001.TXT')
            else:
                file_input = st.text_input('Fichier de données*')

            input_date = st.date_input("Date de l'experience*")
            input_lieu = st.text_input("Lieu de l'experience*")
            input_operateur = st.text_input("Operateur/trice de l'experience*", value=st.session_state['login'])

            st.subheader("Capteurs")
            tab_titre_cpt = []
            tab_cpt = []

            # Récupération des données des farines, levains et levures et création de dictionnaire pour les
            # selectbox
            list_of_farine = models.Farine.get_farines()
            dict_farines = {"---": "---"}
            for farine in list_of_farine:
                dict_farines[farine.id_farine] = str(farine)
            list_of_levain = models.Levain.get_levains()
            dict_levains = {"---": "---"}
            for levain in list_of_levain:
                dict_levains[levain.id] = str(levain)
            list_of_levures = models.Levure.get_levures()
            dict_levures = {"---": "---"}
            for levure in list_of_levures:
                dict_levures[levure.espece] = str(levure)

            # Mise en page et création des formulaires pour les capteurs
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            list_col = [col1, col2, col3, col4]
            for i in range(4):
                with list_col[i]:
                    st.write(f"**Capteur_{i + 1}**")
                    input_alias = st.text_input("Alias", key=i)
                    selectfarine = st.selectbox("Farine", list(dict_farines.items()), key=i, format_func=lambda o: o[1])
                    selectlevain = st.selectbox("Levain", list(dict_levains.items()), key=i, format_func=lambda o: o[1])
                    select_levure = st.selectbox("Levure", list(dict_levures.items()), key=i,
                                                 format_func=lambda o: o[1])
                    input_remarque = st.text_area("Remarque", max_chars=100, key=i)
                    tab_cpt.append((f"Capteur_{i + 1}", input_alias, selectfarine[0], selectlevain[0], select_levure[0],
                                    input_remarque))
                    tab_titre_cpt.append(input_alias)

            if st.form_submit_button('Lancer'):
                operateur = models.get_by("users", "login", input_operateur)
                if not operateur:
                    st.error("Opérateur inconnus")
                else:
                    # print(tab_titre_cpt)
                    experience = Experience(int(selectbox_boitiers), input_date, input_lieu, input_operateur,
                                            tab_titre_cpt, '', file_input)
                    st.session_state['experience'] = experience
                    st.sidebar.write(st.session_state)
                    list_of_capteurs = []
                    for infos in tab_cpt:
                        if infos[2] == '---':
                            farine_chosen = ''
                        else:
                            farine_chosen = infos[2]
                        if infos[3] == '---':
                            levain_chosen = ''
                        else:
                            levain_chosen = infos[3]
                        if infos[4] == '---':
                            levure_chosen = ''
                        else:
                            levure_chosen = infos[4]
                        cpt = Capteur(infos[0], experience.get_id(), farine_chosen, levain_chosen, levure_chosen,
                                      experience.get_id() + infos[0] + '.csv', infos[5])
                        list_of_capteurs.append(cpt)
                    st.session_state[f'capteurs'] = list_of_capteurs
                    st.success("Résultats génerés ! Allez consulter la page Résultats")
