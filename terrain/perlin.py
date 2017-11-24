import random
from time import time
from math import floor
from numpy import array


def bilin(a, b, c, d):
    return ((a+b) /2 + (c+d)/2)/2


def hashcoord2vector(x, y):
    random.seed(x)
    xp = random.random()
    random.seed(-y)
    yp = random.random()

    return array((xp, yp))


class Perlin2D:
    """Stara trida na generovani perlinova sumu, pouze pro jednotlive hodnoty, asi nefunguje, hodne pomala"""
    def __init__(self, seed=None):
        if seed is None:
            self.seed = floor(time() % 1 * 100000)
        else:
            self.seed = seed
        random.seed(self.seed)

    def noise(self, x, y):
        gridpoints = self.gridPoints(x, y)
        vects = [hashcoord2vector(*p) for p in gridpoints]
        pos = array((x, y))
        deltas = [p - pos for p in gridpoints]
        # print(x, y, deltas)
        grads = [vects[i].dot(deltas[i])/4 for i in range(len(vects))]
        n = bilin(*grads)
        # print(n)
        return n

    def gridPoints(self, x, y):
        l = floor(x)
        t = floor(y)
        return [array((t,   l)),
                array((t,   l+1)),
                array((t+1, l)),
                array((t+1, l+1))]
