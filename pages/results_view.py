import models
from models import *
from hydralit import HydraHeadApp


class ResultPage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        st.header('Résultat')
        if "experience" not in st.session_state:
            st.warning(f"**Renseignez une experience pour voir les résultats**")
            return

        mssg_archiver = ''
        if self.session_state.allow_access > 1:
            mssg_archiver = " ou les enregistrer dans la base de données pour les consulter plus tard en cliquant sur "\
                            "**'Archiver dans la base de données'** "
        st.write(f"Vous pouvez consulter vos resutats sur cette page. Retrouvez ses informations dans la barre de "
                 f"droite et les différents graphiques ci-dessous. Vous pouvez télécharger un pdf de votre résultat en "
                 f"cliquant sur **'Télécharger les résultats'**{mssg_archiver}.")
        experience = st.session_state["experience"]
        with st.sidebar:
            st.header("Informations")
            st.subheader(f"Experience {experience.identificateur}")
            if experience.projet is not None:
                st.write(f"Fais partis du projet numéros {experience.projet}")
            if self.session_state.allow_access > 1:
                fichier = f"Fichier de données : {experience.fichier_donnees}  \n"
            else:
                fichier = f"Fichier de données : {experience.fichier_donnees.name}  \n"
            st.write(f"Boitier : {experience.id_boitier}  \n"
                     f"Date : {experience.date}  \n"
                     f"Lieu : {experience.lieu}  \n"
                     f"Operateur : {experience.operateur}  \n"
                     f"{fichier}")
            if experience.remarque is not None:
                st.write(f"Remarque : {experience.remarque}  \n")

            st.subheader("Capteurs")
            for capteur in st.session_state['capteurs']:
                st.write(str(capteur))

        experience.dessiner_courbes()
        col1, col2 = st.columns(2)

        # Génération du pdf
        with col1:
            """download = st.button("Télécharger les résultats", on_click=experience.generate_pdf)"""
            experience.generate_pdf()
            pdf_byte = ""
            with open(f"{experience.identificateur}.pdf", "rb") as pdf_file:
                pdf_byte = pdf_file.read()
            st.download_button(label="Télécharger les résultats",
                               data=pdf_byte, file_name="test.pdf", mime="application/octet-stream")
            i = 0
            for cpt in st.session_state['capteurs']:
                files = experience.generate_csv_cpt()
                cpt.set_fichier_donnees(files[i])

        # Enregistrement dans la base de données
        with col2:
            if self.session_state.allow_access > 1:
                archiver = st.button("Archiver dans la base de données")
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
