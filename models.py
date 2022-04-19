import streamlit as st
import mysql.connector


@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])


conn = init_connection()


class Model:
    nom_table = ""

    def run_query(self, query, tuple_values):
        with conn.cursor() as cur:
            cur.execute(query, tuple_values)
            return cur.fetchall()

    def get_all(self):
        query = "SELECT * FROM {self.nom_table}"
        return self.run_query(query, None)

    def get_by(self, selector, value):
        query = "SELECT * FROM {self.nom_table} WHERE {selector} = %s"
        tuple_values = (value,)
        return self.run_query(query, tuple_values)


class Boitier(Model):
    nom_table = "boitier"

    def __init__(self, id_boitier):
        self.id = id_boitier


class Farine(Model):
    nom_table = "farine"

    def __init__(self, nom, cereal=None, mouture=None, cendre=None):
        self.nom = nom
        self.cereal = cereal
        self.mouture = mouture
        self.cendre = cendre


class Levain(Model):
    nom_table = "levain"

    def __init__(self, espece, generation, origine=None, cereale=None, hydratation=None, bacterie=None):
        self.espece = espece
        self.generation = generation
        self.origine = origine
        self.cereale = cereale
        self.hydratation = hydratation
        self.bacterie = bacterie


class User(Model):
    nom_table = "user"

    def __init__(self, login, mdp, nom, prenom):
        self.login = login
        self.nom = nom
        self.prenom = prenom
        self.mdp = mdp


class Campagne(Model):
    nom_table = "campagne"

    def __init__(self, date_debut, login_user):
        self.date_debut = date_debut
        self.login_user = login_user


class Experience(Model):
    nom_table = "experience"

    def __init__(self, id_boitier, id_camp, date, lieu, operateur, fichier_donnees=None, fichier_resultat=None,
                 remarque=None):
        self.id_boitier = id_boitier
        self.id_camp = id_camp
        self.date = date
        self.lieu = lieu
        self.operateur = operateur
        self.fichier_donnes = fichier_donnees
        self.fichier_resultat = fichier_resultat
        self.remarque = remarque


class Capteur(Model):
    nom_table = "capteur"

    def __init__(self, type_capteur, id_experience, nom_farine, id_levain, remarque=None):
        self.type_capteur = type_capteur
        self.id_experience = id_experience
        self.nom_farine = nom_farine
        self.id_levain = id_levain
        self.remarque = remarque
