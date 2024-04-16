import pickle
import random
import numpy as np
from treys import Card
from .gameState.gameState import GameState

def sig(x):
    return 1 / (1 + np.exp(-x))

def find_max_value(actions:list) -> float:
    maxV = 0
    for ac in actions:
        if ac[1] > maxV:
            maxV = ac[1]
    return maxV

def turn_action_regrets_to_values(actions:list) -> list:
    maxV = find_max_value(actions)
    for ac in actions:
        if ac[1] < 1:
            ac[1] = maxV
        else:
            ac[1] = (maxV / ac[1])
    return actions

def extract_strategy_values(actions:list) -> list:
    maxV = find_max_value(actions)
    for ac in actions:
        if ac[1] < maxV:
            ac[1] *= (ac[1] / maxV)
    return actions

def compute_probabilities(actions:list) -> list:
    sum = 0
    for ac in actions:
        sum += ac[1]
    for ac in actions:
        if ac[1] > 0:
            ac[1] /= sum
    return actions

def compute_regrets_probabilities(actions:list) -> list:
    return compute_probabilities(extract_strategy_values(turn_action_regrets_to_values(actions)))

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
    uncertaintyValue = 8.34
    for action in liste_actions:
        index += 1
        if action[0] == 'fold':
            if wins > 0.01:
                regrets[index][1] += ((potMinusDiff + (maxBetAmount * winsCoefficient)) * wins)
            if draws > 0.01:
                regrets[index][1] += ((potMinusDiff / 2) * draws)
        if action[0] == 'check':
            if wins > 0.01:
                regrets[index][1] += ((potMinusDiff / 2) + ((maxBetAmount / (uncertaintyValue ** 2)) * winsCoefficient) * wins)
        if action[0] in ['call', 'raise', 'all-in']:
            if loses > 0.01:
                if liste_actions[0][0] == 'check' or action[0] != 'raise':
                    regrets[index][1] += ((min(action[1], maxBetAmount) / winsCoefficient) * loses)
                else:
                    regrets[index][1] += (((min(action[1], maxBetAmount) * (1 + sig(uncertaintyValue))) / winsCoefficient) * loses)
            if wins > 0.01:
                if action[1] < maxBetAmount:
                    regrets[index][1] += ((((maxBetAmount - action[1]) / (uncertaintyValue ** 2)) * winsCoefficient) * wins)
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
    """ 
    Create your own algorithm here 
    Or leave the call to the function below
    """
    return algorithm(gameState=gameState, iterations=iterations, verboseLevel=verboseLevel, verboseIterationsSteps=verboseIterationsSteps)
