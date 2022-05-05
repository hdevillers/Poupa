import random
import models
from models import *
from hydralit import HydraHeadApp


class ResultPage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        st.title('Résultat')
        if "experience" not in st.session_state:
            st.warning(f"**Renseignez une experience pour voir les résultats**")
            return

        experience = st.session_state["experience"]

        experience.dessiner_courbes()
        col1, col2 = st.columns(2)
        with col1:
            download = st.button("Télécharger les résultats")
            if download:
                experience.generate_pdf()
        with col2:
            archiver = st.button("Enregistrer")
            if archiver:
                i = 0
                if not models.get_by("experiences", "id", experience.get_id()):
                    experience.create_experience()
                else:
                    experience.update_experience()
                for cpt in st.session_state['capteurs']:
                    files = experience.generate_csv_cpt()
                    cpt.set_fichier_donnees(files[i])
                    i += 1
                    if not models.Capteur.get_capteur_by_pk(cpt.get_type(), cpt.get_id_experience()):
                        cpt.create_capteur()
                    else:
                        cpt.update_capteur()
