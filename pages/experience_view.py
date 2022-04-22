import streamlit as st
import random
import models
from models import *

test = True


def app():
    st.title("Créer une experience")
    with st.container():
        list_of_poupa = models.get_all("boitiers")
        list_id_poupa = []
        for poupa in list_of_poupa:
            list_id_poupa.append(poupa[0])

        selectbox_boitiers = st.selectbox("Boitier utilisé", list_id_poupa)
        if test:
            file_input = st.text_input('Fichier de données', value='PP03-001.TXT')
        else:
            file_input = st.text_input('Fichier de données')

        input_date = st.date_input("Date de l'experience")
        input_lieu = st.text_input("Lieu de l'experience")
        input_operateur = st.text_input("Operateur de l'experience")

        tab_titre_cpt = []
        # tab_carac_choisis = []
        list_of_farine = models.get_all("farines")
        list_nom_farine = []
        for farine in list_of_farine:
            list_nom_farine.append(farine[0])
        list_of_levain = models.get_all("levains")
        list_nom_levain = []
        for levain in list_of_levain:
            list_nom_levain.append(levain[0])
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        list_col = [col1, col2, col3, col4]
        for i in range(4):
            with list_col[i]:
                st.write(f"Capteur_{i+1}")
                selectfarine = st.selectbox("Farine", list_nom_farine, key=i)
                selectlevain = st.selectbox("Levain", list_nom_levain, key=i)
                # tab_carac_choisis.append((selectfarine, selectlevain))
                tab_titre_cpt.append(selectfarine + "-" + selectlevain)

        button = st.button('Lancer')
        if button:
            if test:
                print(tab_titre_cpt)
                # for farine in tab_farines_choisies
                    # tab_titre_cpt.append(selectfarine + "-" + selectlevain)
                experience = Experience(int(selectbox_boitiers), input_date, input_lieu, input_operateur,
                                        file_input)
                experience.create_experience()

                # experience = Experience(1, 1, '21/04/2022', 'Inrae Montpellier', 'fmabille',  file_input)
                experience.dessiner_courbes(tab_titre_cpt)
