import numpy as np
from ai import ai
from ai.gameState.gameState import GameState

def get_play(probability_distribution: list[tuple]) -> tuple:
    probability_distribution = np.array(probability_distribution, dtype=list)
    indices = np.arange(len(probability_distribution))
    probabilities = probability_distribution[:, 1].astype(float)
    chosen_index = np.random.choice(indices, p=probabilities)
    return probability_distribution[chosen_index]

def eval(gameState: GameState) -> tuple:
    algorithm_result = ai.algorithm(gameState)
    print("Computed probabilities:")
    for action in algorithm_result:
        print(f"Action: {action[0]}, Probability: {action[1]}")
    return get_play(algorithm_result)
