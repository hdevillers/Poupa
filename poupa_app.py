import streamlit as st
import pages.connexion
from pages.experience_view import ExperiencePage
from pages.home import HomePage
from pages.results_view import ResultPage
from hydralit import HydraApp
from pages.merge_capteurs import MergePage
from pages.element_view import FarinePage, LevainPage, LevurePage

# st.set_page_config(page_title="Poupa")

test = True
# if "login" in st.session_state and "prenom_nom" in st.session_state:
app = HydraApp(title="Poupa",
               hide_streamlit_markers=True,
               use_navbar=True,
               navbar_sticky=False,
               navbar_animation=True,
               )
app.add_app("Home", icon="🏠", app=HomePage("Accueil"), is_home=True)

app.add_app("Nouvelle Expérience", icon="🥼", app=ExperiencePage("Nouvelle Expérience"))
app.add_app("Résultats", icon="📚", app=ResultPage("Résultats"))
app.add_app("Fusion de capteurs", icon="🔃", app=MergePage("Fusion de capteurs"))
app.add_app("Farines", icon="🌾", app=FarinePage("Farines"))
app.add_app("Levains", icon="🦠", app=LevainPage("Levains"))
app.add_app("Levures", app=LevurePage("Levures"))

app.add_app("Signup", icon="🛰️", app=pages.connexion.InscriptionPage("Signup"), is_unsecure=True, logout_label="Logout")

app.add_app("Login", app=pages.connexion.ConnexionPage("Login"), is_login=True, logout_label="Logout")

menu_data = {
    'Home': ['Accueil'],
    'Nouvelle Expérience': ['Nouvelle Expérience'],
    'Résultats': ['Résultats'],
    'Fusion de capteurs': ['Fusion de capteurs'],
    'Farines&Levain': ["Farines", "Levains", "Levures"], }
over_theme = {'txc_inactive': '#FFFFFF'}

app.run(menu_data)


@app.logout_callback
def mylogout_callback():
    app.session_state.logged_in = False


@app.login_callback
def mylogin_callback():
    print('i was here')
    app.session_state.logged_in = True
    st.success("Bienvenu !!")
