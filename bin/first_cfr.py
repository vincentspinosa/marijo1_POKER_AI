""" def is_distrib_like_prev(distrib, prevDistrib):
    return

def cfr(gameState, evaluatorStep):
    player_cible = gameState.current_player
    liste_actions = gameState.available_actions()
    probabilities = []
    distribution = []
    gameStateInitial = gameState
    nashEq = False
    while nashEq != True:
        mainIters = 0
        counterNE = 0
        for _ in range(evaluatorStep):
            gameState.deck.shuffle()
            maxReward = None
            index = -1
            for i in liste_actions:
                #algorithme
                index += 1
            probabilities[index][1] += 1
        distrib = compute_distrib()
        mainIters += 1
        if mainIters == 1:
            prevDistrib = distrib
        else:
            if is_distrib_like_prev(distrib, prevDistrib) == True:
                counterNE += 1
                if counterNE > 2:
                    nashEq = True
                else:
                    counterNE = 0 
    index = 0
    for el in distribution:
        probabilities[index][2] = el
        index += 1
    return probabilities """