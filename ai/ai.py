import time
import pickle
import random
from treys import Card
from gameState.gameState import GameState

def compute_probabilities(probabilities:list) -> list:
    sum = 0
    for proba in probabilities:
        sum += proba[1]
    for proba in probabilities:
        proba[1] /= sum
    return probabilities

def algorithm(gameState:GameState, seconds:int or float, verbose:bool=False, verboseSteps:int=50) -> dict[list, int]:
    liste_actions = gameState.available_actions()
    probabilities = [[el, 0] for el in liste_actions]
    opposite_player_index = (gameState.get_player_position(gameState.ai_player) + 1) % len(gameState.players)
    gameStateInitial = pickle.dumps(gameState)
    gameStateTemp = pickle.loads(gameStateInitial)
    start_time = time.time()
    iterations = 0
    while (time.time() - start_time) < seconds:
        maxReward = None
        index = -1
        for action in liste_actions:
            reward = 0
            sumAction = gameStateTemp.current_pot + action[1]
            if action[0] == 'fold':
                reward -= sumAction
            elif action[0] in ['call', 'raise', 'all-in']:
                gameStateTemp.ai_deck = gameStateTemp.deck.cards + gameStateTemp.players[opposite_player_index].hand
                random.shuffle(gameStateTemp.ai_deck)
                gameStateTemp.community_cards += [gameStateTemp.ai_deck.pop() for _ in range(5 - len(gameStateTemp.community_cards))]
                gameStateTemp.players[opposite_player_index].hand = [gameStateTemp.ai_deck.pop() for _ in range(2)]
                if verbose == True:
                    if iterations % verboseSteps == 0:
                        print(f"\nIteration {iterations}")
                        print(f"Community cards:")
                        Card.print_pretty_cards(gameStateTemp.community_cards)
                        print(f"Opposite player cards:")
                        Card.print_pretty_cards(gameStateTemp.players[opposite_player_index].hand)
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
            gameStateTemp = pickle.loads(gameStateInitial)
        probabilities[index][1] += 1
    return {'probability_distribution': compute_probabilities(probabilities), 'iterations': iterations}
