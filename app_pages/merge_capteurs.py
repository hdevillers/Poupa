from hydralit import HydraApp, HydraHeadApp
import streamlit as st
import models


class MergePage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        st.header("Comparaison de Capteurs")
        st.write("Sur cette page comparez plusieurs pâtons d'experience différentes. Pour cela, vous devez d'abord "
                 "avoir généré l'experience du pâton voulu et enregistré les résultats sur votre ordinateur. Vous "
                 "pouvez alors selectionner le fichier des capteurs correspondants dans le selecteur ci-dessous ")
        with st.form('choose cpt'):
            list_cpt = []
            # début du code pour, récupérer les fichiers des capteurs du serveur et les afficher comme une liste de
            # radio boutons. Pas implémenté par contraite de temps
            """if self.session_state.allow_access > 1:
                all_exp = models.get_by("experiences", 'operateur', st.session_state['login'])
                list_checkbox = []
                i = 0
                for experience in all_exp:
                    list_cpt = models.Capteur.get_capteurs("id_experience", experience[0])
                    with st.container():
                        st.subheader(experience[0])

                        for capteur in list_cpt:
                            cpt_checkbox = st.checkbox(str(capteur), key=f"chckbx{i}")
                            list_checkbox.append(cpt_checkbox)
                            i += 1"""

            list_cpt = st.file_uploader("Fichier des flacons à fusionner", accept_multiple_files=True)
            if st.form_submit_button("Fusionner"):
                i = 0
                list_file = []
                """if self.session_state.allow_access > 1:
                    for cpt in list_cpt:
                        if list_checkbox[i]:
                            list_file.append(cpt.get_fichier_donnes())
                        i += 1"""
                list_file = list_cpt

                if not list_file or len(list_file) == 1:
                    st.error("Veuillez choisir au moins 2 capteurs")
                else:
                    merge_cpt = models.MergeCapteur(list_file)
