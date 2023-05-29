import time
import pickle
import random
import copy
from treys import Card
from gameState.gameState import GameState

def find_max_regret(regrets:list) -> int or float:
    maxR = 0
    for data in regrets:
        if data[1] > maxR:
            maxR = data[1]
    return maxR

def turn_regrets_to_value(regrets:list) -> list:
    maxR = find_max_regret(regrets)
    for data in regrets:
        data[1] = maxR / data[1] if data[1] > 0 else maxR
    return regrets

def compute_probabilities(regrets:list) -> list:
    sum = 0
    for rg in regrets:
        sum += rg[1]
    for rg in regrets:
        rg[1] /= sum
    return regrets

def compute_regrets_probabilities(regrets:list) -> list:
    return compute_probabilities(turn_regrets_to_value(regrets))

def algorithm(gameState:GameState, seconds:int or float, verboseLevel:int=0, verboseIterationsSteps:int=50) -> dict[list, int]:
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
                if verboseLevel > 1:
                    if iterations % verboseIterationsSteps == 0:
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
    result = {'probability_distribution': compute_probabilities(probabilities), 'iterations': iterations}
    if verboseLevel > 0:
        for action_distribution in result['probability_distribution']:
            print("\nAction distribution:")
            print(action_distribution)
    return result

def algorithm2(gameState:GameState, seconds:int or float, verboseLevel:int=0, verboseIterationsSteps:int=50) -> dict[list, int]:
    liste_actions = gameState.available_actions()
    regrets = [[el, 0] for el in liste_actions]
    opposite_player_index = (gameState.get_player_position(gameState.ai_player) + 1) % len(gameState.players)
    gameStateInitial = pickle.dumps(gameState)
    gameStateTemp = pickle.loads(gameStateInitial)
    start_time = time.time()
    iterations = 0
    while (time.time() - start_time) < seconds:
        gameStateTemp.ai_deck = gameStateTemp.deck.cards + gameStateTemp.players[opposite_player_index].hand
        random.shuffle(gameStateTemp.ai_deck)
        gameStateTemp.community_cards += [gameStateTemp.ai_deck.pop() for _ in range(5 - len(gameStateTemp.community_cards))]
        gameStateTemp.players[opposite_player_index].hand = [gameStateTemp.ai_deck.pop() for _ in range(2)]
        potSave = copy.copy(gameStateTemp.current_pot)
        aiChipsSave = copy.copy(gameStateTemp.ai_player.chips)
        """ aiChipsSave = copy.copy(gameStateTemp.ai_player.chips)
        if gameStateTemp.ai_player.chips < gameStateTemp.players[opposite_player_index].chips:
            bestReward = copy.copy(gameStateTemp.current_pot + gameStateTemp.players[opposite_player_index].chips - (gameStateTemp.players[opposite_player_index].chips - gameStateTemp.ai_player.chips))
        else:
            bestReward = copy.copy(gameStateTemp.current_pot + gameStateTemp.players[opposite_player_index].chips) """
        winner = gameStateTemp.showdown(gameStateTemp.players)
        if verboseLevel > 1:
            if iterations % verboseIterationsSteps == 0:
                print(f"\nIteration {iterations}")
                print(f"Community cards:")
                Card.print_pretty_cards(gameStateTemp.community_cards)
                print(f"Opposite player cards:")
                Card.print_pretty_cards(gameStateTemp.players[opposite_player_index].hand)
        index = -1
        for action in liste_actions:
            index += 1
            if action[0] == 'fold':
                if winner == gameStateTemp.ai_player:
                    #regrets[index][1] += bestReward
                    regrets[index][1] += potSave
                elif winner == None:
                    regrets[index][1] += (potSave / 2)
            if action[0] == 'check':
                if winner == gameStateTemp.ai_player:
                    #regrets[index][1] += bestReward
                    regrets[index][1] += (potSave / 2)
            elif action[0] in ['call', 'raise', 'all-in']:
                """ if winner == gameStateTemp.ai_player:
                    regrets[index][1] += (bestReward - (action[1] * 2) - potSave) """
                if winner == gameStateTemp.players[opposite_player_index]:
                    regrets[index][1] += action[1] if action[1] <= aiChipsSave else aiChipsSave
            iterations += 1
        gameStateTemp = pickle.loads(gameStateInitial)
    if verboseLevel > 0:
        print("\nRegrets before computing them:")
        for r in regrets:
            print(r)
    result = {'probability_distribution': compute_regrets_probabilities(regrets), 'iterations': iterations}
    if verboseLevel > 0:
        print("\nAction distribution:")
        for action_distribution in result['probability_distribution']:
            print(action_distribution)
    return result