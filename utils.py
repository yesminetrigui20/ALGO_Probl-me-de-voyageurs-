
import math

def calculer_distance(chemin, matrice):
    """Calcule la distance totale d'un chemin (avec retour à la ville de départ)"""
    distance = 0
    for i in range(len(chemin)):
        ville_actuelle = chemin[i]
        ville_suivante = chemin[(i + 1) % len(chemin)]
        distance += matrice[ville_actuelle][ville_suivante]
    return distance

def aptitude(chemin, matrice):
    """Calcule le fitness d'un chemin (inverse de la distance)"""
    return 1 / calculer_distance(chemin, matrice)

def calculer_distance_euclidienne(ville1, ville2):
    """Calcule la distance euclidienne entre deux villes"""
    return math.sqrt((ville1[0] - ville2[0])**2 + (ville1[1] - ville2[1])**2)

def creer_matrice_depuis_coords(coords):
    """Crée une matrice de distances à partir de coordonnées"""
    n = len(coords)
    matrice = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrice[i][j] = calculer_distance_euclidienne(coords[i], coords[j])
    return matrice