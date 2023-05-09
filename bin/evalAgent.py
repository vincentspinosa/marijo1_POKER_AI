import numpy as np
from ..cfr import cfr

def get_play(arrayProbas):
    indices = np.arange(len(arrayProbas))
    probabilities = arrayProbas[:, 1].astype(float)
    chosen_index = np.random.choice(indices, p=probabilities)
    return arrayProbas[chosen_index]

def eval(gameState):
    eval = get_play(cfr(gameState))
    return eval