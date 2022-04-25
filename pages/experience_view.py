import random
import models
from models import *
import multipage_streamlit as mt

test = True


def app():

    with open("css\\experience.css", "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("Créer une experience")
    with st.form("form experience"):
        st.subheader("Informations de l'experience")
        list_of_poupa = models.get_all("boitiers")
        list_id_poupa = []
        for poupa in list_of_poupa:
            list_id_poupa.append(poupa[0])

        selectbox_boitiers = st.selectbox("Boitier utilisé*", list_id_poupa)
        if test:
            file_input = st.text_input('Fichier de données*', value='PP03-001.TXT')
        else:
            file_input = st.text_input('Fichier de données*')

        input_date = st.date_input("Date de l'experience*")
        input_lieu = st.text_input("Lieu de l'experience*")
        input_operateur = st.text_input("Operateur/trice de l'experience*")

        st.subheader("Capteurs")
        tab_titre_cpt = []
        tab_cpt = []
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
                st.write(f"**Capteur_{i + 1}**")
                selectfarine = st.selectbox("Farine*", list_nom_farine, key=i)
                selectlevain = st.selectbox("Levain*", list_nom_levain, key=i)
                input_remarque = st.text_area("Remarque", max_chars=100, key=i)
                tab_cpt.append((f"Capteur_{i + 1}", selectfarine, selectlevain, input_remarque))
                tab_titre_cpt.append(selectfarine + "-" + selectlevain)

        if st.form_submit_button('Lancer'):

            # print(tab_titre_cpt)
            experience = Experience(int(selectbox_boitiers), input_date, input_lieu, input_operateur, tab_titre_cpt,
                                    file_input)
            st.session_state['experience'] = experience
            st.sidebar.write(st.session_state)
            # experience.create_experience()
            for infos in tab_cpt:
                cpt = Capteur(infos[0], experience.get_id(), infos[1], infos[2], infos[3])


