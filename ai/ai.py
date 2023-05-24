import time
import pickle
from gameState import gameState

def compute_probabilities(probabilities:list) -> list:
    sum = 0
    for proba in probabilities:
        sum += proba[1]
    for proba in probabilities:
        proba[1] /= sum
    return probabilities

def algorithm(gameState:gameState.GameState, seconds:int or float) -> dict[list, int]:
    liste_actions = gameState.available_actions()
    probabilities = [[el, 0] for el in liste_actions]
    opposite_player_index = (gameState.get_player_position(gameState.ai_player) + 1) % len(gameState.players)
    gameStateInitial = pickle.dumps(gameState)
    start_time = time.time()
    iterations = 0
    while (time.time() - start_time) < seconds:
        gameStateTemp = pickle.loads(gameStateInitial)
        maxReward = None
        index = -1
        for action in liste_actions:
            reward = 0
            sumAction = gameStateTemp.current_pot + action[1]
            if action[0] == 'fold':
                reward -= sumAction
            elif action[0] in ['call', 'raise', 'all-in']:
                gameStateTemp.deck.shuffle()
                gameStateTemp.go_to_showdown()
                gameStateTemp.players[opposite_player_index].hand = [gameStateTemp.deck.deal() for _ in range(2)]
                winner = gameStateTemp.showdown(gameStateTemp.players)
                if winner == gameStateTemp.ai_player:
                    reward += sumAction
                elif winner == gameStateTemp.players[opposite_player_index]:
                    reward -= sumAction
            if maxReward is not None and reward < maxReward:
                break
            maxReward = reward
            index += 1
            iterations += 1
        probabilities[index][1] += 1
    return {'probability_distribution': compute_probabilities(probabilities), 'iterations': iterations}
