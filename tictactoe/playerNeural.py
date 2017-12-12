from playField import Pos
import numpy as np
import time
import math


class PlayerNeural:
    def __init__(self):
        self.structure = [10, 10, 9]
        self.thetas = []

    def nextMove(self, id, playField):
        a = []
        a.append(np.ones((self.structure[1], 1)))
        index = 1
        for line in playField:
            for cell in line:
                if cell == 2:
                    cell = -1
                a[0][index, 0] = cell
                index += 1
        index = 0

        for theta in self.thetas:
            # print(theta.shape, " * ", a[index].shape)
            nextA = sigmoid(np.matmul(theta, a[index]))
            # print("   => ", nextA.shape)
            if index < len(self.structure) - 2:
                nextA[0, 0] = 1
            a.append(nextA)
            index += 1

        outIndex = int(np.argmax(a[-1]))
        output = Pos(outIndex % 3, outIndex // 3)
        print(output)
        return output

    def setStrategy(self, strategy):
        self.thetas = []
        start = 0
        for i in range(len(self.structure)-1):
            size = (self.structure[i], self.structure[i+1])
            curLen = size[0] * size[1]
            self.thetas.append(strategy[start:curLen].reshape(size).T)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))
