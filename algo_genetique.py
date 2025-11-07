
import random
import matplotlib.pyplot as plt
from utils import calculer_distance
from selection_roulette import selection_par_roulette
from selection_rang import selection_par_rang

# Opérateurs de croisement
def croisement_un_point(parent1, parent2):
    """Croisement en un point"""
    point = random.randint(1, len(parent1) - 2)
    partie1 = parent1[:point]
    partie2 = [v for v in parent2 if v not in partie1]
    return partie1 + partie2

def croisement_deux_points(parent1, parent2):
    """Croisement en deux points"""
    a, b = sorted(random.sample(range(len(parent1)), 2))
    segment = parent1[a:b]
    base = [v for v in parent2 if v not in segment]
    return base[:a] + segment + base[a:]

def croisement_uniforme(parent1, parent2):
    """Croisement uniforme avec masque binaire"""
    masque = [random.randint(0, 1) for _ in range(len(parent1))]
    enfant_temp = [parent1[i] if masque[i] else parent2[i] for i in range(len(parent1))]

    villes_vues = set()
    enfant_final = []
    for v in enfant_temp:
        if v not in villes_vues:
            villes_vues.add(v)
            enfant_final.append(v)
    for v in parent1:
        if v not in villes_vues:
            enfant_final.append(v)
    return enfant_final

# Opérateur de mutation
def mutation(chemin):
    """Mutation par échange de deux villes"""
    i, j = random.sample(range(len(chemin)), 2)
    chemin[i], chemin[j] = chemin[j], chemin[i]

# Algorithme génétique complet
def algorithme_genetique_tsp(
    matrice,
    generations=200,
    taille_population=50,
    proba_croisement=0.8,
    proba_mutation=0.05,
    methode_selection="roulette",
    methode_croisement="2points",
    afficher_graphique=True,
    callback=None
):
    """Algorithme génétique pour le TSP avec élitisme"""
    nb_villes = len(matrice)
    population = [random.sample(range(nb_villes), nb_villes) for _ in range(taille_population)]
    historique = []

    meilleur_initial = min(population, key=lambda p: calculer_distance(p, matrice))
    distance_initiale = calculer_distance(meilleur_initial, matrice)

    for gen in range(generations):
        nouvelle_population = []

        meilleur = min(population, key=lambda p: calculer_distance(p, matrice))
        meilleure_distance = calculer_distance(meilleur, matrice)
        nouvelle_population.append(meilleur[:])
        historique.append(meilleure_distance)

        while len(nouvelle_population) < taille_population:
            if methode_selection == "roulette":
                parent1 = selection_par_roulette(population, matrice)
                parent2 = selection_par_roulette(population, matrice)
            else:
                parent1 = selection_par_rang(population, matrice)
                parent2 = selection_par_rang(population, matrice)

            if random.random() < proba_croisement:
                if methode_croisement == "1point":
                    enfant = croisement_un_point(parent1, parent2)
                elif methode_croisement == "2points":
                    enfant = croisement_deux_points(parent1, parent2)
                else:
                    enfant = croisement_uniforme(parent1, parent2)
            else:
                enfant = parent1[:]

            if random.random() < proba_mutation:
                mutation(enfant)

            nouvelle_population.append(enfant)

        population = nouvelle_population

        if callback:
            callback(gen, meilleur, meilleure_distance, historique)

        if not callback:
            print(f"🌀 Génération {gen+1}/{generations} | Meilleure distance = {meilleure_distance:.2f}")

    meilleur = min(population, key=lambda p: calculer_distance(p, matrice))
    meilleure_distance = calculer_distance(meilleur, matrice)

    if afficher_graphique and not callback:
        plt.figure(figsize=(10, 6))
        plt.plot(historique, linewidth=2)
        plt.title("Algorithme Génétique - Évolution de la meilleure distance", fontsize=14)
        plt.xlabel("Génération", fontsize=12)
        plt.ylabel("Distance minimale", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.show()

    return meilleur, meilleure_distance, distance_initiale, historique