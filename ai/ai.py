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

def algorithm(gameState:GameState, iterations:int, verboseLevel:int=0, verboseIterationsSteps:int=50) -> dict[list, int]:
    liste_actions = gameState.available_actions()
    regrets = [[el, 0] for el in liste_actions]
    opposite_player_index = (gameState.get_player_position(gameState.ai_player) + 1) % len(gameState.players)
    gameState.ai_deck = gameState.deck.cards + gameState.players[opposite_player_index].hand
    potSave = gameState.current_pot
    oppChipsSave = gameState.players[opposite_player_index].chips
    gameStateInitial = pickle.dumps(gameState)
    gameStateTemp = pickle.loads(gameStateInitial)
    traversals = int(iterations / len(liste_actions)) + 1
    for _ in range(traversals):
        random.shuffle(gameStateTemp.ai_deck)
        gameStateTemp.community_cards += [gameStateTemp.ai_deck.pop() for _ in range(5 - len(gameStateTemp.community_cards))]
        gameStateTemp.players[opposite_player_index].hand = [gameStateTemp.ai_deck.pop() for _ in range(2)]
        """ if gameStateTemp.ai_player.chips < gameStateTemp.players[opposite_player_index].chips:
            bestReward = copy.copy(gameStateTemp.current_pot + gameStateTemp.players[opposite_player_index].chips - (gameStateTemp.players[opposite_player_index].chips - gameStateTemp.ai_player.chips))
        else:
            bestReward = copy.copy(gameStateTemp.current_pot + gameStateTemp.players[opposite_player_index].chips) """
        winner = gameStateTemp.showdown(gameStateTemp.players)
        if verboseLevel > 2:
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
                """ if winner == gameStateTemp.ai_player and action[1] <= oppChipsSave:
                    regrets[index][1] += (bestReward - (action[1] * 2) - potSave """
                if winner == gameStateTemp.players[opposite_player_index]:
                    regrets[index][1] += action[1] if action[1] <= oppChipsSave else oppChipsSave
        gameStateTemp = pickle.loads(gameStateInitial)
    if verboseLevel > 0:
        print(f"\nIterations: {iterations}")
    if verboseLevel > 1:
        print("\nRegrets before computing them:")
        for r in regrets:
            print(r)
    result = compute_regrets_probabilities(regrets)
    if verboseLevel > 1:
        print("\nAction distribution:")
        for action_distribution in result:
            print(action_distribution)
    return result