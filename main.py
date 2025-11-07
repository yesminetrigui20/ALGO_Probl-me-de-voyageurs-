
import matplotlib.pyplot as plt
from algo_genetique import algorithme_genetique_tsp
from recuit_simule import recuit_simule


def comparer_algorithmes(matrice):
    """
    Compare l'algorithme génétique et le recuit simulé
    """
    print("=" * 80)
    print("COMPARAISON DES ALGORITHMES - PROBLÈME DU VOYAGEUR DE COMMERCE")
    print("=" * 80)

    #  1. Algorithme Génétique - Sélection Roulette - Croisement 1 point
    print("\n  ALGORITHME GÉNÉTIQUE - Roulette + Croisement 1 point")
    print("-" * 80)
    sol_ag1, dist_ag1, init_ag1, hist_ag1 = algorithme_genetique_tsp(
        matrice,
        generations=200,
        taille_population=50,
        methode_selection="roulette",
        methode_croisement="1point",
        proba_croisement=0.8,
        proba_mutation=0.05,
        afficher_graphique=False
    )
    print(f" Chemin trouvé: {sol_ag1}")
    print(f" Distance initiale: {init_ag1:.2f}")
    print(f" Distance finale: {dist_ag1:.2f}")

    #  2. Algorithme Génétique - Sélection Roulette - Croisement 2 points
    print("\n  ALGORITHME GÉNÉTIQUE - Roulette + Croisement 2 points")
    print("-" * 80)
    sol_ag2, dist_ag2, init_ag2, hist_ag2 = algorithme_genetique_tsp(
        matrice,
        generations=200,
        taille_population=50,
        methode_selection="roulette",
        methode_croisement="2points",
        proba_croisement=0.8,
        proba_mutation=0.05,
        afficher_graphique=False
    )
    print(f" Chemin trouvé: {sol_ag2}")
    print(f" Distance initiale: {init_ag2:.2f}")
    print(f" Distance finale: {dist_ag2:.2f}")

    #  3. Algorithme Génétique - Sélection Roulette - Croisement Uniforme
    print("\n ALGORITHME GÉNÉTIQUE - Roulette + Croisement Uniforme")
    print("-" * 80)
    sol_ag3, dist_ag3, init_ag3, hist_ag3 = algorithme_genetique_tsp(
        matrice,
        generations=200,
        taille_population=50,
        methode_selection="roulette",
        methode_croisement="uniforme",
        proba_croisement=0.8,
        proba_mutation=0.05,
        afficher_graphique=False
    )
    print(f" Chemin trouvé: {sol_ag3}")
    print(f" Distance initiale: {init_ag3:.2f}")
    print(f" Distance finale: {dist_ag3:.2f}")

    #  4. Algorithme Génétique - Sélection Rang - Croisement 1 point
    print("\n  ALGORITHME GÉNÉTIQUE - Rang + Croisement 1 point")
    print("-" * 80)
    sol_ag4, dist_ag4, init_ag4, hist_ag4 = algorithme_genetique_tsp(
        matrice,
        generations=200,
        taille_population=50,
        methode_selection="rang",
        methode_croisement="1point",
        proba_croisement=0.8,
        proba_mutation=0.05,
        afficher_graphique=False
    )
    print(f" Chemin trouvé: {sol_ag4}")
    print(f" Distance initiale: {init_ag4:.2f}")
    print(f"Distance finale: {dist_ag4:.2f}")

    # 🔹 5. Algorithme Génétique - Sélection Rang - Croisement 2 points
    print("\n  ALGORITHME GÉNÉTIQUE - Rang + Croisement 2 points")
    print("-" * 80)
    sol_ag5, dist_ag5, init_ag5, hist_ag5 = algorithme_genetique_tsp(
        matrice,
        generations=200,
        taille_population=50,
        methode_selection="rang",
        methode_croisement="2points",
        proba_croisement=0.8,
        proba_mutation=0.05,
        afficher_graphique=False
    )
    print(f" Chemin trouvé: {sol_ag5}")
    print(f" Distance initiale: {init_ag5:.2f}")
    print(f" Distance finale: {dist_ag5:.2f}")

    # 🔹 6. Algorithme Génétique - Sélection Rang - Croisement Uniforme
    print("\n⃣  ALGORITHME GÉNÉTIQUE - Rang + Croisement Uniforme")
    print("-" * 80)
    sol_ag6, dist_ag6, init_ag6, hist_ag6 = algorithme_genetique_tsp(
        matrice,
        generations=200,
        taille_population=50,
        methode_selection="rang",
        methode_croisement="uniforme",
        proba_croisement=0.8,
        proba_mutation=0.05,
        afficher_graphique=False
    )
    print(f" Chemin trouvé: {sol_ag6}")
    print(f" Distance initiale: {init_ag6:.2f}")
    print(f" Distance finale: {dist_ag6:.2f}")

    # 🔹 7. Recuit Simulé
    print("\n RECUIT SIMULÉ")
    print("-" * 80)
    sol_rs, dist_rs, init_rs, hist_rs = recuit_simule(
        matrice,
        temperature_initiale=1000,
        temperature_finale=1,
        alpha=0.95,
        iterations_par_temperature=100,
        afficher_graphique=False
    )
    print(f"Chemin trouvé: {sol_rs}")
    print(f" Distance initiale: {init_rs:.2f}")
    print(f"Distance finale: {dist_rs:.2f}")

    # 🔸 Graphique comparatif
    print("\n Génération du graphique comparatif...")
    plt.figure(figsize=(14, 8))

    plt.plot(hist_ag1, label="AG - Roulette + 1 point", linewidth=2)
    plt.plot(hist_ag2, label="AG - Roulette + 2 points", linewidth=2)
    plt.plot(hist_ag3, label="AG - Roulette + Uniforme", linewidth=2)
    plt.plot(hist_ag4, label="AG - Rang + 1 point", linewidth=2)
    plt.plot(hist_ag5, label="AG - Rang + 2 points", linewidth=2)
    plt.plot(hist_ag6, label="AG - Rang + Uniforme", linewidth=2)

    # Adapter l'axe X pour le recuit simulé (beaucoup plus d'itérations)
    x_rs = [i * (200 / len(hist_rs)) for i in range(len(hist_rs))]
    plt.plot(x_rs, hist_rs, label="Recuit Simulé", linewidth=2, linestyle='--')

    plt.title("Comparaison des Algorithmes - TSP", fontsize=16, fontweight='bold')
    plt.xlabel("Génération / Itération normalisée", fontsize=12)
    plt.ylabel("Distance minimale", fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # 🔸 Tableau récapitulatif
    print("\n" + "=" * 80)
    print("TABLEAU RÉCAPITULATIF")
    print("=" * 80)
    resultats = [
        ("AG - Roulette + 1 point", dist_ag1),
        ("AG - Roulette + 2 points", dist_ag2),
        ("AG - Roulette + Uniforme", dist_ag3),
        ("AG - Rang + 1 point", dist_ag4),
        ("AG - Rang + 2 points", dist_ag5),
        ("AG - Rang + Uniforme", dist_ag6),
        ("Recuit Simulé", dist_rs)
    ]

    resultats.sort(key=lambda x: x[1])
    print(f"\n{'Rang':<5} {'Algorithme':<30} {'Distance':<10}")
    print("-" * 80)
    for i, (nom, distance) in enumerate(resultats, 1):
        print(f"{i:<5} {nom:<30} {distance:<10.2f}")


if __name__ == "__main__":
    # Matrice de distances - 10 villes
    matrice_10_villes = [
        [0, 29, 20, 21, 16, 31, 100, 12, 4, 31],
        [29, 0, 15, 29, 28, 40, 72, 21, 29, 27],
        [20, 15, 0, 28, 24, 27, 81, 9, 23, 30],
        [21, 29, 28, 0, 12, 25, 91, 17, 21, 16],
        [16, 28, 24, 12, 0, 17, 101, 8, 18, 22],
        [31, 40, 27, 25, 17, 0, 110, 19, 31, 14],
        [100, 72, 81, 91, 101, 110, 0, 90, 85, 95],
        [12, 21, 9, 17, 8, 19, 90, 0, 11, 18],
        [4, 29, 23, 21, 18, 31, 85, 11, 0, 25],
        [31, 27, 30, 16, 22, 14, 95, 18, 25, 0]
    ]

    # Lancer la comparaison
    comparer_algorithmes(matrice_10_villes)