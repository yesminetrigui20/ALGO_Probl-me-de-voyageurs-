
import random
from utils import aptitude

def selection_par_roulette(population, matrice):
    """Sélection par roulette biaisée"""
    total_aptitude = sum(aptitude(ind, matrice) for ind in population)
    tirage = random.uniform(0, total_aptitude)
    cumul = 0
    for individu in population:
        cumul += aptitude(individu, matrice)
        if cumul >= tirage:
            return individu
    return population[-1]