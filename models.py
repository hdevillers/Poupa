import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import csv
import re
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])


test = True
conn = init_connection()


@st.experimental_memo(ttl=10)
def run_query(query, tuple_values):
    with conn.cursor() as cur:
        cur.execute(query, tuple_values)
        return cur.fetchall()


def get_all(nom_table):
    query = f"SELECT * FROM {nom_table}"
    return run_query(query, None)


def get_by(nom_table, selector, value):
    query = f"SELECT * FROM {nom_table} WHERE {selector} = %s"
    tuple_values = (value,)
    return run_query(query, tuple_values)


@st.experimental_memo(ttl=10)
def insert_into(query, tuple_values):
    with conn.cursor() as cur:
        cur.execute(query, tuple_values)
        conn.commit()


class Boitier:
    nom_table = "boitiers"

    def __init__(self, id_boitier):
        self.id = id_boitier


class Farine:
    nom_table = "farines"

    def __init__(self, nom, cereal=None, mouture=None, cendre=None):
        self.nom = nom
        self.cereal = cereal
        self.mouture = mouture
        self.cendre = cendre


class Levain:
    nom_table = "levains"

    def __init__(self, espece, generation, origine=None, cereale=None, hydratation=None, bacterie=None):
        self.identificateur = espece + "-" + generation
        self.espece = espece
        self.generation = generation
        self.origine = origine
        self.cereale = cereale
        self.hydratation = hydratation
        self.bacterie = bacterie


class User:
    nom_table = "users"

    def __init__(self, login, mdp, nom, prenom):
        self.login = login
        self.nom = nom
        self.prenom = prenom
        self.mdp = mdp


class Experience:
    nom_table = "experiences"
    tab_figures = []
    test = True

    def __init__(self, id_boitier, date, lieu, operateur, titres_cpt, fichier_donnees=None, fichier_resultat=None,
                 remarque=None):
        self.identificateur = str(id_boitier) + "_" + str(date) + "_" + operateur
        self.id_boitier = id_boitier
        self.date = date
        self.lieu = lieu
        self.operateur = operateur
        self.titres_cpt = titres_cpt
        self.fichier_donnees = fichier_donnees
        self.fichier_resultat = fichier_resultat
        self.remarque = remarque

    def get_id(self):
        return self.identificateur

    def create_experience(self):
        query = f"INSERT INTO {self.nom_table} (id, id_boitier, date, lieu, operateur, fichier_donnees, " \
                f"fichier_resultat, remarque) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (self.identificateur, self.id_boitier, self.date, self.lieu, self.operateur, self.fichier_donnees,
                  self.fichier_resultat, self.remarque)
        print(values)
        insert_into(query, values)

    COULEURS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9242b4"]

    def donnees_brutes(self):
        # on trouve en entrée le nom du fichier à lire

        f = open('data\\' + self.fichier_donnees, "r")
        my_reader = csv.reader(f)
        stot = [[], [], [], [], [], [], [], [], [], [], ]
        w = []
        glob = []
        # convertion des données du fichier en matrice
        for row in my_reader:
            # transformation de la chaine de caractère en nombre -> on enleve les char mais on garde les num de capteurs
            w.append([float(w) for w in re.findall(r'-?\d+\.?\d*', str(row))])

        for loop in w:
            # si len == 3 donc c'est un capteur
            if len(loop) == 3:
                for i in range(4):
                    if loop[1] == i + 1:
                        stot[2 * i].append(loop[0])
                        stot[2 * i + 1].append(loop[2])
            # sinon c'est la temperature
            if len(loop) == 2:
                stot[8].append(loop[0])
                stot[9].append(loop[1])

        # transformation des listes en matrices
        for elem in stot:
            glob.append(np.array(elem))
        return glob

    def lissage(self, x, y, p):
        # Fonction qui débruit une courbe par une moyenne glissante
        # sur 2P+1 points
        yout = []
        xout = x[p: -p]
        for index in range(p, len(y) - p):
            average = np.mean(y[index - p: index + p + 1])
            yout.append(average)
        return xout, yout

    def reg_lin(self, x, y):
        # conversion en array numpy
        x = np.array(x)
        y = np.array(y)
        # calculs des parametres a et b
        a = (len(x) * (np.dot(x, y)).sum() - x.sum() * y.sum()) / (len(x) * (x ** 2).sum() - (x.sum()) ** 2)
        b = ((np.dot(x, x)).sum() * y.sum() - x.sum() * (np.dot(x, y)).sum()) / (
                len(x) * (np.dot(x, x)).sum() - (x.sum()) ** 2)
        # renvoie des parametres
        return a, b

    def info_courbe(self, titre, x, y):
        plt.title(titre)
        plt.xlabel(x)
        plt.ylabel(y)

    def find_t0(self, a, b):
        t0 = -(b / a)
        return round(t0, 2)

    def find_t1(self, coor_current, x, y, intervalle):
        """ trouve t1 a partir de l'endroit ou on a trouvé la pente max, renvoi t1 arrondie .2"""
        x_current = coor_current
        y_current = coor_current
        while x_current + intervalle < len(y):
            a, b = self.reg_lin(x[x_current:x_current + intervalle], y[y_current: y_current + intervalle])
            x_current += 1
            y_current += 1
            if a < 0:
                return round(x[x_current], 2)

    def trouver_pente(self, x, y, i, intervalle, info_coeff_max, x_len, ax):
        """ trouve la pente maximum, la dessine, puis renvoi [a, b, t0] """
        if len(y) < intervalle or len(x) < intervalle:
            a, b = self.reg_lin([x[0], x[-1]],
                                [y[0], y[-1]])
            if info_coeff_max[0] < a:
                info_coeff_max[0] = round(a, 3)
                info_coeff_max[1] = b
                info_coeff_max[2] = intervalle * (i + 1)
            penteX = np.arange(x_len)
            ax.plot(penteX, info_coeff_max[0] * penteX + info_coeff_max[1], color="#B4B100")
            info_coeff_max.append(self.find_t0(info_coeff_max[0], info_coeff_max[1]))
            if test:
                print("############### stop #################")
            coor_max = info_coeff_max[2]
            info_coeff_max.pop(2)
            return coor_max, info_coeff_max
        else:
            a, b = self.reg_lin([x[0], x[intervalle]],
                                [y[0], y[intervalle]])
            if info_coeff_max[0] < a:
                info_coeff_max[0] = round(a, 3)
                info_coeff_max[1] = b
                info_coeff_max[2] = intervalle * (i + 1)
            if test:
                print(i)
                print("a   ={:8.3f}\nb   ={:8.3f}\n".format(a, b))
            return self.trouver_pente(x[intervalle:], y[intervalle:], i + 1, intervalle, info_coeff_max, x_len, ax)

    def dessiner_tableau(self, donnees):
        st.header("Tableau de données")
        container = st.container()
        with container:
            i = 0
            data = []
            for pente in donnees:
                pente.pop(1)
                pente.insert(0, self.titres_cpt[i])
                data.insert(i, pente)
                i += 1
            df = pd.DataFrame(data, columns=("Capteur", "pente max (mm/min)", "Début pousse (min)", "Fin pousse (min)"))
            st.dataframe(df)

            fig = plt.figure()
            ax = plt.subplot(111)
            ax.axis('off')
            ax.table(cellText=df.values, colLabels=df.columns, bbox=[0, 0, 1, 1])
            self.tab_figures.append(fig)

        # lecture du fichier de données et tracé

    def dessiner_courbes(self):
        with st.container():
            st.header("Courbes")
            touty = self.donnees_brutes()
            # infos_pente_courbes -> [[a, b, t0, t1], ....]
            infos_pente_courbes = []
            # on cherche les valeurs maximum de chaque graph pour les mettre à la meme echelle
            max_values = []
            for i in range(4):
                if len(touty[2 * i]) > 3:
                    max_values.append(np.amax(touty[2 * i + 1][0] - touty[2 * i + 1]))

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            col5, col6 = st.columns(2)
            tab_col = [col1, col2, col3, col4, col5, col6]
            # pour chaque graph, on fait une transaltation vers la droite et vers le bas pour que les courbes
            # commencent à (0, 0) puis on les dessines elles et leur pente max et on trouve le t0 et t1
            for i in range(4):
                with tab_col[i]:
                    if len(touty[2 * i]) > 3:
                        touty[2 * i] = (touty[2 * i] - touty[2 * i][0]) / 60
                        touty[2 * i + 1] = touty[2 * i + 1][0] - touty[2 * i + 1]

                        fig_courbe, ax = plt.subplots()
                        liss = self.lissage(touty[2 * i], touty[2 * i + 1], 5)

                        self.info_courbe(self.titres_cpt[i], 'temps (min)', 'pousse (mm)')
                        intervalle = 45

                        i_max, info_pente = self.trouver_pente(liss[0], liss[1], 0, intervalle, [0, 0, 0],
                                                               len(liss[0]),
                                                               ax)
                        infos_pente_courbes.append(info_pente)
                        infos_pente_courbes[i].append(self.find_t1(i_max, liss[0], liss[1], intervalle))

                        ax.plot([infos_pente_courbes[i][2] for j in range(len(liss[0]))], np.arange(len(liss[0])),
                                linestyle='--', linewidth=0.5, label="t0")
                        ax.plot([infos_pente_courbes[i][3] for j in range(len(liss[0]))], np.arange(len(liss[0])),
                                linestyle='--', linewidth=0.5, label="t1")
                        # if i == 0:
                        #     fig_courbe.legend(bbox_to_anchor=(0.75, 1.15), ncol=2)
                        plt.ylim(ymin=-3, ymax=max(max_values))

                        ax.plot(liss[0], liss[1], color=self.COULEURS[i])

                        listOf_Xticks = np.arange(0, max(touty[2 * i]), 20)
                        ax.set_xticks(listOf_Xticks, minor=True)
                        listOf_Yticks = np.arange(0, max(max_values), 2)
                        ax.set_yticks(listOf_Yticks, minor=True)

                        ax.grid(which='both')
                        ax.grid(which='minor', alpha=0.2, linestyle='--')

                        st.pyplot(fig_courbe)
                        self.tab_figures.append(fig_courbe)

                    else:
                        fig, ax = plt.subplots()
                        st.write("""Pas de données""")
                        st.pyplot(fig)
                        self.tab_figures.append(fig)
                    # info_courbe("Capteur n°" + str(i + 1), 'temps (min)', 'pousse (mm)', fig_courbe_vide)
                    # fig_courbe_vide.grid()

            # courbe des températures
            with col5:
                fig, ax = plt.subplots()
                touty[8] = (touty[8] - touty[8][0]) / 60
                ax.plot(touty[8], touty[9])

                listOf_Xticks = np.arange(0, max(touty[8]), 20)
                ax.set_xticks(listOf_Xticks, minor=True)
                listOf_Yticks = np.arange(0, max(touty[9]), 2)
                ax.set_yticks(listOf_Yticks, minor=True)

                ax.grid(which='both')
                ax.grid(which='minor', alpha=0.2, linestyle='--')

                st.pyplot(fig)
                # fig_temp.plot(touty[8], touty[9], color=COULEURS[4])
                plt.ylim(ymin=10)
                self.info_courbe("temperature", 'temps (min)', 'température  (°c)')
                self.tab_figures.append(fig)

            # toutes les courbes
            # fig_all = fig.add_subplot(236)
            with col6:
                fig, ax = plt.subplots()
                for i in range(4):
                    arr = self.lissage(touty[2 * i], touty[2 * i + 1], 5)
                    ax.plot(arr[0], arr[1])
                self.info_courbe("Capteurs", 'temps (min)', 'pousse (mm)')
                listOf_Xticks = np.arange(0, max(touty[8]), 20)
                ax.set_xticks(listOf_Xticks, minor=True)
                listOf_Yticks = np.arange(0, max(max_values), 2)
                ax.set_yticks(listOf_Yticks, minor=True)

                ax.grid(which='both')
                ax.grid(which='minor', alpha=0.2, linestyle='--')
                st.pyplot(fig)
                self.tab_figures.append(fig)

            # tableau des infos
            self.dessiner_tableau(infos_pente_courbes)
            print(self.tab_figures)

    def generate_pdf(self):
        pp = PdfPages(f"{self.get_id()}.pdf")
        for fig in self.tab_figures:
            pp.savefig(fig)
        pp.close()


class Capteur:
    nom_table = "capteurs"

    def __init__(self, type_capteur, id_experience, nom_farine, id_levain, remarque=None, fichier_donnees=None):
        self.type_capteur = type_capteur
        self.id_experience = id_experience
        self.nom_farine = nom_farine
        self.id_levain = id_levain
        self.remarque = remarque
        self.fichier_donnees = fichier_donnees

    def get_type(self):
        return self.type_capteur

    def get_id_experience(self):
        return self.id_experience

    def create_capteur(self):
        query = f"INSERT INTO {self.nom_table} ( type_capteur, id_experience, nom_farine, id_levain, remarque, " \
                f"fichier_donnees) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (self.type_capteur, self.id_experience, self.nom_farine, self.id_levain, self.remarque,
                  self.fichier_donnees,)
        print(values)
        insert_into(query, values)
