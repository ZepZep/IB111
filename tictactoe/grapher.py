from ticTacToe import TicTacToe
from playerRand import PlayerRand
from playerReact import PlayerReact
from playerUnbeat import PlayerUnbeat
import matplotlib.pyplot as plt
import math

playerVariants = [PlayerRand, PlayerReact, PlayerUnbeat]
playerLabels = ["Random", "Reactive", "Unbeatable"]
game = TicTacToe()
numIterations = 1000

plt.close('all')
_, plots = plt.subplots(3, 3)


def getLabels(a, valA,  b, valB):
    return [("P1 " + playerLabels[a] + " wins") if valA > 0 else "",
            "Draw",
            ("P2 " + playerLabels[b] + " wins") if valB > 0 else ""]


def pieFilter(pct):
    return ('%1.1f%%' % pct) if pct > 0 else ""


def printProgress(string, part, whole, indent=50, size=20):
    indent -= int(math.log(part/whole*100, 10))
    out = "\r" + string + " " * (indent - len(string))
    out += "%.0f%%" % (part/whole*100)
    hashNum = int(size * part/whole)
    out += " [" + "#" * hashNum + " " * (size-hashNum) + "]"
    print(out, end="")


for row, first in enumerate(playerVariants):
    for col, second in enumerate(playerVariants):
        p1 = playerVariants[row]
        p2 = playerVariants[col]
        w1 = 0
        draws = 0
        w2 = 0

        outString = "Simulating " + playerLabels[row] + " vs " + playerLabels[col]
        printProgress(outString, 1, numIterations)
        for i in range(numIterations):
            score, turnNum = game.simulate([p1, p2])
            if score[0] == 1:
                w1 += 1
            elif score[1] == 1:
                w2 += 1
            else:
                draws += 1
            if (i+1) % (numIterations/100) == 0:
                printProgress(outString, i+1, numIterations)

        print()
        # stats = [s*100/numIterations for s in [w1, draws, w2]]
        stats = [w1, draws, w2]

        # Plotting
        curPlot = plots[row, col]
        labels = getLabels(row, w1, col, w2)
        curPlot.pie(stats, labels=labels, autopct=pieFilter, shadow=False, startangle=90)
        curPlot.set_title(playerLabels[row] + " vs " + playerLabels[col])
        curPlot.axis('equal')

plt.tight_layout()
plt.show()
