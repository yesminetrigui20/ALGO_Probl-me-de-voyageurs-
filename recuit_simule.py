

import random
import math
from utils import calculer_distance

def recuit_simule(matrice_distances,
                  temperature_initiale=1000,
                  temperature_finale=1,
                  alpha=0.95,
                  iterations_par_temperature=100,
                  afficher_graphique=False,
                  callback=None):

    n_villes = len(matrice_distances)
    # Chemin initial aléatoire
    chemin = list(range(n_villes))
    random.shuffle(chemin)
    distance_actuelle = calculer_distance(chemin, matrice_distances)
    distance_initiale = distance_actuelle

    meilleur_chemin = chemin.copy()
    meilleure_distance = distance_actuelle

    temperature = temperature_initiale
    historique = [distance_actuelle]
    iteration_totale = 0

    while temperature > temperature_finale:
        for _ in range(iterations_par_temperature):
            # Générer voisin par swap de 2 villes
            i, j = random.sample(range(n_villes), 2)
            voisin = chemin.copy()
            voisin[i], voisin[j] = voisin[j], voisin[i]
            distance_voisin = calculer_distance(voisin, matrice_distances)

            delta = distance_voisin - distance_actuelle

            if delta < 0 or random.random() < math.exp(-delta / temperature):
                chemin = voisin
                distance_actuelle = distance_voisin

                # Mise à jour du meilleur
                if distance_actuelle < meilleure_distance:
                    meilleur_chemin = chemin.copy()
                    meilleure_distance = distance_actuelle

            historique.append(distance_actuelle)
            iteration_totale += 1

            # Appel du callback pour la simulation interactive
            if callback:
                callback(iteration_totale, chemin, distance_actuelle, historique, temperature)

        temperature *= alpha

    return meilleur_chemin, meilleure_distance, distance_initiale, historique
