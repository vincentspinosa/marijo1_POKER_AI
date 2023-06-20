import pickle
import random
from treys import Card
from gameState.gameState import GameState

def find_max_regret(regrets:list) -> int or float:
    maxR = 0
    for data in regrets:
        if data[1] > maxR:
            maxR = data[1]
    return maxR

def turn_regrets_to_values(regrets:list) -> list:
    maxR = find_max_regret(regrets)
    for data in regrets:
        data[1] = maxR / data[1] if data[1] >= 1 else maxR
    return regrets

def clean_values(values:list, floor:float) -> list:
    sum = 0
    for vl in values:
        sum += vl[1]
    for vl in values:
        vl[1] -= (sum * floor)
    for vl in values:
        vl[1] = 0 if vl[1] < 0 else vl[1]
    return values

def compute_probabilities(values:list) -> list:
    sum = 0
    for vl in values:
        sum += vl[1]
    for vl in values:
        if vl[1] > 0:
            vl[1] /= sum
    return values

def compute_regrets_probabilities(regrets:list, floor: float) -> list:
    return compute_probabilities(clean_values(values=turn_regrets_to_values(regrets), floor=floor))

def algorithm(gameState:GameState, iterations:int, verboseLevel:int=0, verboseIterationsSteps:int=50) -> dict[list, int]:
    # SETTING-UP EVERYTHING
    liste_actions = gameState.available_actions()
    floorAlgo = 0.07
    isPreflopFoldMultiplier = 3 if gameState.current_stage == 'pre-flop' else 1
    coeffL1 = 1000
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
    diff = oppCB - maxBetAmount if maxBetAmount < oppCB else 0
    potMinusDiff = potSave - diff
    gameStateInitial = pickle.dumps(gameState)
    gameStateTemp = pickle.loads(gameStateInitial)
    traversals = int(iterations / len(liste_actions)) + 1
    # TRAVERSAL OF THE GAME TREE
    for _ in range(traversals):
        random.shuffle(gameStateTemp.ai_deck)
        gameStateTemp.community_cards += [gameStateTemp.ai_deck.pop() for _ in range(5 - len(gameStateTemp.community_cards))]
        gameStateTemp.players[opposite_player_index].hand = [gameStateTemp.ai_deck.pop() for _ in range(2)]
        winner = gameStateTemp.showdown(gameStateTemp.players)
        if verboseLevel > 2 and iterations % verboseIterationsSteps == 0:
            print(f"\nIteration {iterations}")
            print(f"Community cards:")
            Card.print_pretty_cards(gameStateTemp.community_cards)
            print(f"Opposite player cards:")
            Card.print_pretty_cards(gameStateTemp.players[opposite_player_index].hand)
        index = -1
        for action in liste_actions:
            index += 1
            # LAYER 1 - DEFENSIVE
            # In this Layer, the goal is to not loose money
            if action[0] == 'fold':
                if winner == gameStateTemp.ai_player:
                    regrets[index][1] += ((potMinusDiff * coeffL1) * isPreflopFoldMultiplier)
                elif winner == None:
                    regrets[index][1] += (((potMinusDiff / 2) * coeffL1) * isPreflopFoldMultiplier)
            elif action[0] == 'check' and winner == gameStateTemp.ai_player:
                regrets[index][1] += ((potMinusDiff / 2) * coeffL1)
            elif action[0] in ['call', 'raise', 'all-in'] and winner == gameStateTemp.players[opposite_player_index]:
                regrets[index][1] += (min(action[1], maxBetAmount) * coeffL1)
            # LAYER 2 - OFFENSIVE
            # In this Layer, the goal is to win the max amount of money
            if action[0] == 'fold':
                if winner == gameStateTemp.ai_player:
                    regrets[index][1] += ((potMinusDiff + maxBetAmount) * isPreflopFoldMultiplier)
                elif winner == None:
                    regrets[index][1] += ((potMinusDiff / 2) * isPreflopFoldMultiplier)
            elif action[0] == 'check' and winner == gameStateTemp.ai_player:
                regrets[index][1] += (potMinusDiff / 2)
            elif action[0] in ['call', 'raise', 'all-in']:
                if winner == gameStateTemp.players[opposite_player_index]:
                    regrets[index][1] += min(action[1], maxBetAmount)
                elif winner == gameStateTemp.ai_player and action[1] < maxBetAmount:
                    regrets[index][1] += (maxBetAmount - action[1])
        gameStateTemp = pickle.loads(gameStateInitial)
    if verboseLevel > 0:
        print(f"\nIterations: {iterations}")
    if verboseLevel > 1:
        print("\nRegrets before computing them:")
        for r in regrets:
            print(r)
    # COMPUTATION OF THE RESULTS
    result = compute_regrets_probabilities(regrets=regrets, floor=floorAlgo)
    if verboseLevel > 1:
        print("\nAction distribution:")
        for action_distribution in result:
            print(action_distribution)
    return result
