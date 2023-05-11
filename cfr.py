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
    opposite_player_index = (gameState.get_player_position(gameState.target_player) + 1) % len(gameState.players)
    gameStateInitial = copy.deepcopy(gameState)
    start_time = time.time()
    iterations = 0
    while (time.time() - start_time) < seconds:
        gameStateTemp = copy.deepcopy(gameStateInitial)
        maxReward = None
        index = -1
        for action in liste_actions:
            gameStateTemp.deck.shuffle()
            reward = 0
            sumAction = gameStateTemp.current_pot + action[1]
            if action[0] == 'fold':
                reward -= sumAction
            else:
                gameStateTemp.go_to_showdown()
                gameStateTemp.players[opposite_player_index].hand = [gameStateTemp.deck.deal() for _ in range(2)]
                winner = gameStateTemp.showdown(gameStateTemp.players)
                if winner == gameStateTemp.target_player:
                    reward += sumAction
                elif winner == gameStateTemp.players[opposite_player_index]:
                    reward -= sumAction
            if maxReward is not None:
                if reward < maxReward or (reward == maxReward and random.choice([True, False])):
                    break
            maxReward = copy.copy(reward)
            index += 1
            iterations += 1
        probabilities[index][1] += 1
    """ print(f"\nNUMBER OF ITERATIONS: {iterations}")
    print("Probabilities:")
    for p in probabilities:
        print(p) """
    probabilities = compute_probabilities(probabilities)
    """ print("Computed probabilities:")
    for p in probabilities:
        print(p) """
    return probabilities


def get_play(array):
    array = np.array(array, dtype=list)
    indices = np.arange(len(array))
    probabilities = array[:, 1].astype(float)
    chosen_index = np.random.choice(indices, p=probabilities)
    return array[chosen_index]


def eval(gameState):
    return get_play(cfr(gameState, 50))