import copy
import plotext as plt
from rules.player import Player
from ui.ui import UI
from ai import ai

p1 = Player(chips=1000)
p2 = Player(chips=1000)
game_state = UI(ai_thinking_time=None, players=(p1, p2), ai_player_index=0, ai_verbose=0, dealer_position=1, small_blind=10, big_blind=20)
game_state.deal_hole_cards()
game_state.collect_blinds()

max_seconds = 50
max_iterations = 15501
# using 1 as a secondDivisor will create steps of 1 second
# using 5 as a secondDivisor will create steps of 0.2 second
secondDivisor = 1
algorithm_runs = 100
strategyFound = False
plot = [[], []]
""" for i in range(1, max_seconds * secondDivisor):
    seconds = i / secondDivisor
    print(f"\n{seconds} seconds:")
    #spreadTable will store, for each action, its lowest and highest probability distribution
    spreadTable = []
    for run in range(algorithm_runs):
        algorithm_result = ai.algorithm(copy.deepcopy(game_state), seconds=seconds, verboseLevel=game_state.ai_verbose)
        print(f"\nRun n°{run}")
        print(f"Number of iterations inside the run: {algorithm_result['iterations']}")
        if run == 0:
            for action in algorithm_result['probability_distribution']:
                spreadTable.append([action[0], [action[1], action[1]]])
        else:
            #for each possible action:
            for i in range(len(spreadTable)):
                # if the lowest probability distribution is higher that the one in algorithm_result, we replace it
                if spreadTable[i][1][0] > algorithm_result['probability_distribution'][i][1]:
                    spreadTable[i][1][0] = copy.copy(algorithm_result['probability_distribution'][i][1])
                # if the highest probability distribution is lower that the one in algorithm_result, we replace it
                elif spreadTable[i][1][1] < algorithm_result['probability_distribution'][i][1]:
                    spreadTable[i][1][1] = copy.copy(algorithm_result['probability_distribution'][i][1])
        for data in spreadTable:
            print(data)
    totalSpread = 0
    for data in spreadTable:
        #totalSpread += highest probability distribution for the action - lowest probability distribution for the action
        totalSpread += data[1][1] - data[1][0]
    print(f"\nTotal spread: {totalSpread}".upper())
    plot[0].append(seconds)
    plot[1].append(totalSpread)
    if totalSpread < 0.1:
        strategyFound = True
        break """
for iterations in range(500, max_iterations, 1000):
    print(f"\n{iterations} iterations:")
    #spreadTable will store, for each action, its lowest and highest probability distribution
    spreadTable = []
    for run in range(algorithm_runs):
        algorithm_result = ai.algorithm(copy.deepcopy(game_state), maxIterations=iterations, seconds=1, verboseLevel=game_state.ai_verbose)
        print(f"\nRun n°{run}")
        print(f"Number of iterations inside the run: {algorithm_result['iterations']}")
        if run == 0:
            for action in algorithm_result['probability_distribution']:
                spreadTable.append([action[0], [action[1], action[1]]])
        else:
            #for each possible action:
            for i in range(len(spreadTable)):
                # if the lowest probability distribution is higher that the one in algorithm_result, we replace it
                if spreadTable[i][1][0] > algorithm_result['probability_distribution'][i][1]:
                    spreadTable[i][1][0] = copy.copy(algorithm_result['probability_distribution'][i][1])
                # if the highest probability distribution is lower that the one in algorithm_result, we replace it
                elif spreadTable[i][1][1] < algorithm_result['probability_distribution'][i][1]:
                    spreadTable[i][1][1] = copy.copy(algorithm_result['probability_distribution'][i][1])
        for data in spreadTable:
            print(data)
    totalSpread = 0
    for data in spreadTable:
        #totalSpread += highest probability distribution for the action - lowest probability distribution for the action
        totalSpread += data[1][1] - data[1][0]
    print(f"\nTotal spread: {totalSpread}".upper())
    plot[0].append(iterations)
    plot[1].append(totalSpread)
    """ if totalSpread < 0.1:
        strategyFound = True
        break """
plt.bar(plot[0], plot[1])
plt.show()
