import copy
from player import Player
from gameState import GameState
import plotext as plt
from cfr import cfr

p1 = Player(chips=1000)
p2 = Player(chips=1000)
game_state = GameState((p1, p2), 1, small_blind=10, big_blind=20)

start = 10
iterations = 100
plot = [[], []]
for second in range(start, 0, -1):
    print(f"\n{second} seconds:")
    loss = []
    for iter in range(iterations):
        cfr_result = cfr(copy.deepcopy(game_state), second)
        print(f"\nIteration {iter}")
        if iter == 0:
            for action in cfr_result[0]:
                loss.append([action[0], [action[1], action[1]]])
            for el in loss:
                print(el)
        else:
            for i in range(len(loss)):
                if loss[i][1][0] > cfr_result[0][i][1]:
                    loss[i][1][0] = copy.copy(cfr_result[0][i][1])
                elif loss[i][1][1] < cfr_result[0][i][1]:
                    loss[i][1][1] = copy.copy(cfr_result[0][i][1])
    totalLoss = 0
    for el in loss:
        print(el)
        totalLoss += el[1][1] - el[1][0]
    print(f"\nTotal loss: {totalLoss}".upper())
    plot[0].append(second)
    plot[1].append(totalLoss)
for el in plot[0]:
    print(el)
for el in plot[1]:
    print(el)
plt.bar(plot[0], plot[1])
plt.show()
