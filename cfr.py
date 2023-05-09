import time
import numpy as np
import random


def compute_probabilities(arrayInput):
    arrayInput = np.array(arrayInput)
    integers = arrayInput[:, 1].astype(int)
    total = np.sum(integers)
    arrayProbas = integers / total
    result = []
    for index, proba in enumerate(arrayProbas):
        result.append([arrayInput[index, 0], proba])
    return np.array(result)


def cfr(gameState, seconds):
    liste_actions = gameState.current_player.available_actions()
    probabilities = [[el, 0] for el in liste_actions]
    gameStateInitial = gameState
    start_time = time.time()
    while (time.time() - start_time) < seconds:
        gameState = gameStateInitial
        gameState.deck.shuffle()
        maxReward = None
        index = -1
        for action in liste_actions:
            reward = 0
            """ 
            We execute 'action'
            While the hand is not over
                If Chance Node : we compute ONE possibility of card
                Elif Action Node : call / all -in if call is not possible
                Elif Terminal Node :
                    1 - If showdown :
                        A - We compute ONE possibility of hole cards for players who are not 'gameState.target_player'
                        B - We compute the best hand between the players  
                    2 - We compute the 'reward' variable
                        If player who wins is target_player:
                            reward = gameState.pot
                        Elif player who wins is not None:
                            reward = 0 - gameState.pot
                We update the Game State accordingly
            """
            if maxReward is not None:
                if reward < maxReward:
                    break
                elif reward == maxReward:
                    if random.choice([True, False]):
                        break
            maxReward = reward
            index += 1
        probabilities[index][1] += 1
    return compute_probabilities(probabilities)


def get_play(arrayProbas):
    indices = np.arange(len(arrayProbas))
    probabilities = arrayProbas[:, 1].astype(float)
    chosen_index = np.random.choice(indices, p=probabilities)
    return arrayProbas[chosen_index]


def eval(gameState):
    return get_play(cfr(gameState, 1))