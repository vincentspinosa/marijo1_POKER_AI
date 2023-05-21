import numpy as np
from ai import ai

def get_play(array):
    array = np.array(array, dtype=list)
    indices = np.arange(len(array))
    probabilities = array[:, 1].astype(float)
    chosen_index = np.random.choice(indices, p=probabilities)
    return array[chosen_index]

def eval(gameState, seconds):
    cfr_result = ai.cfr(gameState, seconds)
    print(f"\nNumber of iterations: {cfr_result[1]}")
    print("Computed probabilities:")
    for action in cfr_result[0]:
        print(f"Action: {action[0]}, Probability: {action[1]}")
    return get_play(cfr_result[0])