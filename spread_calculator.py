import copy
import plotext as plt
from rules.player import Player
from gameState.gameState import GameState
from ai import ai

p1 = Player(chips=1000)
p2 = Player(chips=1000)
game_state = GameState((p1, p2), 1, small_blind=10, big_blind=20)

max_seconds = 3
# using 5 as a secondDivisor will create steps of 0.2 seconds
secondDivisor = 5
algorithm_runs = 100
strategyFound = False
plot = [[], []]
for i in range(1, max_seconds * secondDivisor):
    seconds = i / secondDivisor
    print(f"\n{seconds} seconds:")
    #spreadTable will store, for each action, its lowest and highest probability distribution
    spreadTable = []
    for run in range(algorithm_runs):
        algorithm_result = ai.algorithm(copy.deepcopy(game_state), seconds)
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
        break
plt.bar(plot[0], plot[1])
plt.show()
