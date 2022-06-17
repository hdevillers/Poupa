import streamlit as st
import models
import hashlib
import time
from typing import Dict
from mysql.connector import Error
from hydralit import HydraHeadApp


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


class ConnexionPage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        st.subheader("Login Section")

        form_data = self._create_login_form()
        if form_data['submitted']:
            self._do_login(form_data)

    def _create_login_form(self) -> Dict:
        login_form = st.form(key="login_form")

        form_state = {'username': login_form.text_input('Identifiant'),
                      'password': login_form.text_input('Password', type="password"),
                      'submitted': login_form.form_submit_button('Login')}

        if st.button('Mode visiteur', key='guestbtn'):
            self.set_access(1, 'guest', True)
            st.session_state["access_level"] = 1
            self.do_redirect()

        if st.button("Créer un compte", key='signupbtn'):
            self.set_access(-1, 'guest')
            self.do_redirect()

        return form_state

    def _do_login(self, form_data):
        access, nom, prenom = self._check_access(form_data['username'], form_data['password'])
        if access:
            st.success(f"Connecté en tant que {nom} {prenom}")
            st.session_state['login'] = form_data['username']
            st.session_state['prenom_nom'] = str(nom + " " + prenom)
            with st.spinner("redirection vers l'application...."):
                time.sleep(1)
                st.session_state["access_level"] = 2
                self.set_access(2, st.session_state['login'], True)

                # Do the kick to the home page
                self.do_redirect()
        else:
            if nom is not None:
                st.error("Mauvais mot de passe :P")

    def _check_access(self, login, mdp):
        user = models.get_by('users', 'login', login)
        if user:
            return check_hashes(str(st.secrets["seed"] + mdp), user[0][3]), user[0][1], user[0][2]
        else:
            st.error("Utilisateur inconnus")
            return False, None, None


class InscriptionPage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        form_data = self._create_signup_form()

        if form_data['submitted']:
            self._do_signup(form_data)

    def _create_signup_form(self) -> Dict:
        login_form = st.form(key="login_form")

        form_state = {'username': login_form.text_input('Identifiant'),
                      'nom': login_form.text_input('Nom'),
                      'prenom': login_form.text_input('Prénom'),
                      'password': login_form.text_input('Password', type="password"),
                      'password2': login_form.text_input('Confirm Password', type="password"),
                      'submitted': login_form.form_submit_button("Inscription")}
        st.error("ATTENTION : il n'y a pas encore de moyen de retrouver votre mot de passe si vous l'oubliez")
        return form_state

    def _do_signup(self, form_data):
        if form_data['password'] == form_data['password2']:
            hash_password = make_hashes(st.secrets['seed'] + form_data['password'])
            user = models.User(form_data['username'], form_data['nom'], form_data['prenom'], hash_password)
            already_exist = models.User.get_users("login", form_data['username'])
            if already_exist:
                st.error("L'identifiant existe déja !")
                print(already_exist)
            else:
                user.create_user()
                with st.spinner("🤓 now redirecting to login...."):
                    time.sleep(2)
                    self.set_access(0, None)
                    self.do_redirect()
        else:
            st.error("Les mots de passes doivent être identiques")

