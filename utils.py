
import math

def calculer_distance(chemin, matrice):
    """Calcule la distance totale d'un chemin (retour à la ville de départ)."""
    distance = 0
    n = len(chemin)
    for i in range(n):
        distance += matrice[chemin[i]][chemin[(i + 1) % n]]
    return distance

def aptitude(chemin, matrice):
    """Fitness : inverse de la distance totale ."""
    return 1 / calculer_distance(chemin, matrice)

def calculer_distance_euclidienne(ville1, ville2):
    """Distance euclidienne entre deux villes."""
    return math.sqrt((ville1[0] - ville2[0])**2 + (ville1[1] - ville2[1])**2)

def creer_matrice_depuis_coords(coords):
    """Crée une matrice de distances à partir d'une liste de coordonnées """
    n = len(coords)
    matrice = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrice[i][j] = calculer_distance_euclidienne(coords[i], coords[j])
    return matrice
