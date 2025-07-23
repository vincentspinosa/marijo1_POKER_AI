import pickle
import random
import numpy as np
import math
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
            ac[1] *= (ac[1] / (maxV * maxV))
    return actions

def compute_distribution(actions:list) -> list:
    sum = 0
    for ac in actions:
        sum += ac[1]
    for ac in actions:
        if ac[1] > 0:
            ac[1] /= sum
    return actions

def compute_actions_distribution(actions:list) -> list:
    return compute_distribution(extract_strategy_values(turn_action_regrets_to_values(actions)))

def algorithm(gameState:GameState, iterations:int, verboseLevel:int=0, verboseIterationsSteps:int=50) -> dict[list, int]:
    # SETTING-UP EVERYTHING
    liste_actions = gameState.available_actions()
    regrets = [[el, 0] for el in liste_actions]
    aiIndex = gameState.get_player_position(gameState.ai_player)
    opposite_player_index = (aiIndex + 1) % len(gameState.players)
    """ The ai_deck property is scary, but it is fine:
        - We receive, in the GameSate, all the cards from the Game.
        - We then combine the deck received and the cards of the opposite player, to create
          the Deck from which the AI will draw the cards to traverse the game tree.
        - At absolutely no moment does the AI know the cards of the opposite player.
    """
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
    games = 0.0000001
    wins = 0.0000001
    draws = 0.0000001
    loses = 0.0000001
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
        if verboseLevel > 3 and iter % verboseIterationsSteps == 0:
            print(f"\nIteration {iter}")
            print(f"Community cards:")
            Card.print_pretty_cards(gameStateTemp.community_cards)
            print(f"Opposite player cards:")
            Card.print_pretty_cards(gameStateTemp.players[opposite_player_index].hand)
    # COMPUTATION OF THE REGRETS
    c = wins / games
    index = -1
    for action in liste_actions:
        index += 1
        if action[0] == 'fold':
            regrets[index][1] = ((potMinusDiff + (maxBetAmount * c)) * wins) + ((potMinusDiff / 2) * draws)
        if action[0] == 'check':
            regrets[index][1] = ((potMinusDiff / 2) + ((maxBetAmount / math.e) * c)) * wins
        if action[0] in ['call', 'bet/raise', 'all-in']:
            if liste_actions[0][0] == 'check' or action[0] != 'bet/raise':
                regrets[index][1] = (min(action[1], maxBetAmount) / c) * loses
            else:
                regrets[index][1] = ((min(action[1], maxBetAmount) * (1 + sig(math.e))) / c) * loses
            if action[1] < maxBetAmount:
                regrets[index][1] += (((maxBetAmount - action[1]) / math.e) * c) * wins
    # VERBOSE
    if verboseLevel > 1:
        print(f"\nIterations: {iterations}")
    if verboseLevel > 2:
        print("\nRegrets before computing them:")
        for r in regrets:
            print(r)
    # COMPUTATION OF THE RESULTS
    result = compute_actions_distribution(regrets)
    # VERBOSE
    if verboseLevel > 0:
        print("\nAction distribution:")
        for action_distribution in result:
            print(action_distribution)
    # RETURN
    return result

def get_play(probability_distribution: list[tuple]) -> tuple:
    probability_distribution = np.array(probability_distribution, dtype=list)
    indices = np.arange(len(probability_distribution))
    probabilities = probability_distribution[:, 1].astype(float)
    chosen_index = np.random.choice(indices, p=probabilities)
    return probability_distribution[chosen_index]
