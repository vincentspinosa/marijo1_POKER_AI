import copy
import plotext as plt
from rules import player
from gameState import gameState
from ai import ai

p1 = player.Player(chips=1000)
p2 = player.Player(chips=1000)
game_state = gameState.GameState((p1, p2), 1, small_blind=10, big_blind=20)

max_seconds = 10
cfr_runs = 100
strategyFound = False
plot = [[], []]
for second in range(1, max_seconds):
    print(f"\n{second} seconds:")
    spreadTable = []
    for run in range(cfr_runs):
        cfr_result = ai.cfr(copy.deepcopy(game_state), second)
        print(f"\nRun n°{run}")
        print(f"Number of iterations inside the run: {cfr_result[1]}")
        if run == 0:
            for action in cfr_result[0]:
                spreadTable.append([action[0], [action[1], action[1]]])
        else:
            for i in range(len(spreadTable)):
                if spreadTable[i][1][0] > cfr_result[0][i][1]:
                    spreadTable[i][1][0] = copy.copy(cfr_result[0][i][1])
                elif spreadTable[i][1][1] < cfr_result[0][i][1]:
                    spreadTable[i][1][1] = copy.copy(cfr_result[0][i][1])
        for data in spreadTable:
            print(data)
    totalSpread = 0
    for data in spreadTable:
        totalSpread += data[1][1] - data[1][0]
    print(f"\nTotal spread: {totalSpread}".upper())
    plot[0].append(second)
    plot[1].append(totalSpread)
    if totalSpread < 0.1:
        strategyFound = True
        break
plt.bar(plot[0], plot[1])
plt.show()
