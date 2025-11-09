# -*- coding: utf-8 -*-
"""
Simulation interactive du TSP avec interface graphique Matplotlib
Compatible avec : algo_genetique.py, recuit_simule.py, tabou.py, utils.py
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons
from utils import creer_matrice_depuis_coords
from algo_genetique import algorithme_genetique_tsp
from recuit_simule import recuit_simule
from tabou import tabu_search


class SimulationTSP:
    def __init__(self):
        self.coords_villes = []
        self.matrice_distances = None
        self.meilleur_chemin = None
        self.historique = []
        self.en_cours = False
        self.iteration_actuelle = 0

        # Algorithme sélectionné
        self.algo_choisi = "AG - Roulette"
        self.methode_croisement = "2points"

        # Création figure
        self.fig = plt.figure(figsize=(16, 9))
        self.fig.suptitle(" Simulation TSP - Voyageur de Commerce", fontsize=16, fontweight='bold')

        # Disposition
        gs = self.fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

        # 1. Carte
        self.ax_carte = self.fig.add_subplot(gs[:, 0:2])
        self.ax_carte.set_title("Cliquez pour placer des villes", fontsize=12, fontweight='bold')
        self.ax_carte.set_xlim(0, 100)
        self.ax_carte.set_ylim(0, 100)
        self.ax_carte.grid(True, alpha=0.3)
        self.ax_carte.set_aspect('equal')

        # 2. Évolution
        self.ax_evolution = self.fig.add_subplot(gs[0, 2])
        self.ax_evolution.set_title("Évolution de la distance", fontsize=10, fontweight='bold')
        self.ax_evolution.set_xlabel("Itération / Génération", fontsize=9)
        self.ax_evolution.set_ylabel("Distance", fontsize=9)
        self.ax_evolution.grid(True, alpha=0.3)

        # 3. Stats
        self.ax_stats = self.fig.add_subplot(gs[1, 2])
        self.ax_stats.axis('off')
        self.text_stats = self.ax_stats.text(0.1, 0.5, "", fontsize=10, family='monospace',
                                             verticalalignment='center')

        # 4. Contrôles
        self.ax_controles = self.fig.add_subplot(gs[2, 2])
        self.ax_controles.axis('off')

        self.creer_widgets()
        self.fig.canvas.mpl_connect('button_press_event', self.ajouter_ville)
        plt.show()

    def creer_widgets(self):
        """Crée les boutons"""
        ax_start = plt.axes([0.70, 0.15, 0.08, 0.04])
        self.btn_start = Button(ax_start, '▶️ START', color='lightgreen', hovercolor='green')
        self.btn_start.on_clicked(self.start_simulation)

        ax_reset = plt.axes([0.79, 0.15, 0.08, 0.04])
        self.btn_reset = Button(ax_reset, '🔄 RESET', color='lightcoral', hovercolor='red')
        self.btn_reset.on_clicked(self.reset_simulation)

        ax_clear = plt.axes([0.88, 0.15, 0.08, 0.04])
        self.btn_clear = Button(ax_clear, '🗑️ CLEAR', color='lightyellow', hovercolor='yellow')
        self.btn_clear.on_clicked(self.clear_villes)

        # Radio boutons pour algorithme
        ax_radio = plt.axes([0.70, 0.02, 0.26, 0.10])
        self.radio_algo = RadioButtons(ax_radio,
                                       ('AG - Roulette', 'AG - Rang', 'Recuit Simulé', 'Tabou'),
                                       active=0)
        self.radio_algo.on_clicked(self.changer_algorithme)

        # Radio boutons pour croisement
        ax_radio_crois = plt.axes([0.70, 0.20, 0.26, 0.08])
        self.radio_croisement = RadioButtons(ax_radio_crois,
                                             ('1 point', '2 points', 'Uniforme'),
                                             active=1)
        self.radio_croisement.on_clicked(self.changer_croisement)

    def ajouter_ville(self, event):
        """Ajoute une ville sur clic"""
        if event.inaxes == self.ax_carte and not self.en_cours:
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                self.coords_villes.append((x, y))
                self.ax_carte.plot(x, y, 'ro', markersize=10)
                self.ax_carte.text(x, y + 2, str(len(self.coords_villes) - 1),
                                   ha='center', fontsize=9, fontweight='bold')
                self.fig.canvas.draw()
                self.afficher_stats()

    def changer_algorithme(self, label):
        self.algo_choisi = label
        self.afficher_stats()

    def changer_croisement(self, label):
        if label == '1 point':
            self.methode_croisement = '1point'
        elif label == '2 points':
            self.methode_croisement = '2points'
        else:
            self.methode_croisement = 'uniforme'

    def start_simulation(self, event):
        """Lance la simulation"""
        if len(self.coords_villes) < 3:
            print("⚠️ Il faut au moins 3 villes !")
            return
        if self.en_cours:
            return

        self.en_cours = True
        print(f"\n🚀 Démarrage de la simulation avec {self.algo_choisi}")

        self.matrice_distances = creer_matrice_depuis_coords(self.coords_villes)
        self.historique = []
        self.iteration_actuelle = 0

        if "Recuit" in self.algo_choisi:
            self.lancer_recuit_simule()
        elif "Tabou" in self.algo_choisi:
            self.lancer_tabou()
        else:
            self.lancer_algo_genetique()

    def lancer_algo_genetique(self):
        methode_selection = "roulette" if "Roulette" in self.algo_choisi else "rang"

        def callback(gen, chemin, distance, historique):
            self.iteration_actuelle = gen
            self.meilleur_chemin = chemin
            self.historique = historique
            if gen % 5 == 0:
                self.afficher_chemin()
                self.afficher_evolution()
                self.afficher_stats()
                plt.pause(0.01)

        chemin, distance, _, hist = algorithme_genetique_tsp(
            self.matrice_distances,
            generations=200,
            taille_population=50,
            methode_selection=methode_selection,
            methode_croisement=self.methode_croisement,
            proba_croisement=0.8,
            proba_mutation=0.05,
            afficher_graphique=False,
            callback=callback
        )

        self.meilleur_chemin = chemin
        self.historique = hist
        self.afficher_chemin()
        self.afficher_evolution()
        self.afficher_stats()
        self.en_cours = False
        print(f"Simulation terminée ! Distance finale: {distance:.2f}")

    def lancer_recuit_simule(self):
        def callback(iteration, chemin, distance, historique, temperature):
            self.iteration_actuelle = iteration
            self.meilleur_chemin = chemin
            self.historique = historique
            if iteration % 50 == 0:
                self.afficher_chemin()
                self.afficher_evolution()
                self.afficher_stats(temperature=temperature)
                plt.pause(0.01)

        chemin, distance, _, hist = recuit_simule(
            self.matrice_distances,
            temperature_initiale=1000,
            temperature_finale=1,
            alpha=0.95,
            iterations_par_temperature=100,
            afficher_graphique=False,
            callback=callback
        )

        self.meilleur_chemin = chemin
        self.historique = hist
        self.afficher_chemin()
        self.afficher_evolution()
        self.afficher_stats()
        self.en_cours = False
        print(f" Recuit terminé ! Distance finale: {distance:.2f}")

    def lancer_tabou(self):
        """Exécute la recherche tabou"""
        def callback(iteration, chemin, distance, historique):
            self.iteration_actuelle = iteration
            self.meilleur_chemin = chemin
            self.historique = historique
            if iteration % 10 == 0:
                self.afficher_chemin()
                self.afficher_evolution()
                self.afficher_stats()
                plt.pause(0.01)

        chemin, distance = tabu_search(
            self.matrice_distances,
            nombre_iterations=300,
            taille_tabu=20
        )
        self.meilleur_chemin = chemin
        self.historique = [distance]
        self.afficher_chemin()
        self.afficher_evolution()
        self.afficher_stats()
        self.en_cours = False
        print(f"Recherche Tabou terminée ! Distance finale: {distance:.2f}")

    def afficher_chemin(self):
        if self.meilleur_chemin is None:
            return

        self.ax_carte.clear()
        self.ax_carte.set_title("Meilleur chemin trouvé", fontsize=12, fontweight='bold')
        self.ax_carte.set_xlim(0, 100)
        self.ax_carte.set_ylim(0, 100)
        self.ax_carte.grid(True, alpha=0.3)
        self.ax_carte.set_aspect('equal')

        for i, (x, y) in enumerate(self.coords_villes):
            self.ax_carte.plot(x, y, 'ro', markersize=10)
            self.ax_carte.text(x, y + 2, str(i), ha='center', fontsize=9, fontweight='bold')

        for i in range(len(self.meilleur_chemin)):
            a, b = self.meilleur_chemin[i], self.meilleur_chemin[(i + 1) % len(self.meilleur_chemin)]
            x1, y1 = self.coords_villes[a]
            x2, y2 = self.coords_villes[b]
            self.ax_carte.plot([x1, x2], [y1, y2], 'b-', linewidth=2, alpha=0.6)

        self.fig.canvas.draw()

    def afficher_evolution(self):
        if not self.historique:
            return
        self.ax_evolution.clear()
        self.ax_evolution.set_title("Évolution de la distance", fontsize=10, fontweight='bold')
        self.ax_evolution.plot(self.historique, linewidth=2, color='blue')
        self.ax_evolution.grid(True, alpha=0.3)
        self.fig.canvas.draw()

    def afficher_stats(self, temperature=None):
        nb_villes = len(self.coords_villes)
        txt = f"Villes: {nb_villes}\nAlgorithme: {self.algo_choisi}\n"
        if "AG" in self.algo_choisi:
            txt += f"Croisement: {self.methode_croisement}\n"
        if self.historique:
            txt += f"Iteration: {self.iteration_actuelle}\n"
            txt += f"Distance: {self.historique[-1]:.2f}\n"
            txt += f"Meilleure: {min(self.historique):.2f}\n"
        if temperature:
            txt += f"Température: {temperature:.2f}\n"
        self.text_stats.set_text(txt)
        self.fig.canvas.draw()

    def reset_simulation(self, event):
        if not self.en_cours:
            self.meilleur_chemin = None
            self.historique = []
            self.iteration_actuelle = 0
            self.ax_carte.clear()
            self.ax_carte.set_xlim(0, 100)
            self.ax_carte.set_ylim(0, 100)
            self.ax_carte.grid(True, alpha=0.3)
            for i, (x, y) in enumerate(self.coords_villes):
                self.ax_carte.plot(x, y, 'ro', markersize=10)
                self.ax_carte.text(x, y + 2, str(i), ha='center', fontsize=9, fontweight='bold')
            self.afficher_stats()
            self.fig.canvas.draw()
            print(" Simulation réinitialisée")

    def clear_villes(self, event):
        if not self.en_cours:
            self.coords_villes = []
            self.meilleur_chemin = None
            self.historique = []
            self.iteration_actuelle = 0
            self.ax_carte.clear()
            self.ax_carte.set_xlim(0, 100)
            self.ax_carte.set_ylim(0, 100)
            self.ax_carte.grid(True, alpha=0.3)
            self.afficher_stats()
            self.fig.canvas.draw()
            print(" Toutes les villes ont été effacées")


if __name__ == "__main__":
    print("=" * 60)
    print("SIMULATION INTERACTIVE DU TSP")
    print("=" * 60)
    print(" Cliquez pour placer des villes")
    print("⃣ Choisissez un algorithme")
    print("Cliquez sur START pour lancer la simulation\n")
    SimulationTSP()
