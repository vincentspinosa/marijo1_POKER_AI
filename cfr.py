import time
import numpy as np
import random
import copy

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
    liste_actions = gameState.available_actions()
    probabilities = [[el, 0] for el in liste_actions]
    gameStateInitial = copy.deepcopy(gameState)
    gameStateTemp = copy.deepcopy(gameState)
    start_time = time.time()
    while (time.time() - start_time) < seconds:
        maxReward = None
        index = -1
        for action in liste_actions:
            print('iterating')
            opposite_player_index = (gameStateTemp.get_player_position(gameStateTemp.target_player) + 1) % len(gameStateTemp.players)
            reward = 0
            gameStateTemp.handle_action(action[0], raise_amount=action[1])
            if action[0] == 'fold':
                reward = 0 - gameStateTemp.current_pot
            else:
                gameStateTemp.next_player()
                actions = gameStateTemp.available_actions()
                try:
                    if actions[0][0] == 'call':
                        gameStateTemp.handle_action(action[0], raise_amount=action[1])
                    else:
                        gameStateTemp.handle_action('all-in', raise_amount=gameStateTemp.current_player.chips)
                except:
                    print(action)
                gameStateTemp.go_to_showdown()
                print(len(gameStateTemp.community_cards))
                print(len(gameStateTemp.deck.cards))
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
        probabilities[index][1] += 1
    return compute_probabilities(probabilities)


def get_play(arrayProbas):
    indices = np.arange(len(arrayProbas))
    probabilities = arrayProbas[:, 1].astype(float)
    chosen_index = np.random.choice(indices, p=probabilities)
    return arrayProbas[chosen_index]


def eval(gameState):
    return get_play(cfr(gameState, 1))