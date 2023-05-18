from ai import ai

def eval(gameState, seconds):
    cfr_result = ai.cfr(gameState, seconds)
    print(f"\nNumber of iterations: {cfr_result[1]}")
    print("Computed probabilities:")
    for action in cfr_result[0]:
        print(f"Action: {action[0]}, Probability: {action[1]}")
    return ai.get_play(cfr_result[0])