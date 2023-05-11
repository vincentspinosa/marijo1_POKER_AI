import time
import numpy as np
import random
import copy

def compute_probabilities(array):
    sum = 0
    for el in array:
        sum += el[1]
    for el in array:
        el[1] /= sum
    return array


def cfr(gameState, seconds):
    liste_actions = gameState.available_actions()
    probabilities = [[el, 0] for el in liste_actions]
    gameStateInitial = copy.deepcopy(gameState)
    gameStateTemp = copy.deepcopy(gameState)
    start_time = time.time()
    iterations = 0
    while (time.time() - start_time) < seconds:
        maxReward = None
        index = -1
        for action in liste_actions:
            opposite_player_index = (gameStateTemp.get_player_position(gameStateTemp.target_player) + 1) % len(gameStateTemp.players)
            reward = 0
            gameStateTemp.handle_action(action[0], raise_amount=action[1])
            if action[0] == 'fold':
                reward = 0 - gameStateTemp.current_pot
            else:
                gameStateTemp.go_to_showdown()
                gameStateTemp.players[opposite_player_index].hand = [gameStateTemp.deck.deal() for _ in range(2)]
                winner = gameStateTemp.showdown(gameStateTemp.players)
                if winner == gameStateTemp.target_player:
                    reward = gameStateTemp.current_pot
                elif winner == gameStateTemp.players[opposite_player_index]:
                    reward == 0 - gameStateTemp.current_pot
            gameStateTemp = copy.deepcopy(gameStateInitial)
            gameStateTemp.deck.shuffle()
            if maxReward is not None:
                if reward < maxReward:
                    break
                elif reward == maxReward:
                    if random.choice([True, False]):
                        break
            maxReward = reward
            index += 1
            iterations += 1
        probabilities[index][1] += 1
    print(f"\nNUMBER OF ITERATIONS: {iterations}")
    sum = 0
    for i in range(1, len(probabilities)):
        sum += probabilities[i][1]
    probabilities[0][1] = iterations - sum
    print("Probabilities:")
    for p in probabilities:
        print(p)
    probabilities = compute_probabilities(probabilities)
    print("Computed probabilities:")
    for p in probabilities:
        print(p)
    return probabilities


def get_play(array):
    array = np.array(array, dtype=list)
    indices = np.arange(len(array))
    probabilities = array[:, 1].astype(float)
    chosen_index = np.random.choice(indices, p=probabilities)
    return array[chosen_index]


def eval(gameState):
    return get_play(cfr(gameState, 1))