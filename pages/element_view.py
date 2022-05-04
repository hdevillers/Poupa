import streamlit as st
from hydralit import HydraHeadApp
import models


class FarinePage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        with st.expander("Ajouter une farine"):
            with st.form("add_farine"):
                input_nom = st.text_input("Nom", max_chars=100)
                input_cereale = st.text_input("Céréale", max_chars=50)
                input_mouture = st.text_input("Mouture", max_chars=50)
                input_cendre = st.text_input("Cendres", max_chars=50)
                if st.form_submit_button("Ajouter"):
                    farine = models.Farine(input_nom, input_cereale, input_mouture, input_cendre)
                    farine.create_farine()

        with st.container():
            all_farines = models.Farine.get_farines()
            for farine in all_farines:
                st.write(str(farine))


class LevainPage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        with st.expander("Ajouter un Levain"):
            with st.form("add_levain"):
                input_espece = st.text_input("Espece", max_chars=100)
                input_generation = st.number_input("Génération", max_value=999)
                input_origine = st.text_input("Origine", max_chars=100)
                input_cereale = st.text_input("Céréale", max_chars=50)
                input_hydratation = st.number_input("% Hydratation", max_value=999)
                input_bacterie = st.text_input("Bactérie", max_chars=50)
                if st.form_submit_button("Ajouter"):
                    levain = models.Levain(input_espece, input_generation, input_origine, input_cereale,
                                           input_hydratation, input_bacterie)
                    levain.create_levain()

        with st.container():
            all_levains = models.Levain.get_levains()
            for levain in all_levains:
                st.write(str(levain))

