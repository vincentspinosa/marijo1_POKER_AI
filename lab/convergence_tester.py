# iterations is as of now specified as a hard number in algorithm, change it to make this script work
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import copy
import plotext as plt

from ui import UI
from ai import ai
from ai.rules.player import Player

min_iterations = 1000
max_iterations = 10000
iterations_step = 1000
algorithm_runs = 100
stopAtStratFound = False
# stratFoundCeiling is on a scale of 0 to 1
stratFoundCeiling = 0.1
plot = [[], []]

p1 = Player(chips=1000)
p2 = Player(chips=1000)
game_state = UI(ai_iterations=max_iterations, players=(p1, p2), ai_player_index=0, ai_verbose=0, dealer_position=1, small_blind=10, big_blind=20)
game_state.deal_hole_cards()
game_state.collect_blinds()

for iterations in range(min_iterations, max_iterations, iterations_step):
    print(f"\n{iterations} iterations:")
    #spreadTable will store, for each action, its lowest and highest probability distribution
    spreadTable = []
    for run in range(algorithm_runs):
        algorithm_result = ai.algorithm(copy.deepcopy(game_state), iterations=iterations, verboseLevel=game_state.ai_verbose)
        print(f"\nRun n°{run}")
        print(f"Number of iterations inside the run: {iterations}")
        if run == 0:
            for action in algorithm_result:
                spreadTable.append([action[0], [action[1], action[1]]])
        else:
            #for each possible action:
            for i in range(len(spreadTable)):
                # if the lowest probability distribution is higher that the one in algorithm_result, we replace it
                if spreadTable[i][1][0] > algorithm_result[i][1]:
                    spreadTable[i][1][0] = copy.copy(algorithm_result[i][1])
                # if the highest probability distribution is lower that the one in algorithm_result, we replace it
                elif spreadTable[i][1][1] < algorithm_result[i][1]:
                    spreadTable[i][1][1] = copy.copy(algorithm_result[i][1])
        for data in spreadTable:
            print(data)
    totalSpread = 0
    for data in spreadTable:
        #totalSpread += highest probability distribution for the action - lowest probability distribution for the action
        totalSpread += data[1][1] - data[1][0]
    print(f"\nTotal spread: {totalSpread}".upper())
    plot[0].append(iterations)
    plot[1].append(totalSpread)
    if stopAtStratFound == True:
        if totalSpread < stratFoundCeiling:
            break

plt.bar(plot[0], plot[1])
plt.show()
