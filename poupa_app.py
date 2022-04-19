from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from codecs import *
import csv
import re
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

COULEURS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9242b4"]
test = True
st.set_page_config(page_title="Poupa")


def donnees_brutes(fic):
    # on trouve en entrée le nom du fichier à lire
    # on trouve en sortie les points de la fonction x et y
    f = open(fic, "r")
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


def lissage(x, y, p):
    # Fonction qui débruit une courbe par une moyenne glissante
    # sur 2P+1 points
    yout = []
    xout = x[p: -p]
    for index in range(p, len(y) - p):
        average = np.mean(y[index - p: index + p + 1])
        yout.append(average)
    return xout, yout


def reg_lin(x, y):
    # conversion en array numpy
    x = np.array(x)
    y = np.array(y)
    # calculs des parametres a et b
    a = (len(x) * (np.dot(x, y)).sum() - x.sum() * y.sum()) / (len(x) * (x ** 2).sum() - (x.sum()) ** 2)
    b = ((np.dot(x, x)).sum() * y.sum() - x.sum() * (np.dot(x, y)).sum()) / (
            len(x) * (np.dot(x, x)).sum() - (x.sum()) ** 2)
    # renvoie des parametres
    return a, b


def info_courbe(titre, x, y):
    plt.title(titre)
    plt.xlabel(x)
    plt.ylabel(y)


def find_t0(a, b):
    t0 = -(b / a)
    return round(t0, 2)


def find_t1(coor_current, x, y, intervalle):
    ''' trouve t1 a partir de l'endroit ou on a trouvé la pente max, renvoi t1 arrondie .2'''
    x_current = coor_current
    y_current = coor_current
    while x_current + intervalle < len(y):
        a, b = reg_lin(x[x_current:x_current + intervalle], y[y_current: y_current + intervalle])
        x_current += 1
        y_current += 1
        if a < 0:
            return round(x[x_current], 2)


def trouver_pente(x, y, i, intervalle, info_coeff_max, x_len, ax):
    ''' trouve la pente maximum, la dessine, puis renvoi [a, b, t0] '''
    if len(y) < intervalle or len(x) < intervalle:
        a, b = reg_lin([x[0], x[-1]],
                       [y[0], y[-1]])
        if info_coeff_max[0] < a:
            info_coeff_max[0] = round(a, 3)
            info_coeff_max[1] = b
            info_coeff_max[2] = intervalle * (i + 1)
        penteX = np.arange(x_len)
        ax.plot(penteX, info_coeff_max[0] * penteX + info_coeff_max[1], color="#B4B100")
        info_coeff_max.append(find_t0(info_coeff_max[0], info_coeff_max[1]))
        if test:
            print("############### stop #################")
        coor_max = info_coeff_max[2]
        info_coeff_max.pop(2)
        return coor_max, info_coeff_max
    else:
        a, b = reg_lin([x[0], x[intervalle]],
                       [y[0], y[intervalle]])
        if info_coeff_max[0] < a:
            info_coeff_max[0] = round(a, 3)
            info_coeff_max[1] = b
            info_coeff_max[2] = intervalle * (i + 1)
        if test:
            print(i)
            print("a   ={:8.3f}\nb   ={:8.3f}\n".format(a, b))
        return trouver_pente(x[intervalle:], y[intervalle:], i + 1, intervalle, info_coeff_max, x_len, ax)


def dessiner_tableau(donnees, titles):
    st.header("Tableau de données")
    container = st.container()
    with container:
        i = 0
        print(donnees)
        data = []
        for pente in donnees:
            pente.pop(1)
            pente.insert(0, titles[i])
            data.insert(i, pente)
            i += 1
        print(data)
        df = pd.DataFrame(data, columns=("Capteur", "pente max (mm/min)", "Début pousse (min)", "Fin pousse (min)"))
        st.dataframe(df)


# lecture du fichier de données et tracé
def dessiner_courbes(fichier, titres):
    st.header("Courbes")
    touty = donnees_brutes(fichier)
    # infos_pente_courbes -> [[a, b, t0, t1], ....]
    infos_pente_courbes = []
    # on cherche les valeurs maximum de chaque graph pour les mettre à la meme echelle
    max_values = []
    for i in range(4):
        if len(touty[2 * i]) > 3:
            max_values.append(np.amax(touty[2 * i + 1][0] - touty[2 * i + 1]))

    with st.container():
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)
        tab_col = [col1, col2, col3, col4, col5, col6]
        # pour chaque graph, on fait une transaltation vers la droite et vers le bas pour que les courbes commences à
        # (0, 0) puis on les dessines elles et leur pente max et on trouve le t0 et t1
        for i in range(4):
            with tab_col[i]:
                if len(touty[2 * i]) > 3:
                    touty[2 * i] = (touty[2 * i] - touty[2 * i][0]) / 60
                    touty[2 * i + 1] = touty[2 * i + 1][0] - touty[2 * i + 1]

                    fig_courbe, ax = plt.subplots()
                    liss = lissage(touty[2 * i], touty[2 * i + 1], 5)

                    info_courbe(titres[i], 'temps (min)', 'pousse (mm)')
                    intervalle = 45

                    i_max, info_pente = trouver_pente(liss[0], liss[1], 0, intervalle, [0, 0, 0], len(liss[0]), ax)
                    infos_pente_courbes.append(info_pente)
                    infos_pente_courbes[i].append(find_t1(i_max, liss[0], liss[1], intervalle))

                    ax.plot([infos_pente_courbes[i][2] for j in range(len(liss[0]))], np.arange(len(liss[0])),
                            linestyle='--', linewidth=0.5, label="t0")
                    ax.plot([infos_pente_courbes[i][3] for j in range(len(liss[0]))], np.arange(len(liss[0])),
                            linestyle='--', linewidth=0.5, label="t1")
                    # if i == 0:
                    #     fig_courbe.legend(bbox_to_anchor=(0.75, 1.15), ncol=2)
                    plt.ylim(ymin=-3, ymax=max(max_values))
                    ax.plot(liss[0], liss[1], color=COULEURS[i])
                    st.pyplot(fig_courbe)

                else:
                    fig, ax = plt.subplots()
                    st.write("""Pas de données""")
                    st.pyplot(fig)
                # info_courbe("Capteur n°" + str(i + 1), 'temps (min)', 'pousse (mm)', fig_courbe_vide)
                # fig_courbe_vide.grid()

        # courbe des températures
        with col5:
            fig, ax = plt.subplots()
            touty[8] = (touty[8] - touty[8][0]) / 60
            ax.plot(touty[8], touty[9])
            st.pyplot(fig)
            # fig_temp.plot(touty[8], touty[9], color=COULEURS[4])
            plt.ylim(ymin=10)
            info_courbe("temperature", 'temps (min)', 'température  (°c)')

        # toutes les courbes
        # fig_all = fig.add_subplot(236)
        with col6:
            fig, ax = plt.subplots()
            for i in range(4):
                arr = lissage(touty[2 * i], touty[2 * i + 1], 5)
                ax.plot(arr[0], arr[1])
            info_courbe("Capteurs", 'temps (min)', 'pousse (mm)')
            st.pyplot(fig)

    # tableau des infos
    dessiner_tableau(infos_pente_courbes, titres)


def accueil():
    st.title('Poupa')
    with st.container():
        file_input = st.text_input('Fichier de données')
        tab_cpt = []
        for i in range(4):
            capteur_input = st.text_input('Capteur %d' % (i+1))
            tab_cpt.append(capteur_input)
        button = st.button('Lancer')
        if button:
            dessiner_courbes('data\\' + file_input, tab_cpt)


if test:
    accueil()
    # dessiner_courbes('data\PP03-001.TXT', [1, 2, 3, 4])
