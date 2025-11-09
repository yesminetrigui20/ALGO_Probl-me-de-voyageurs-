import matplotlib.pyplot as plt
from algo_genetique import algorithme_genetique_tsp
from recuit_simule import recuit_simule

def comparer_algorithmes(matrice):

    print("=" * 80)
    print("COMPARAISON DES ALGORITHMES - TSP")
    print("=" * 80)

    # Configurations AG à tester
    selections = ["roulette", "rang"]
    croisements = ["1point", "2points", "uniforme"]

    resultats = []

    for sel in selections:
        for crois in croisements:
            print(f"\nALGO GENETIQUE - {sel.capitalize()} + {crois.capitalize()}")
            print("-" * 80)
            sol, dist, dist_init, hist = algorithme_genetique_tsp(
                matrice,
                generations=200,
                taille_population=50,
                methode_selection=sel,
                methode_croisement=crois,
                proba_croisement=0.8,
                proba_mutation=0.05,
                afficher_graphique=False
            )
            print(f" Chemin trouvé: {sol}")
            print(f" Distance initiale: {dist_init:.2f}")
            print(f" Distance finale: {dist:.2f}")
            resultats.append((f"AG - {sel.capitalize()} + {crois.capitalize()}", dist, hist))

    # Recuit simulé
    print("\nRECUIT SIMULÉ")
    print("-" * 80)
    sol_rs, dist_rs, init_rs, hist_rs = recuit_simule(
        matrice,
        temperature_initiale=1000,
        temperature_finale=1,
        alpha=0.95,
        iterations_par_temperature=100,
        afficher_graphique=False
    )
    print(f" Chemin trouvé: {sol_rs}")
    print(f" Distance initiale: {init_rs:.2f}")
    print(f" Distance finale: {dist_rs:.2f}")
    resultats.append(("Recuit Simulé", dist_rs, hist_rs))

    # 🔹 Graphique comparatif
    plt.figure(figsize=(14, 8))
    for nom, _, hist in resultats[:-1]:  # AG
        plt.plot(hist, label=nom, linewidth=2)

    # Recuit simulé (normaliser X)
    x_rs = [i * (200 / len(hist_rs)) for i in range(len(hist_rs))]
    plt.plot(x_rs, hist_rs, label="Recuit Simulé", linewidth=2, linestyle='--')

    plt.title("Comparaison des Algorithmes - TSP", fontsize=16, fontweight='bold')
    plt.xlabel("Génération / Itération normalisée", fontsize=12)
    plt.ylabel("Distance minimale", fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # 🔹 Tableau récapitulatif
    print("\n" + "=" * 80)
    print("TABLEAU RÉCAPITULATIF")
    print("=" * 80)
    resultats_table = [(nom, dist) for nom, dist, _ in resultats]
    resultats_table.sort(key=lambda x: x[1])
    print(f"\n{'Rang':<5} {'Algorithme':<30} {'Distance':<10}")
    print("-" * 80)
    for i, (nom, distance) in enumerate(resultats_table, 1):
        print(f"{i:<5} {nom:<30} {distance:<10.2f}")

if __name__ == "__main__":
    # Matrice de distances exemple (10 villes)
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

    comparer_algorithmes(matrice_10_villes)
