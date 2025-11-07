"""
simulation_interactive.py
Simulation interactive du TSP avec interface graphique Matplotlib
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, Slider
from matplotlib.animation import FuncAnimation
from utils import creer_matrice_depuis_coords, calculer_distance
from algo_genetique import algorithme_genetique_tsp
from recuit_simule import recuit_simule


class SimulationTSP:
    def __init__(self):
        # Paramètres
        self.coords_villes = []
        self.matrice_distances = None
        self.meilleur_chemin = None
        self.historique = []
        self.en_cours = False
        self.generation_actuelle = 0

        # Algorithme sélectionné
        self.algo_choisi = "AG - Roulette"
        self.methode_croisement = "2points"

        # Configuration de la figure
        self.fig = plt.figure(figsize=(16, 9))
        self.fig.suptitle("🗺️ SIMULATION TSP - Problème du Voyageur de Commerce",
                          fontsize=16, fontweight='bold')

        # Disposition des subplots
        gs = self.fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

        # 1. Carte des villes (grand, à gauche)
        self.ax_carte = self.fig.add_subplot(gs[:, 0:2])
        self.ax_carte.set_title("🏙️ Cliquez pour placer des villes", fontsize=12, fontweight='bold')
        self.ax_carte.set_xlim(0, 100)
        self.ax_carte.set_ylim(0, 100)
        self.ax_carte.grid(True, alpha=0.3)
        self.ax_carte.set_aspect('equal')

        # 2. Graphique d'évolution (en haut à droite)
        self.ax_evolution = self.fig.add_subplot(gs[0, 2])
        self.ax_evolution.set_title("📈 Évolution de la distance", fontsize=10, fontweight='bold')
        self.ax_evolution.set_xlabel("Génération", fontsize=9)
        self.ax_evolution.set_ylabel("Distance", fontsize=9)
        self.ax_evolution.grid(True, alpha=0.3)

        # 3. Statistiques (milieu à droite)
        self.ax_stats = self.fig.add_subplot(gs[1, 2])
        self.ax_stats.axis('off')
        self.text_stats = self.ax_stats.text(0.1, 0.5, "", fontsize=10,
                                             verticalalignment='center',
                                             family='monospace')

        # 4. Contrôles (bas à droite)
        self.ax_controles = self.fig.add_subplot(gs[2, 2])
        self.ax_controles.axis('off')

        # Création des boutons et widgets
        self.creer_widgets()

        # Event: clic sur la carte
        self.fig.canvas.mpl_connect('button_press_event', self.ajouter_ville)

        plt.show()

    def creer_widgets(self):
        """Crée les boutons et contrôles"""
        # Bouton START
        ax_start = plt.axes([0.70, 0.15, 0.08, 0.04])
        self.btn_start = Button(ax_start, '▶️ START', color='lightgreen', hovercolor='green')
        self.btn_start.on_clicked(self.start_simulation)

        # Bouton RESET
        ax_reset = plt.axes([0.79, 0.15, 0.08, 0.04])
        self.btn_reset = Button(ax_reset, '🔄 RESET', color='lightcoral', hovercolor='red')
        self.btn_reset.on_clicked(self.reset_simulation)

        # Bouton CLEAR
        ax_clear = plt.axes([0.88, 0.15, 0.08, 0.04])
        self.btn_clear = Button(ax_clear, '🗑️ CLEAR', color='lightyellow', hovercolor='yellow')
        self.btn_clear.on_clicked(self.clear_villes)

        # Radio buttons pour choix de l'algorithme
        ax_radio = plt.axes([0.70, 0.02, 0.26, 0.10])
        self.radio_algo = RadioButtons(ax_radio,
                                       ('AG - Roulette', 'AG - Rang', 'Recuit Simulé'),
                                       active=0)
        self.radio_algo.on_clicked(self.changer_algorithme)

        # Radio buttons pour croisement (seulement pour AG)
        ax_radio_crois = plt.axes([0.70, 0.20, 0.26, 0.08])
        self.radio_croisement = RadioButtons(ax_radio_crois,
                                             ('1 point', '2 points', 'Uniforme'),
                                             active=1)
        self.radio_croisement.on_clicked(self.changer_croisement)

    def ajouter_ville(self, event):
        """Ajoute une ville en cliquant sur la carte"""
        if event.inaxes == self.ax_carte and not self.en_cours:
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                self.coords_villes.append((x, y))
                self.ax_carte.plot(x, y, 'ro', markersize=12)
                self.ax_carte.text(x, y + 2, str(len(self.coords_villes) - 1),
                                   ha='center', fontsize=10, fontweight='bold')
                self.fig.canvas.draw()

                # Mettre à jour les stats
                self.afficher_stats()

    def changer_algorithme(self, label):
        """Change l'algorithme sélectionné"""
        self.algo_choisi = label
        self.afficher_stats()

    def changer_croisement(self, label):
        """Change la méthode de croisement"""
        if label == '1 point':
            self.methode_croisement = '1point'
        elif label == '2 points':
            self.methode_croisement = '2points'
        else:
            self.methode_croisement = 'uniforme'

    def start_simulation(self, event):
        """Lance la simulation"""
        if len(self.coords_villes) < 3:
            print("Il faut au moins 3 villes !")
            return

        if self.en_cours:
            return

        self.en_cours = True
        print(f"\n Démarrage de la simulation avec {self.algo_choisi}")

        # Créer la matrice de distances
        self.matrice_distances = creer_matrice_depuis_coords(self.coords_villes)

        # Réinitialiser l'historique
        self.historique = []
        self.generation_actuelle = 0

        # Lancer l'algorithme choisi avec callback
        if "Recuit" in self.algo_choisi:
            self.lancer_recuit_simule()
        else:
            self.lancer_algo_genetique()

    def lancer_algo_genetique(self):
        """Lance l'algorithme génétique avec animation"""
        methode_selection = "roulette" if "Roulette" in self.algo_choisi else "rang"

        def callback_ag(gen, chemin, distance, historique):
            """Callback appelé à chaque génération"""
            self.generation_actuelle = gen
            self.meilleur_chemin = chemin
            self.historique = historique

            # Mise à jour tous les 5 générations
            if gen % 5 == 0:
                self.afficher_chemin()
                self.afficher_evolution()
                self.afficher_stats()
                plt.pause(0.01)

        # Lancer l'AG
        chemin, distance, dist_init, hist = algorithme_genetique_tsp(
            self.matrice_distances,
            generations=200,
            taille_population=50,
            methode_selection=methode_selection,
            methode_croisement=self.methode_croisement,
            proba_croisement=0.8,
            proba_mutation=0.05,
            afficher_graphique=False,
            callback=callback_ag
        )

        self.meilleur_chemin = chemin
        self.historique = hist
        self.afficher_chemin()
        self.afficher_evolution()
        self.afficher_stats()
        self.en_cours = False
        print(f" Simulation terminée ! Distance finale: {distance:.2f}")

    def lancer_recuit_simule(self):
        """Lance le recuit simulé avec animation"""

        def callback_rs(iteration, chemin, distance, historique, temperature):
            """Callback appelé pendant le recuit"""
            self.generation_actuelle = iteration
            self.meilleur_chemin = chemin
            self.historique = historique

            # Mise à jour tous les 50 itérations
            if iteration % 50 == 0:
                self.afficher_chemin()
                self.afficher_evolution()
                self.afficher_stats(temperature=temperature)
                plt.pause(0.01)

        # Lancer le recuit simulé
        chemin, distance, dist_init, hist = recuit_simule(
            self.matrice_distances,
            temperature_initiale=1000,
            temperature_finale=1,
            alpha=0.95,
            iterations_par_temperature=100,
            afficher_graphique=False,
            callback=callback_rs
        )

        self.meilleur_chemin = chemin
        self.historique = hist
        self.afficher_chemin()
        self.afficher_evolution()
        self.afficher_stats()
        self.en_cours = False
        print(f" Simulation terminée ! Distance finale: {distance:.2f}")

    def afficher_chemin(self):
        """Affiche le meilleur chemin sur la carte"""
        if self.meilleur_chemin is None:
            return

        self.ax_carte.clear()
        self.ax_carte.set_title(" Meilleur chemin trouvé", fontsize=12, fontweight='bold')
        self.ax_carte.set_xlim(0, 100)
        self.ax_carte.set_ylim(0, 100)
        self.ax_carte.grid(True, alpha=0.3)
        self.ax_carte.set_aspect('equal')

        # Dessiner les villes
        for i, (x, y) in enumerate(self.coords_villes):
            self.ax_carte.plot(x, y, 'ro', markersize=12)
            self.ax_carte.text(x, y + 2, str(i), ha='center', fontsize=10, fontweight='bold')

        # Dessiner le chemin
        for i in range(len(self.meilleur_chemin)):
            ville_actuelle = self.meilleur_chemin[i]
            ville_suivante = self.meilleur_chemin[(i + 1) % len(self.meilleur_chemin)]

            x1, y1 = self.coords_villes[ville_actuelle]
            x2, y2 = self.coords_villes[ville_suivante]

            self.ax_carte.plot([x1, x2], [y1, y2], 'b-', linewidth=2, alpha=0.6)
            self.ax_carte.arrow(x1, y1, (x2 - x1) * 0.8, (y2 - y1) * 0.8,
                                head_width=2, head_length=2, fc='blue', ec='blue', alpha=0.5)

        self.fig.canvas.draw()

    def afficher_evolution(self):
        """Affiche le graphique d'évolution"""
        if not self.historique:
            return

        self.ax_evolution.clear()
        self.ax_evolution.set_title(" Évolution de la distance", fontsize=10, fontweight='bold')
        self.ax_evolution.plot(self.historique, linewidth=2, color='blue')
        self.ax_evolution.set_xlabel("Génération", fontsize=9)
        self.ax_evolution.set_ylabel("Distance", fontsize=9)
        self.ax_evolution.grid(True, alpha=0.3)
        self.fig.canvas.draw()

    def afficher_stats(self, temperature=None):
        """Affiche les statistiques"""
        nb_villes = len(self.coords_villes)

        stats_text = f" STATISTIQUES\n"
        stats_text += f"{'=' * 25}\n"
        stats_text += f"Villes: {nb_villes}\n"
        stats_text += f"Algorithme: {self.algo_choisi}\n"

        if "AG" in self.algo_choisi:
            stats_text += f"Croisement: {self.methode_croisement}\n"

        if self.historique:
            stats_text += f"\nGénération: {self.generation_actuelle}\n"
            stats_text += f"Distance actuelle: {self.historique[-1]:.2f}\n"
            stats_text += f"Meilleure: {min(self.historique):.2f}\n"

            if temperature is not None:
                stats_text += f"Température: {temperature:.2f}\n"

        self.text_stats.set_text(stats_text)
        self.fig.canvas.draw()

    def reset_simulation(self, event):
        """Réinitialise la simulation"""
        if not self.en_cours:
            self.meilleur_chemin = None
            self.historique = []
            self.generation_actuelle = 0

            self.ax_carte.clear()
            self.ax_carte.set_title(" Cliquez pour placer des villes", fontsize=12, fontweight='bold')
            self.ax_carte.set_xlim(0, 100)
            self.ax_carte.set_ylim(0, 100)
            self.ax_carte.grid(True, alpha=0.3)
            self.ax_carte.set_aspect('equal')

            # Redessiner les villes
            for i, (x, y) in enumerate(self.coords_villes):
                self.ax_carte.plot(x, y, 'ro', markersize=12)
                self.ax_carte.text(x, y + 2, str(i), ha='center', fontsize=10, fontweight='bold')

            self.ax_evolution.clear()
            self.ax_evolution.set_title("Évolution de la distance", fontsize=10, fontweight='bold')
            self.ax_evolution.grid(True, alpha=0.3)

            self.afficher_stats()
            self.fig.canvas.draw()
            print("🔄 Simulation réinitialisée")

    def clear_villes(self, event):
        """Efface toutes les villes"""
        if not self.en_cours:
            self.coords_villes = []
            self.meilleur_chemin = None
            self.historique = []
            self.generation_actuelle = 0

            self.ax_carte.clear()
            self.ax_carte.set_title(" Cliquez pour placer des villes", fontsize=12, fontweight='bold')
            self.ax_carte.set_xlim(0, 100)
            self.ax_carte.set_ylim(0, 100)
            self.ax_carte.grid(True, alpha=0.3)
            self.ax_carte.set_aspect('equal')

            self.ax_evolution.clear()
            self.ax_evolution.set_title("📈 Évolution de la distance", fontsize=10, fontweight='bold')
            self.ax_evolution.grid(True, alpha=0.3)

            self.afficher_stats()
            self.fig.canvas.draw()
            print("🗑️ Toutes les villes ont été effacées")


if __name__ == "__main__":
    print("=" * 60)
    print("  SIMULATION INTERACTIVE DU TSP")
    print("=" * 60)
    print("\n Instructions:")
    print("1. Cliquez sur la carte pour placer des villes")
    print("2. Choisissez un algorithme (AG ou Recuit Simulé)")
    print("3. Pour AG: choisissez le type de croisement")
    print("4. Cliquez sur START pour lancer la simulation")
    print("5. RESET pour recommencer avec les mêmes villes")
    print("6. CLEAR pour tout effacer\n")

    sim = SimulationTSP()