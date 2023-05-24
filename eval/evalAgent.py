import numpy as np
from ai import ai
from gameState.gameState import GameState

def get_play(probability_distribution: list[tuple]) -> tuple:
    probability_distribution = np.array(probability_distribution, dtype=list)
    indices = np.arange(len(probability_distribution))
    probabilities = probability_distribution[:, 1].astype(float)
    chosen_index = np.random.choice(indices, p=probabilities)
    return probability_distribution[chosen_index]

def eval(gameState: GameState, seconds: int or float) -> tuple:
    algorithm_result = ai.algorithm(gameState, seconds)
    print(f"\nNumber of iterations: {algorithm_result['iterations']}")
    print("Computed probabilities:")
    for action in algorithm_result['probability_distribution']:
        print(f"Action: {action[0]}, Probability: {action[1]}")
    return get_play(algorithm_result['probability_distribution'])
