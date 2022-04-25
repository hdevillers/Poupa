import pages.experience_view, pages.results_view, pages.home
from models import *
import multipage_streamlit as mt

# st.set_page_config(page_title="Poupa")
COULEURS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9242b4"]
test = True

app = mt.MultiPage()

# app.add_page("Accueil", home.app())
app.add("Accueil", pages.home.app)
app.add("Nouvelle Experience", pages.experience_view.app)
app.add("Résultats", pages.results_view.app)

if test:
    # rows = run_query("SELECT * from boitiers;")
    # for row in rows:
    #   st.write(f"le boitier {row[0]} est il dispo ? {row[1]}")
    # pages.experience_view.app()
    # dessiner_courbes('data\PP03-001.TXT', [1, 2, 3, 4])
    app.run_radio()

