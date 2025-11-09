from collections import deque
import random


def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale


def generer_voisins(solution):
    voisins = []
    n = len(solution)
    for i in range(n):
        for j in range(i + 1, n):
            v = solution[:]
            v[i], v[j] = v[j], v[i]
            voisins.append(v)
    return voisins


def tabu_search(matrice_distances, nombre_iterations=1000, taille_tabu=10):
    nb_villes = len(matrice_distances)
    solution_actuelle = list(range(nb_villes))
    random.shuffle(solution_actuelle)
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice_distances)
    tabu_list = deque(maxlen=taille_tabu)

    for _ in range(nombre_iterations):
        voisins = [v for v in generer_voisins(solution_actuelle) if v not in tabu_list]
        if not voisins:
            break
        solution_actuelle = min(voisins, key=lambda x: calculer_distance_totale(x, matrice_distances))
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)
        tabu_list.append(solution_actuelle[:])
        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle

    return meilleure_solution, meilleure_distance
