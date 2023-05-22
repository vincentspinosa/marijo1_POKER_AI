import time
import pickle

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
    gameStateInitial = pickle.dumps(gameState)
    start_time = time.time()
    iterations = 0
    time_for_copying = 0
    while (time.time() - start_time) < seconds:
        t_cpy = time.time()
        gameStateTemp = pickle.loads(gameStateInitial)
        t_cpy = time.time() - t_cpy
        time_for_copying += t_cpy
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
                if winner == gameStateTemp.target_player:
                    reward += sumAction
                elif winner == gameStateTemp.players[opposite_player_index]:
                    reward -= sumAction
            if maxReward is not None and reward < maxReward:
                break
            maxReward = reward
            index += 1
            iterations += 1
        probabilities[index][1] += 1
    print(f"Time for copying: {time_for_copying}")
    return [compute_probabilities(probabilities), iterations]
