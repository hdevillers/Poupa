from hydralit import HydraApp, HydraHeadApp
import streamlit as st
import models


class MergePage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        all_exp = models.get_by("experiences", 'operateur', st.session_state['login'])
        list_cpt = []
        with st.form('choose cpt'):
            list_checkbox = []
            i = 0
            for experience in all_exp:
                list_cpt = models.Capteur.get_capteurs("id_experience", experience[0])
                with st.container():
                    st.subheader(experience[0])

                    for capteur in list_cpt:
                        cpt_checkbox = st.checkbox(str(capteur), key=f"chckbx{i}")
                        list_checkbox.append(cpt_checkbox)
                        i += 1

            if st.form_submit_button("Fusionner"):
                print(list_checkbox)
                i = 0
                list_file = []
                for cpt in list_cpt:
                    if list_checkbox[i]:
                        list_file.append(cpt.get_fichier_donnes())
                    i += 1

                if not list_file or len(list_file) == 1:
                    st.error("Veuillez choiri au moins 2 capteurs")
                else:
                    merge_cpt = models.MergeCapteur(list_file)
