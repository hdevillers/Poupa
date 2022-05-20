import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import csv
import re
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])


test = True


@st.experimental_memo(ttl=10)
def run_query(query, tuple_values):
    """Prepare et execute une requête sql avec des parametres

    Parameters
    -----------
    query : String
        Requête préparée à executer

    tuple_values : (Any)
        Valeurs de la requête """
    conn = init_connection()
    with conn.cursor() as cur:
        cur.execute(query, tuple_values)
        return cur.fetchall()


def get_all(nom_table):
    """Recupère toutes les lignes d'une table

    :parameter
    -----------
    nom_table : String
        Nom de la table
    """
    query = f"SELECT * FROM {nom_table}"
    return run_query(query, None)


def get_by(nom_table, selector, value):
    """Récupère des lignes d'un tableau avec une condition

    Parameters
    -----------
    nom_table: String
        Nom de la table

    selector: String
        sélecteur de la condition de selection

    value : String, None
        valeur de la condition de selection
    """
    query = f"SELECT * FROM {nom_table} WHERE {selector} = %s"
    tuple_values = (value,)
    return run_query(query, tuple_values)


"""def get_by(nom_table, selectors, values):
    where_clause = ""
    i = 0
    for selector in selectors:
        where_clause += f"{selector}= %s"
        if i < len(selectors) - 1:
            where_clause += " AND "
        i += 1
    query = f"SELECT * FROM {nom_table} WHERE {where_clause}"
    tuple_values = (values,)
    return run_query(query, tuple_values)"""


@st.experimental_memo(ttl=10)
def insert_into(query, tuple_values):
    """Insert une ligne dans une table

    Parameters
    -----------
    query: String
        Requête préparée à exécuter

    tuple_values: (Any)
        Tulpe des valeurs de requête
    """

    conn = init_connection()
    with conn.cursor() as cur:
        cur.execute(query, tuple_values)
        conn.commit()


@st.experimental_memo(ttl=10)
def update(query, tuple_values):
    """Met à jour une ligne d'une table

    :parameter
    -----------
    query: String
        Requête préparée à exécuter
    tulpe_values: (Any)
        Tulpe des valeurs de requête"""
    conn = init_connection()
    with conn.cursor() as cur:
        cur.execute(query, tuple_values)
        conn.commit()


class Boitier:
    nom_table = "boitiers"

    def __init__(self, id_boitier):
        self.id = id_boitier


class Farine:
    nom_table = "farines"

    def __init__(self, alias=None, cereal=None, mouture=None, cendre=None, origine=None):
        """Objet représentant une farine

        Parameters
        -----------
        alias : String, None
            titre de la farine
        cereal : String, None
            cereale de la farine
        mouture : String, None
            type de mouture de la farine
        cendre : String, None
            cendre de la farine
        origine : String, None
            origine de la farine"""

        self.id_farine = None
        self.alias = alias
        self.origine = origine
        self.cereal = cereal
        self.mouture = mouture
        self.cendre = cendre

    def create_farine(self):
        """Insère une farine dans la base de données"""
        query = f"INSERT INTO {self.nom_table} (alias, cereale, type_mouture, cendre, origine) VALUES " \
                f"(%s, %s, %s, %s, %s)"
        values = (self.alias, self.cereal, self.mouture, self.cendre, self.origine)
        insert_into(query, values)

    @staticmethod
    def get_farines(selector=None, value=None):
        """Récupère les farines de la base de données, si il n'y a aucun paramètres récupère toutes les farines sinon
        les rècupère sous la condition selector = value

        :parameter
        -----------
        selector : String, None
            sélecteur de la condition de selection d'une farine
        value : String, None
            valeur de la condition de selection d'une farine

        :returns
        -----------
        Une liste d'objet farine
        """
        if selector is not None and value is not None:
            farines_from_bd = get_by(Farine.nom_table, selector, value)
        else:
            farines_from_bd = get_all(Farine.nom_table)
        farines = []
        for farine in farines_from_bd:
            f = Farine(farine[1], farine[2], farine[3], farine[4])
            farines.append(f)
            f.set_id(farine[0])
        return farines

    def set_id(self, id_farine):
        self.id_farine = id_farine

    def __str__(self):
        if st.session_state["access_level"] > 1:
            fstring = f"Farine n°{self.id_farine}: "
        else:
            fstring = f"Farine : "
        if self.alias != '':
            fstring += f"alias = {self.alias}   "
        if self.cereal != '':
            fstring += f"cereale = {self.cereal}   "
        if self.mouture != '':
            fstring += f"mouture = {self.mouture}   "
        if self.cendre != '':
            fstring += f"cendre = {self.cendre}   "
        return fstring

    def str_from(self):
        return "- " + self.alias


class Levain:
    nom_table = "levains"

    def __init__(self, alias, farine=None, origine=None, cereale=None, hydratation=None, microbiome=None):
        """Objet représentant un levain

        :parameter
        -----------
        alias: String, None
            Alias du levain
        farine: String, Int, None
            Farine ou identifiant de la farine du levain
        origine: String, None
            Origine du levain
        cereale: String, None
            Cereale du levain
        hydratation: Int, None
            Pourcentatge d'hydratation du levain
        microbiome: String, None
            Microbiome du levain
        """
        self.id = None
        self.alias = alias
        self.farine = farine
        self.origine = origine
        self.cereale = cereale
        self.hydratation = hydratation
        self.microbiome = microbiome

    def create_levain(self):
        """Insert un nouveau levain dans la base de données"""
        query = f"INSERT INTO {self.nom_table} (alias, farine, origine, cereale, hydratation, microbiome) VALUES " \
                f"(%s, %s, %s, %s, %s, %s)"
        values = (self.alias, self.farine, self.origine, self.cereale, self.hydratation,
                  self.microbiome)
        insert_into(query, values)

    def set_id(self, id_levain):
        self.id = id_levain

    @staticmethod
    def get_levains(selector=None, value=None):
        """Récupère les levains de la base de données, si il n'y a aucun paramètres récupère tous les levains sinon
                les rècupère sous la condition selector = value

                :parameter
                -----------
                selector : String, None
                    sélecteur de la condition de selection d'un levain
                value : String, None
                    valeur de la condition de selection d'un levain

                :returns
                -----------
                Une liste d'objets levains
                """
        if selector is not None and value is not None:
            levains_from_bd = get_by(Levain.nom_table, selector, value)
        else:
            levains_from_bd = get_all(Levain.nom_table)
        levains = []
        for levain in levains_from_bd:
            l = Levain(levain[1], levain[2], levain[3], levain[4], levain[5], levain[6])
            levains.append(l)
            l.set_id(levain[0])

        return levains

    def __str__(self):
        if st.session_state['access_level'] > 1:
            lstring = f"Levain n°{self.id}: "
        else:
            lstring = f"Levain : "
        if self.alias != '':
            lstring += f"alias = {self.alias}  "
        if self.farine != '':
            if st.session_state['access_level'] > 1:
                lstring += f"farine = {Farine.get_farines('id', self.farine)[0]}"
            else:
                lstring += f" Farine du levain : {str(self.farine)} "
        if self.origine != '':
            lstring += f"origine = {self.origine}  "
        if self.cereale != '':
            lstring += f"cereale = {self.cereale}  "
        if self.hydratation != '':
            lstring += f"hydratation = {str(self.hydratation)}  "
        if self.microbiome != '':
            lstring += f"bactérie = {self.microbiome}"
        return lstring

    def str_form(self):
        lstring = "- " + self.alias
        if self.farine is not None and self.farine != "":
            if st.session_state["access_level"] > 1:
                farine = Farine.get_farines("id", self.farine)[0].alias
            else:
                farine = self.farine.alias
            lstring += f" Farine = {farine}"
        return lstring


class Levure:
    nom_table = "levures"

    def __init__(self, espece, origine=None):
        """Objet représentant les levures

        Parameters
        -----------
        espece: String
            Espece de la levure
        origine: String, None
            Origine de la levure"""
        self.espece = espece
        self.origine = origine

    def create_levure(self):
        """Insert une levure dans la base de données"""
        query = f"INSERT INTO {self.nom_table} (espece, origine) VALUES ( %s, %s)"
        values = (self.espece, self.origine)
        insert_into(query, values)

    @staticmethod
    def get_levures(selector=None, value=None):
        """Récupère les levures de la base de données, si il n'y a aucun paramètres récupère toutes les levures sinon
                les rècupère sous la condition selector = value

                :parameter
                -----------
                selector : String, None
                    sélecteur de la condition de selection d'une levure
                value : String, None
                    valeur de la condition de selection d'une levure

                :returns
                -----------
                Une liste d'objet levure
                """
        if selector is not None and value is not None:
            levures_from_bd = get_by(Levure.nom_table, selector, value)
        else:
            levures_from_bd = get_all(Levure.nom_table)
        levures = []
        for levure in levures_from_bd:
            l = Levure(levure[0], levure[1])
            levures.append(l)
        return levures

    def __str__(self):
        lstring = f"Levure {self.espece}: "
        if self.origine != '':
            lstring += f"origine = {self.origine}  "
        return lstring


class User:
    nom_table = "users"

    def __init__(self, login, mdp, nom, prenom):
        """Classe des utilisateurs

        Parameters
        -----------
        login: String
            Login de l'utilisateur
        mdp: String
            Mot de passe de l'utilisateur
        nom: String
            Nom de l'utilisateur
        prenom: String
            Prenom de l'utilisateur"""
        self.login = login
        self.nom = nom
        self.prenom = prenom
        self.mdp = mdp

    def create_user(self):
        """Insert un utilisateur dans la base de données"""
        query = f"INSERT INTO {self.nom_table} (login, nom, prenom, mot_de_passe) VALUES (%s, %s, %s, %s)"
        values = (self.login, self.nom, self.prenom, self.mdp)
        insert_into(query, values)

    @staticmethod
    def get_users(selector=None, value=None):
        """Récupère les utilisateurs de la base de données, si il n'y a aucun paramètres récupère tous les utilisateurs
        sinon les rècupère sous la condition selector = value

                :parameter
                -----------
                selector : String, None
                    sélecteur de la condition de selection d'un utilisateur
                value : String, None
                    valeur de la condition de selection d'un utilisateur

                :returns
                -----------
                Une liste d'objets utilisateur
                """
        users = []
        if selector is not None and value is not None:
            users_from_bd = get_by(User.nom_table, selector, value)
        else:
            users_from_bd = get_all(User.nom_table)
        for user in users_from_bd:
            u = User(user[0], user[1], user[2], user[3])
            users.append(u)
        return users

    def __str__(self):
        return self.login + " : " + self.nom + " " + self.prenom


class Projet:
    nom_table = "projets"

    def __init__(self, directeur):
        """Classe représentant les projets

        Parameters
        -----------
        directeur: String
            Directeur/trice du projet"""
        self.directeur = directeur
        self.participants = []
        self.id_projet = None

    def set_id(self, id_p):
        self.id_projet = id_p

    @staticmethod
    def get_projets(selector=None, value=None):
        """Récupère les projets de la base de données, si il n'y a aucun paramètres récupère tous les projets sinon
                les rècupères sous la condition selector = value

                :parameter
                -----------
                selector : String, None
                    sélecteur de la condition de selection d'un projet
                value : String, None
                    valeur de la condition de selection d'un projet

                :returns
                -----------
                Une liste d'objets projet
                """

        if selector is not None and value is not None:
            projets_from_bd = get_by(Projet.nom_table, selector, value)
        else:
            projets_from_bd = get_all(Projet.nom_table)
        projets = []
        for projet in projets_from_bd:
            p = Projet(projet[1])
            projets.append(p)
            p.set_id(projet[0])
        return projets

    def get_participants(self):
        """Récupère les participants d'un projet depuis la base de données"""
        query = f"SELECT login FROM participer_projet pp JOIN users u ON u.login=pp.login_utilisateur WHERE " \
                f"id_projet={self.id_projet}"
        participants_from_bd = run_query(query, None)
        participants = []
        for participant in participants_from_bd:
            u = User(participant[0], participant[1], participant[2], participant[3])
            participants.append(u)
        return participants

    def get_project_experiences(self):
        return Experience.get_experiences("projet", self.id_projet)


class Experience:
    nom_table = "experiences"
    test = True

    def __init__(self, id_boitier, date, lieu, operateur, titres_cpt=None, projet=None, fichier_donnees=None,
                 fichier_resultat=None, remarque=None):
        """Classe représentant une experience

        Parameters
        -----------
        id_boitier: Int
            identifiant du boitier utiliser dans l'experience
        date: Date
            Date de l'experience
        lieu: String
            Lieu de l'experience
        operateur: String
            Operateur/rice de l'experience
        titres_cpt: [String], None
            Titres des capteurs du boitier de l'experience
        projet: Int, None
            Identificateur du possible projet de l'experience
        fichier_donnees: String, UploadFile
            Fichier TXT ou csv de données de l'expérience
        fichier_resultat: String
            Fichier pdf de résultats de l'experience
        remarque: String, None
            Eventuelles remarques
        """
        self.titres_cpt = titres_cpt
        self.identificateur = str(id_boitier) + "_" + str(date) + "_" + operateur
        self.id_boitier = id_boitier
        self.date = date
        self.lieu = lieu
        self.operateur = operateur
        self.projet = projet
        self.fichier_donnees = fichier_donnees
        self.fichier_resultat = fichier_resultat
        self.remarque = remarque
        self._touty = []
        self._touty_liss = []
        self._tab_figs = []
        self.max_values = []
        self._first_time = True

    def get_id(self):
        return self.identificateur

    def create_experience(self):
        """Insert une experience dans la base de données"""
        query = f"INSERT INTO {self.nom_table} (id, projet, id_boitier, operateur, date, lieu, fichier_donnees, " \
                f"fichier_resultat, remarque) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (self.identificateur, self.projet, self.id_boitier, self.operateur, self.date, self.lieu,
                  self.fichier_donnees, self.fichier_resultat, self.remarque)
        insert_into(query, values)

    def update_experience(self):
        """Met à jour une experience dans la base de données"""
        query = f"UPDATE {self.nom_table} SET projet=%s, id_boitier=%s, operateur=%s, date=%s, lieu=%s,  " \
                f"fichier_donnees=%s, fichier_resultat=%s, remarque=%s WHERE id = %s "
        values = (self.projet, self.id_boitier, self.operateur, self.date, self.lieu, self.fichier_donnees,
                  self.fichier_resultat, self.remarque, self.identificateur,)
        update(query, values)

    def __str__(self):
        estring = f"{self.identificateur}     lieu = {self.lieu}"
        return estring

    @staticmethod
    def get_experiences(selector=None, value=None):
        """Récupère les experiences de la base de données, si il n'y a aucun paramètres récupère toutes les experiences
        sinon les rècupère sous la condition selector = value

                :parameter
                -----------
                selector : String, None
                    sélecteur de la condition de selection d'une experience
                value : String, None
                    valeur de la condition de selection d'une experience

                :returns
                -----------
                Une liste d'objets experience
                """
        if selector is not None and value is not None:
            experiences_from_bd = get_by(Experience.nom_table, selector, value)
        else:
            experiences_from_bd = get_all(Experience.nom_table)
        experiences = []
        for experience in experiences_from_bd:
            e = Experience(id_boitier=experience[2], date=experience[4], lieu=experience[5], operateur=experience[3],
                           titres_cpt=None, projet=experience[1], fichier_donnees=experience[6],
                           fichier_resultat=experience[7], remarque=experience[8])
            experiences.append(e)
        return experiences

    COULEURS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9242b4"]

    def donnees_brutes(self):
        """lit le fichier self.fichier_données et trie ses données par type de capteru dans un tableau

        Returns
        -----------
        glob :  list[ndarray]
             la list[ndarray] des données
             """
        # on trouve en entrée le nom du fichier à lire
        # f = open('data/' + self.fichier_donnees, "r")
        # my_reader = csv.reader(f)
        my_reader = pd.read_csv(self.fichier_donnees).values.tolist()
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
        """Fonction qui débruit une courbe par une moyenne glissante
        """
        # sur 2P+1 points
        yout = []
        xout = x[p: -p]
        for index in range(p, len(y) - p):
            average = np.mean(y[index - p: index + p + 1])
            yout.append(average)
        return xout, yout

    def reg_lin(self, x, y):
        """Fonction qui effectue une régression linéaire

        Parameters
        -----------
        x : list
            intervalle des abscisses
        y : list
            intervalle des ordonnées

        Returns
        -----------
        a : float
            coefficient directeur et coordonées à l'origine
        b : flaat
            coordonnées à l'origine
        """
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
        """Donne un titre au graphique et aux axes

        Parameters
        -----------
        titre : str
            Titre du graphique
        x : str
            Titre de l'axe des abscisses
        y : str
            Titre de l'axe des ordonnées
        """
        plt.title(titre)
        plt.xlabel(x)
        plt.ylabel(y)

    def find_t0(self, a, b):
        """Trouve le t0, le point de début de pousse"""
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
        y_in_touty = self._touty_liss[-1]
        if len(y) < intervalle or len(x) < intervalle:
            if x != [0] and y != [0]:
                a, b = self.reg_lin([x[0], x[-1]],
                                    [y[0], y[-1]])
                if info_coeff_max[0] < a:
                    info_coeff_max[0] = round(a, 3)
                    info_coeff_max[1] = b
                    info_coeff_max[2] = intervalle * (i + 1)
                # x_len = x[0:intervalle] + intervalle * i
            t0 = self.find_t0(info_coeff_max[0], info_coeff_max[1])
            penteX = np.arange(x_len)
            ax.plot(penteX, info_coeff_max[0] * penteX + info_coeff_max[1], color="#B4B100")
            info_coeff_max.append(t0)
            if test:
                print("############### stop #################")
                # ax.plot(penteX, [0] * len(x_len))
            coor_max = info_coeff_max[2]
            info_coeff_max.pop(2)
            return coor_max, info_coeff_max
        else:
            previous = y[0]
            for current in y_in_touty[(intervalle - 20) * i: (intervalle + 20) * (i + 1):10]:
                if previous - current >= 4:
                    if test:
                        print("STOP FROM HERE")
                    return self.trouver_pente([0], [0], i + 1, intervalle, info_coeff_max, x_len, ax)
                previous = current
            a, b = self.reg_lin([x[0], x[intervalle]],
                                [y[0], y[intervalle]])
            if info_coeff_max[0] < a:
                info_coeff_max[0] = round(a, 3)
                info_coeff_max[1] = b
                info_coeff_max[2] = intervalle * (i + 1)
                # x_len = x[0:intervalle] + intervalle * i
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
                # pente.insert(0, self.titres_cpt[i])
                data.insert(i, pente)
                i += 1
            df = pd.DataFrame(data, columns=("pente max (mm/min)", "Début pousse (min)", "Fin pousse (min)"))
            st.dataframe(df)

            fig = plt.figure()
            ax = plt.subplot(111)
            ax.axis('off')
            tab = ax.table(cellText=df.values, rowLabels=self.titres_cpt, rowColours=["#abdbe3"] * len(donnees),
                           colLabels=df.columns,
                           colColours=["#abdbe3"] * len(donnees), bbox=[0, 0, 1, 1])
            tab.auto_set_font_size(False)
            tab.set_fontsize(10)
            self._tab_figs.append(fig)

        # lecture du fichier de données et tracé

    def dessiner_courbes(self):
        """ Dessine les courbes de l'experience \n
        **Probleme** : est appelé une deuxieme fois par streamlit au moment de generer le pdf
        pouvant occasionner une lenteur et remplie deux fois *tab_figures* \n
        **Solution** : pour *tab_figures* on le vide à chaque fois que l'on execute dessiner_courbes mais je n'ai pas
        de solution viable pour le fait qu'elle soit appelée deux fois pour l'instant """

        self._tab_figs = []
        with st.container():
            st.header("Courbes")
            if self._first_time:
                self._touty = self.donnees_brutes()
            # infos_pente_courbes -> [[a, b, t0, t1], ....]
            infos_pente_courbes = []
            # on cherche les valeurs maximum de chaque graph pour les mettre à la meme echelle
            if self._first_time:
                for i in range(4):
                    if len(self._touty[2 * i]) > 3:
                        self.max_values.append(np.amax(self._touty[2 * i + 1][0] - self._touty[2 * i + 1]))
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            col5, col6 = st.columns(2)
            tab_col = [col1, col2, col3, col4, col5, col6]
            # pour chaque graph, on fait une transaltation vers la droite et vers le bas pour que les courbes
            # commencent à (0, 0) puis on les dessines elles et leur pente max et on trouve le t0 et t1
            for i in range(4):
                with tab_col[i]:
                    if len(self._touty[2 * i]) > 3:
                        if self._first_time:
                            self._touty[2 * i] = (self._touty[2 * i] - self._touty[2 * i][0]) / 60
                            self._touty[2 * i + 1] = self._touty[2 * i + 1][0] - self._touty[2 * i + 1]

                        fig_courbe, ax = plt.subplots()
                        liss = self.lissage(self._touty[2 * i], self._touty[2 * i + 1], 5)
                        self._touty_liss.append(liss[1])

                        self.info_courbe(self.titres_cpt[i], 'temps (min)', 'pousse (mm)')
                        intervalle = 45

                        if max(self._touty[2 * i + 1]) > 3:
                            i_max, info_pente = self.trouver_pente(liss[0], liss[1], 0, intervalle, [0, 0, 0],
                                                                   len(liss[0]), ax)
                            infos_pente_courbes.append(info_pente)
                            infos_pente_courbes[i].append(self.find_t1(i_max, liss[0], liss[1], intervalle))

                            ax.plot([infos_pente_courbes[i][2] for j in range(len(liss[0]))],
                                    np.arange(len(liss[0])), linestyle='--', linewidth=1, label="t0")
                            ax.plot([infos_pente_courbes[i][3] for j in range(len(liss[0]))],
                                    np.arange(len(liss[0])), linestyle='--', linewidth=1, label="t1")
                            ax.legend(loc="lower right")
                        else:
                            infos_pente_courbes.append([0, 0, 0, 0])
                        # if i == 0:
                        #     fig_courbe.legend(bbox_to_anchor=(0.75, 1.15), ncol=2)
                        plt.ylim(ymin=-3, ymax=max(self.max_values))

                        ax.plot(liss[0], liss[1], color=self.COULEURS[i])

                        listOf_Xticks = np.arange(0, max(self._touty[2 * i]), 20)
                        ax.set_xticks(listOf_Xticks, minor=True)
                        listOf_Yticks = np.arange(0, max(self.max_values), 2)
                        ax.set_yticks(listOf_Yticks, minor=True)

                        ax.grid(which='both')
                        ax.grid(which='minor', alpha=0.2, linestyle='--')

                        st.pyplot(fig_courbe)
                        self._tab_figs.append(fig_courbe)

                    else:
                        if self._first_time:
                            self.titres_cpt.pop(i)
                        fig, ax = plt.subplots()
                        ax.text(0.5, 0.5, "Pas de données")
                        st.pyplot(fig)
                        self._tab_figs.append(fig)
                    # info_courbe("Capteur n°" + str(i + 1), 'temps (min)', 'pousse (mm)', fig_courbe_vide)
                    # fig_courbe_vide.grid()

            # courbe des températures
            with col5:
                fig, ax = plt.subplots()
                if self._first_time:
                    self._touty[8] = (self._touty[8] - self._touty[8][0]) / 60
                ax.plot(self._touty[8], self._touty[9])

                listOf_Xticks = np.arange(0, max(self._touty[8]), 20)
                ax.set_xticks(listOf_Xticks, minor=True)
                listOf_Yticks = np.arange(0, max(self._touty[9]), 2)
                ax.set_yticks(listOf_Yticks, minor=True)

                ax.grid(which='both')
                ax.grid(which='minor', alpha=0.2, linestyle='--')

                st.pyplot(fig)
                # fig_temp.plot(touty[8], touty[9], color=COULEURS[4])
                plt.ylim(ymin=10)
                self.info_courbe("temperature", 'temps (min)', 'température  (°c)')
                self._tab_figs.append(fig)

            # toutes les courbes
            with col6:
                fig, ax = plt.subplots()
                for i in range(4):
                    arr = self.lissage(self._touty[2 * i], self._touty[2 * i + 1], 5)
                    if i < len(self.titres_cpt):
                        ax.plot(arr[0], arr[1], label=self.titres_cpt[i])
                ax.legend(loc="lower right")
                self.info_courbe(f"Tous les capteurs du PouPâ {self.id_boitier}", 'temps (min)', 'pousse (mm)')
                listOf_Xticks = np.arange(0, max(self._touty[8]), 20)
                ax.set_xticks(listOf_Xticks, minor=True)
                listOf_Yticks = np.arange(0, max(self.max_values), 2)
                ax.set_yticks(listOf_Yticks, minor=True)

                ax.grid(which='both')
                ax.grid(which='minor', alpha=0.2, linestyle='--')
                st.pyplot(fig)
                self._tab_figs.append(fig)

            self._first_time = False
            # tableau des infos
            self.dessiner_tableau(infos_pente_courbes)

    def generate_pdf(self):
        pp = PdfPages(f"data\\results\\{self.get_id()}.pdf")
        first_page = plt.figure(figsize=(11.69, 8.27))
        first_page.clf()
        first_page.text(0.5, 0.5, str(self), size=24, ha="center")
        pp.savefig(first_page)
        for fig in self._tab_figs:
            pp.savefig(fig)
        pp.close()

    def generate_csv_cpt(self):
        tab_file = []
        for i in range(4):
            if len(self._touty[2 * i]) > 3:
                file = 'data\\capteurs\\' + self.identificateur + "_Capteur-" + str(i + 1) + '.csv'
                tab_file.append(file)
                with open(file, 'w') as csvfile:
                    print(csvfile)
                    filewriter = csv.writer(csvfile, delimiter=",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow(self._touty[2 * i])
                    filewriter.writerow(self._touty[2 * i + 1])
        return tab_file


class Capteur:
    nom_table = "capteurs"

    def __init__(self, type_capteur, id_experience, id_farine, id_levain, levure, remarque=None, fichier_donnees=None):
        self.type_capteur = type_capteur
        self.id_experience = id_experience
        self.id_farine = id_farine
        self.id_levain = id_levain
        self.levure = levure
        self.remarque = remarque
        self.fichier_donnees = fichier_donnees

    def get_type(self):
        return self.type_capteur

    def get_id_experience(self):
        return self.id_experience

    def get_id_farine(self):
        return self.id_farine

    def get_levain(self):
        return self.id_levain

    def create_capteur(self):
        query = f"INSERT INTO {self.nom_table} ( type_capteur, id_experience, id_farine, id_levain, levure, remarque, " \
                f"fichier_donnees) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (self.type_capteur, self.id_experience, self.id_farine, self.id_levain, self.levure, self.remarque,
                  self.fichier_donnees,)
        print(values)
        insert_into(query, values)

    def update_capteur(self):
        query = f"UPDATE {self.nom_table} SET id_farine=%s, id_levain=%s, levure=%s, remarque=%s, " \
                f"fichier_donnees=%s) WHERE type_capteur = %s AND id_experience = %s "
        values = (self.id_farine, self.id_levain, self.levure, self.remarque,
                  self.fichier_donnees, self.type_capteur, self.id_experience,)
        update(query, values)

    def __str__(self):
        cstring = f"**{self.type_capteur}**:  \n"
        if self.id_farine is not None:
            if st.session_state['access_level'] > 1:
                farine = Farine.get_farines("id", self.id_farine)
                cstring += f" {str(farine[0])}  \n"
            else:
                cstring += f"{str(self.id_farine)} "
        if self.id_levain is not None:
            if st.session_state['access_level'] > 1:
                levain = Levain.get_levains("id", self.id_levain)
                cstring += f"{str(levain[0])}  \n"
            else:
                cstring += f"{str(self.id_levain)}  \n"
        if self.levure is not None:
            if st.session_state['access_level'] > 1:
                levure = Levure.get_levures("espece", self.levure)
                cstring += f"{str(levure[0])}  \n"
            else:
                if "levures" in st.session_state:
                    for levure in st.session_state["levures"]:
                        if levure.espece == self.levure:
                            cstring += f"{str(levure)}  \n"
        if self.remarque is not None:
            cstring += f"remarque = {self.remarque}  \n"
        if self.fichier_donnees is not None:
            cstring += f"fichier de données = {self.fichier_donnees}  \n"
        return cstring

    def get_fichier_donnes(self):
        return self.fichier_donnees

    def set_fichier_donnees(self, file):
        self.fichier_donnees = file

    @staticmethod
    def get_capteur_by_pk(type_cpt, id_exp):
        query = f"SELECT * FROM capteurs WHERE type_capteur = %s AND id_experience = %s"
        tuple_values = (type_cpt, id_exp)
        return run_query(query, tuple_values)

    @staticmethod
    def get_capteurs(selector=None, value=None):
        if selector is not None and value is not None:
            capteurs_from_database = get_by(Capteur.nom_table, selector, value)
        else:
            capteurs_from_database = get_all(Capteur.nom_table)
        capteurs = []
        for capteur in capteurs_from_database:
            capteurs.append(Capteur(capteur[0], capteur[1], capteur[2], capteur[3], capteur[4], capteur[5], capteur[6]))
        return capteurs


class MergeCapteur:
    def __init__(self, list_files):
        self.list_files = list_files
        self.list_cpt = []
        fig, ax = plt.subplots()
        max_values = []
        max_len = []
        i = 0
        for file in self.list_files:
            my_data = pd.read_csv(file, sep=",").values.tolist()
            self.list_cpt.append(my_data)
            ax.plot(my_data[0])
            i += 1
            max_values.append(max(my_data[0]))
            max_len.append(len(my_data[0]))

        listOf_Xticks = np.arange(0, max(max_len), 20)
        ax.set_xticks(listOf_Xticks, minor=True)
        listOf_Yticks = np.arange(0, max(max_values), 2)
        ax.set_yticks(listOf_Yticks, minor=True)

        ax.grid(which='both')
        ax.grid(which='minor', alpha=0.2, linestyle='--')
        st.pyplot(fig)
