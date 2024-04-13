import pickle
import random
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

def normalize_regrets(regrets:list, min_regret:float) -> list:
    for data in regrets:
        data[1] += (min_regret * -1)
    return regrets

def turn_regrets_to_values(regrets:list) -> list:
    minR = find_min_regret(regrets)
    if minR < 0:
        regrets = normalize_regrets(regrets, minR)
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
    games = 0.01
    wins = 0.01
    draws = 0.01
    loses = 0.01
    cc_to_deal = 5 - len(gameStateTemp.community_cards)
    # TRAVERSAL OF THE GAME TREE
    for iter in range(iterations):
        games += 1
        sampleList = random.sample(gameStateTemp.ai_deck, cc_to_deal + 2)
        gameStateTemp.community_cards = gameState.community_cards + sampleList[:cc_to_deal]
        gameStateTemp.players[opposite_player_index].hand = sampleList[cc_to_deal:]
        winner = gameStateTemp.showdown(gameStateTemp.players)
        if winner == gameStateTemp.ai_player:
            wins += 1
        elif winner is None:
            draws += 1
        else:
            loses += 1
        # VERBOSE
        if verboseLevel > 2 and iter % verboseIterationsSteps == 0:
            print(f"\nIteration {iter}")
            print(f"Community cards:")
            Card.print_pretty_cards(gameStateTemp.community_cards)
            print(f"Opposite player cards:")
            Card.print_pretty_cards(gameStateTemp.players[opposite_player_index].hand)
    # COMPUTATION OF THE REGRETS
    winsCoefficient = wins / games
    index = -1
    uncertaintyValue = 10
    for action in liste_actions:
        index += 1
        if action[0] == 'fold':
            if wins > 0.01:
                regrets[index][1] += ((potMinusDiff + (maxBetAmount * winsCoefficient)) * wins)
            if draws > 0.01:
                regrets[index][1] += ((potMinusDiff / 2) * draws)
        if action[0] == 'check':
            if wins > 0.01:
                regrets[index][1] += ((potMinusDiff / 2) + ((maxBetAmount / pow2(uncertaintyValue)) * winsCoefficient) * wins)
        if action[0] in ['call', 'raise', 'all-in']:
            if loses > 0.01:
                if action[0] != 'raise':
                    regrets[index][1] += ((min(action[1], maxBetAmount) / winsCoefficient) * loses)
                else:
                    regrets[index][1] += (((min(action[1], maxBetAmount) * (1 + sig(uncertaintyValue))) / winsCoefficient) * loses)
            if wins > 0.01:
                regrets[index][1] -= ((potMinusDiff * winsCoefficient) * wins)
                if action[1] < maxBetAmount:
                    regrets[index][1] += ((((maxBetAmount - action[1]) / pow2(uncertaintyValue)) * winsCoefficient) * wins)
            if draws > 0.01:
                regrets[index][1] -= (((potMinusDiff / 2) * winsCoefficient) * draws)
    # VERBOSE
    if verboseLevel > 0:
        print(f"\nIterations: {iterations}")
    if verboseLevel > 1:
        print("\nRegrets before computing them:")
        for r in regrets:
            print(r)
    # COMPUTATION OF THE RESULTS
    result = compute_regrets_probabilities(regrets)
    # VERBOSE
    if verboseLevel > 1:
        print("\nAction distribution:")
        for action_distribution in result:
            print(action_distribution)
    # RETURN
    return result


def algorithm_EXPERIMENTAL(gameState:GameState, iterations:int, verboseLevel:int=0, verboseIterationsSteps:int=50) -> dict[list, int]:
    """ Create your own algorithm here """
