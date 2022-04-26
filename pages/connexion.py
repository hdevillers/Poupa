import streamlit as st
import models
import hashlib
import poupa_app
from mysql.connector import Error
import multipage_streamlit as mt


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


def app():

    app_connexion = mt.MultiPage()
    app_connexion.add("Connexion", connect)
    app_connexion.add("Inscription", inscription)
    app_connexion.run_expander()


def connect():
    with st.form("form connexion"):
        st.subheader("Login Section")

        username = st.text_input("User Name")
        password = st.text_input("Mot de passe", type='password')
        if st.form_submit_button("Login"):
            # if password == '12345':
            user = models.get_by('users', 'login', username)
            result = ""

            if user:
                result = check_hashes(str(st.secrets["seed"] + password), user[0][3])
            else:
                st.error("Utilisateur inconnus")
            if result:
                st.success(f"Connecté en tant que {user[0][1]} {user[0][2]}")
                st.session_state['login'] = user[0][0]
                st.session_state['prenom_nom'] = str(user[0][2] + " " + user[0][1])
                poupa_app.run()
            else:
                st.error("Mauvais mot de passe :P")


def inscription():
    with st.form("form inscription"):
        st.subheader("Insciption")
        username = st.text_input("User Name", key='inscription_username')
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        password = st.text_input("Mot de passe", type='password', key='password_inscription')
        confirm_password = st.text_input("Confirmation du mot de passe", type='password')

        if st.form_submit_button("Valider"):
            if password == confirm_password:
                hash_password = make_hashes(st.secrets['seed']+password)
                user = models.User(username, hash_password, nom, prenom)
                try:
                    user.create_user()
                except Error as err:
                    st.error(err.msg)
                    raise
                st.success("Utilisateur créé avec succé ! Maintenant connctez-vous")
            else:
                st.error("Les mots de passes doivent être identiques")
