
import random
from utils import aptitude


def selection_par_rang(population, matrice):
    """Sélection par rang"""
    fitness = [(ind, aptitude(ind, matrice)) for ind in population]
    fitness.sort(key=lambda x: x[1])
    population_triee = [ind for ind, _ in fitness]

    rangs = list(range(1, len(population) + 1))
    somme_rangs = sum(rangs)

    tirage = random.uniform(0, somme_rangs)
    cumul = 0
    for i, individu in enumerate(population_triee):
        cumul += rangs[i]
        if cumul >= tirage:
            return individu
    return population_triee[-1]