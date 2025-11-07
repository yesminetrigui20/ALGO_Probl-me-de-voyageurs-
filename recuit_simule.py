
import random
import math
import matplotlib.pyplot as plt
from utils import calculer_distance


def recuit_simule(
        matrice,
        temperature_initiale=1000,
        temperature_finale=1,
        alpha=0.95,
        iterations_par_temperature=100,
        afficher_graphique=True,
        callback=None
):
    """Algorithme de recuit simulé pour le TSP"""
    nb_villes = len(matrice)

    chemin_actuel = random.sample(range(nb_villes), nb_villes)
    distance_actuelle = calculer_distance(chemin_actuel, matrice)
    distance_initiale = distance_actuelle

    meilleur_chemin = chemin_actuel[:]
    meilleure_distance = distance_actuelle

    temperature = temperature_initiale
    historique = []
    iteration_globale = 0

    if not callback:
        print(f" Recuit Simulé - Distance initiale: {distance_initiale:.2f}")

    while temperature > temperature_finale:
        for _ in range(iterations_par_temperature):
            nouveau_chemin = chemin_actuel[:]
            i, j = random.sample(range(nb_villes), 2)
            nouveau_chemin[i], nouveau_chemin[j] = nouveau_chemin[j], nouveau_chemin[i]

            nouvelle_distance = calculer_distance(nouveau_chemin, matrice)
            delta = nouvelle_distance - distance_actuelle

            if delta < 0 or random.random() < math.exp(-delta / temperature):
                chemin_actuel = nouveau_chemin
                distance_actuelle = nouvelle_distance

                if distance_actuelle < meilleure_distance:
                    meilleur_chemin = chemin_actuel[:]
                    meilleure_distance = distance_actuelle

            historique.append(meilleure_distance)
            iteration_globale += 1

            if callback and iteration_globale % 10 == 0:
                callback(iteration_globale, meilleur_chemin, meilleure_distance, historique, temperature)

        if not callback and iteration_globale % 1000 == 0:
            print(
                f" Itération {iteration_globale} | Température: {temperature:.2f} | Meilleure distance: {meilleure_distance:.2f}")

        temperature *= alpha

    if not callback:
        print(f" Recuit Simulé terminé - Distance finale: {meilleure_distance:.2f}")

    if afficher_graphique and not callback:
        plt.figure(figsize=(10, 6))
        plt.plot(historique, linewidth=1, alpha=0.7)
        plt.title("Recuit Simulé - Évolution de la meilleure distance", fontsize=14)
        plt.xlabel("Itération", fontsize=12)
        plt.ylabel("Distance minimale", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.show()

    return meilleur_chemin, meilleure_distance, distance_initiale, historique