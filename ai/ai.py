import pickle
import random
import copy
import numpy as np
from treys import Card
from .gameState.gameState import GameState

def pow2(x):
    return x ** 2

def sig(x):
    return 1 / (1 + np.exp(-x))

def find_min_regret(regrets:list) -> float:
    minR = None
    for data in regrets:
        if minR is None:
            minR = data[1]
        elif data[1] < minR:
            minR = data[1]
    return minR

def find_max_regret(regrets:list) -> float:
    maxR = 0
    for data in regrets:
        if data[1] > maxR:
            maxR = data[1]
    return maxR

def turn_regrets_to_values(regrets:list) -> list:
    maxR = find_max_regret(regrets)
    for data in regrets:
        if data[1] < 1:
            data[1] = maxR
        else:
            data[1] = (maxR / data[1])
    return regrets

def compute_probabilities(values:list) -> list:
    sum = 0
    for vl in values:
        sum += vl[1]
    for vl in values:
        if vl[1] > 0:
            vl[1] /= sum
    return values

def compute_regrets_probabilities(regrets:list) -> list:
    return compute_probabilities(turn_regrets_to_values(regrets))

def algorithm(gameState:GameState, iterations:int, verboseLevel:int=0, verboseIterationsSteps:int=50) -> dict[list, int]:
    # SETTING-UP EVERYTHING
    liste_actions = gameState.available_actions()
    prediction_round = copy.copy(gameState.current_stage)
    # missingParametersWeight is :
    #   1 for each hole card of the opposing player
    #   1 for each community card to compute
    """ missingParametersWeight = 2
    if prediction_round == 'pre-flop':
        missingParametersWeight += 5
    elif prediction_round == 'flop':
        missingParametersWeight += 2
    elif prediction_round == 'turn':
        missingParametersWeight += 1 """
    #TEST VALUE
    missingParametersWeight = 10
    regrets = [[el, 0] for el in liste_actions]
    aiIndex = gameState.get_player_position(gameState.ai_player)
    opposite_player_index = (aiIndex + 1) % len(gameState.players)
    gameState.ai_deck = gameState.deck.cards + gameState.players[opposite_player_index].hand
    potSave = gameState.current_pot
    oppChipsSave = gameState.players[opposite_player_index].chips
    aiChipsSave = gameState.ai_player.chips
    oppCB = gameState.current_bets[gameState.players[opposite_player_index]]
    aiCB = gameState.current_bets[gameState.ai_player]
    maxBetAmount = 0
    if aiChipsSave + aiCB >= oppChipsSave + oppCB:
        maxBetAmount += oppChipsSave + oppCB - aiCB
    else:
        maxBetAmount += aiChipsSave
    aiMaxChipsInGame = maxBetAmount + aiCB
    diff = oppCB - aiMaxChipsInGame if aiMaxChipsInGame < oppCB else 0
    potMinusDiff = potSave - diff
    gameStateInitial = pickle.dumps(gameState)
    gameStateTemp = pickle.loads(gameStateInitial)
    traversals = int(iterations / len(liste_actions)) + 1
    games = 0.01
    wins = 0.01
    draws = 0.01
    loses = 0.01
    cc_to_deal = 5 - len(gameStateTemp.community_cards)
    # PRE-TRAVERSAL
    for _ in range(iterations):
        games += 1
        sampleList = random.sample(gameStateTemp.ai_deck, cc_to_deal + 2)
        gameStateTemp.community_cards = gameState.community_cards + sampleList[:cc_to_deal]
        #gameStateTemp.community_cards += [gameStateTemp.ai_deck.pop() for _ in range(5 - len(gameStateTemp.community_cards))]
        gameStateTemp.players[opposite_player_index].hand = sampleList[cc_to_deal:]
        #gameStateTemp.players[opposite_player_index].hand = [gameStateTemp.ai_deck.pop() for _ in range(2)]
        #del gameStateTemp.ai_deck[:cc_to_deal + 2]
        winner = gameStateTemp.showdown(gameStateTemp.players)
        if winner == gameStateTemp.ai_player:
            wins += 1
        elif winner is None:
            draws += 1
        else:
            loses += 1
        #gameStateTemp = pickle.loads(gameStateInitial)
    # START TRY IN ONE TREATMENT
    index = -1
    winsCoefficient = wins / games
    for action in liste_actions:
        index += 1
        if action[0] == 'fold':
            if wins > 0.01:
                regrets[index][1] += ((potMinusDiff + (maxBetAmount * winsCoefficient)) * wins)
            if draws > 0.01:
                regrets[index][1] += ((potMinusDiff / 2) * draws)
        if action[0] == 'check' and wins > 0.01:
            regrets[index][1] += ((potMinusDiff / 2) + ((maxBetAmount / pow2(missingParametersWeight)) * winsCoefficient) * wins)
        if action[0] in ['call', 'raise', 'all-in']:
            if loses > 0.01:
                if action[0] != 'raise':
                    regrets[index][1] += ((min(action[1], maxBetAmount) / winsCoefficient) * loses)
                else:
                    regrets[index][1] += (((min(action[1], maxBetAmount) * (1 + sig(missingParametersWeight))) / winsCoefficient) * loses)
            if wins > 0.01:
                regrets[index][1] -= ((potMinusDiff * winsCoefficient) * wins)
                if action[1] < maxBetAmount:
                    regrets[index][1] += ((((maxBetAmount - action[1]) / pow2(missingParametersWeight)) * winsCoefficient) * wins)
            if draws > 0.01:
                regrets[index][1] -= (((potMinusDiff / 2) * winsCoefficient) * draws)
    # END TRY IN ONE TREATMENT
    """ # TRAVERSAL OF THE GAME TREE
    for _ in range(traversals):
        games += 1
        random.shuffle(gameStateTemp.ai_deck)
        gameStateTemp.community_cards += [gameStateTemp.ai_deck.pop() for _ in range(5 - len(gameStateTemp.community_cards))]
        gameStateTemp.players[opposite_player_index].hand = [gameStateTemp.ai_deck.pop() for _ in range(2)]
        winner = gameStateTemp.showdown(gameStateTemp.players)
        if winner == gameStateTemp.ai_player:
            wins += 1
        winsCoefficient = wins / games
        if verboseLevel > 2 and iterations % verboseIterationsSteps == 0:
            print(f"\nIteration {iterations}")
            print(f"Community cards:")
            Card.print_pretty_cards(gameStateTemp.community_cards)
            print(f"Opposite player cards:")
            Card.print_pretty_cards(gameStateTemp.players[opposite_player_index].hand)
        # REGRETS COMPUTATION
        index = -1
        for action in liste_actions:
            index += 1
            if action[0] == 'fold':
                if winner == gameStateTemp.ai_player:
                    regrets[index][1] += potMinusDiff + (maxBetAmount * winsCoefficient)
                elif winner is None:
                    regrets[index][1] += (potMinusDiff / 2)
            elif action[0] == 'check' and winner == gameStateTemp.ai_player:
                regrets[index][1] += (potMinusDiff / 2) + ((maxBetAmount / pow2(missingParametersWeight)) * winsCoefficient)
            elif action[0] in ['call', 'raise', 'all-in']:
                if winner == gameStateTemp.players[opposite_player_index]:
                    if action[0] != 'raise':
                        regrets[index][1] += (min(action[1], maxBetAmount) / winsCoefficient)
                    else:
                        regrets[index][1] += ((min(action[1], maxBetAmount) * (1 + sig(missingParametersWeight))) / winsCoefficient)
                if winner == gameStateTemp.ai_player:
                    regrets[index][1] -= (potMinusDiff * winsCoefficient)
                if winner is None:
                    regrets[index][1] -= ((potMinusDiff / 2) * winsCoefficient)
                if winner == gameStateTemp.ai_player and action[1] < maxBetAmount:
                    regrets[index][1] += (((maxBetAmount - action[1]) / pow2(missingParametersWeight)) * winsCoefficient)
        gameStateTemp = pickle.loads(gameStateInitial)
    if verboseLevel > 0:
        print(f"\nIterations: {iterations}")
    if verboseLevel > 1:
        print("\nRegrets before computing them:")
        for r in regrets:
            print(r) """
    # COMPUTATION OF THE RESULTS
    result = compute_regrets_probabilities(regrets)
    if verboseLevel > 1:
        print("\nAction distribution:")
        for action_distribution in result:
            print(action_distribution)
    return result
