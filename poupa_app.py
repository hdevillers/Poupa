import multipage_streamlit as mt
import streamlit as st
import pages.connexion
import pages.experience_view
import pages.home
import pages.results_view


# st.set_page_config(page_title="Poupa")
def run():
    test = True
    app = mt.MultiPage()
    if "login" in st.session_state and "prenom_nom" in st.session_state:
        # app.add_page("Accueil", home.app())
        app.add("Accueil", pages.home.app)
        app.add("Nouvelle Experience", pages.experience_view.app)
        app.add("Résultats", pages.results_view.app)

        app.run_radio()

        deco = st.sidebar.button("Déconnexion")
        if deco:
            del st.session_state["login"]
            del st.session_state["prenom_nom"]
            pages.connexion.app()
            pages.home.app()
    else:
        pages.connexion.app()


if __name__ == "__main__":
    run()
