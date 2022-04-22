import pages.experience_view
import pages.home
from models import *
from multipage import MultiPage

# st.set_page_config(page_title="Poupa")
COULEURS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9242b4"]
test = True

app = MultiPage()


# app.add_page("Accueil", home.app())
app.add_page("Novelle Experience", pages.experience_view.app)

if test:
    # rows = run_query("SELECT * from boitiers;")
    # for row in rows:
    #   st.write(f"le boitier {row[0]} est il dispo ? {row[1]}")
    pages.experience_view.app()
    # dessiner_courbes('data\PP03-001.TXT', [1, 2, 3, 4])
