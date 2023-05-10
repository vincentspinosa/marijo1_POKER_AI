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
    """ arrayInput = np.array(arrayInput)
    integers = arrayInput[:, 1].astype(int)
    total = np.sum(integers)
    arrayProbas = integers / total
    result = []
    for index, proba in enumerate(arrayProbas):
        result.append([arrayInput[index, 0], proba])
    return np.array(result) """


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
            print('iterating')
            opposite_player_index = (gameStateTemp.get_player_position(gameStateTemp.target_player) + 1) % len(gameStateTemp.players)
            print(f"Opposite player index: {opposite_player_index}")
            reward = 0
            gameStateTemp.handle_action(action[0], raise_amount=action[1])
            if action[0] == 'fold':
                reward = 0 - gameStateTemp.current_pot
            else:
                if not gameStateTemp.is_round_over():
                    gameStateTemp.next_player()
                    actions = gameStateTemp.available_actions()
                    print(f"Pot before action: {gameStateTemp.current_pot}")
                    if any('check' == action[0] for action in actions):
                        print("ADVERSARY CHECKS")
                        gameStateTemp.handle_action('check', raise_amount=0)
                    elif any('call' == action[0] for action in actions):
                        print("ADVERSARY CALLS")
                        gameStateTemp.handle_action('call', raise_amount=0)
                    else:
                        print("ADVERSARY GOES ALL-IN")
                        gameStateTemp.handle_action('all-in', raise_amount=gameStateTemp.current_player.chips)
                    print(f"Pot after action: {gameStateTemp.current_pot}")
                print(f"Len community cards BEFORE GOING TO SHOWDOWN: {len(gameStateTemp.community_cards)}")
                print(f"GOING TO SHOWDOWN!")
                print(gameStateTemp.community_cards)
                gameStateTemp.go_to_showdown()
                print(f"Len community cards AFTER GOING TO SHOWDOWN: {len(gameStateTemp.community_cards)}")
                gameStateTemp.players[opposite_player_index].hand = [gameStateTemp.deck.deal() for _ in range(2)]
                print(f"Len community cards after distributing hole_cards to the other player: {len(gameStateTemp.community_cards)}")
                print(f"Len deck: {len(gameStateTemp.deck.cards)}")
                winner = gameStateTemp.showdown(gameStateTemp.players)
                if winner == gameStateTemp.target_player:
                    print("Winner is the target player!")
                    reward = gameStateTemp.current_pot
                    print(reward)
                elif winner == gameStateTemp.players[opposite_player_index]:
                    print("Winner is NOT the target player!")
                    reward == 0 - gameStateTemp.current_pot
                    print(reward)
            gameStateTemp = copy.deepcopy(gameStateInitial)
            gameStateTemp.deck.shuffle()
            if maxReward is not None:
                if reward < maxReward:
                    break
                elif reward == maxReward:
                    if random.choice([True, False]):
                        break
            print(f"REWARD: {reward}")
            maxReward = reward
            index += 1
            iterations += 1
        print(f"\n\nINDEX: {index}")
        print(f"MAX REWARD: {maxReward}")
        print(f"ACTION: {str(probabilities[index][0]).upper()}")
        probabilities[index][1] += 1
    print(f"NUMBER OF ITERATIONS: {iterations}")
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