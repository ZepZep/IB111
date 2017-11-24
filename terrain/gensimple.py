import numpy as np
import random
from PIL import Image
from tkinter import Entry, Label, OptionMenu,  StringVar


def pairs(l):
    for i in range(len(l)-1):
        yield (l[i], l[i+1])


def minmax(a, x, b):
    if x < a:
        return a
    elif x > b:
        return b
    else:
        return x


def smoothLineQuad(row, setIndexes):
    # vel = random.random()*4 - 2
    vel = 0
    for i1, i2 in pairs(setIndexes):
        h1 = row[i1]
        h2 = row[i2]
        t = i2-i1
        acc = 2*(float(h2) - h1 - vel*t)/(t*t)

        height = float(h1)
        for i in range(i1, i2 + 1):
            vel += acc
            height = height + vel
            row[i] = minmax(0, round(height), 255)

    return row


def smoothLineLin(row, setIndexes):
    for i1, i2 in pairs(setIndexes):
        h1 = row[i1]
        h2 = row[i2]
        slope = 1.0 * (int(h2)-h1) / (i2-i1)

        for mult, i in enumerate(range(i1, i2+1)):
            val = round(h1 + slope*mult)
            row[i] = minmax(0, val, 255)

    return row


lineSmoothers = {
    "linear": smoothLineLin,
    "quadratic": smoothLineQuad
}


class GenSimpleGrid:
    def __init__(self, updateViewCallback, size=(601, 601)):
        self.size = size
        self.seed = 4
        self.updateView = updateViewCallback

        self.heights = np.zeros(size, dtype=np.uint8)
        self.uiroot = None
        self.smoothLine = smoothLineQuad

    def generate(self):
        """generuje mapu"""
        if self.uiroot is not None:
            self.loadValues()
        random.seed(self.seed)
        np.random.seed(self.seed)
        self._genHeights()

    def drawControls(self, root):
        """vykresli kontrolni panel"""
        self.uiroot = root
        seedLabel = Label(root, text="Seed:")
        seedLabel.grid(row=2, column=0)

        self.seedVar = StringVar(value=str(self.seed))
        self.seedEntry = Entry(root, textvariable=self.seedVar)
        self.seedEntry.bind('<Return>', self.updateMap)
        self.seedEntry.grid(row=2, column=1)

        Label(root, text="Interpolate:").grid(row=3, column=0)
        self.interFcnVar = StringVar()
        optionNames = list(lineSmoothers.keys())
        self.interFcnVar.set(optionNames[0])
        option = OptionMenu(root, self.interFcnVar, *optionNames, command=self.updateMap)
        option.grid(row=3, column=1)

    def loadValues(self):
        """nacte hodnoty z kontrolniho panelu"""
        self.seed = int(self.seedVar.get())
        self.smoothLine = lineSmoothers[self.interFcnVar.get()]

    def updateMap(self, val=None):
        """updatuje mapu po zmene nastaveni"""
        self.generate()
        self.updateView()

    def _genHeights(self):
        """generuje pole vysek"""
        sizeX, sizeY = self.size

        gridSize = 100
        sizeFix = (sizeX//gridSize+1, sizeY//gridSize+1)
        bigSize = ((sizeFix[0] - 1) * gridSize + 1, (sizeFix[1] - 1) * gridSize + 1)
        bx, by = bigSize

        fixField = np.random.randint(100, 150, sizeFix, np.uint8)
        heights = np.zeros(bigSize, dtype=np.uint8)

        indexes = [x*gridSize for x in range(sizeFix[0])]
        for y in range(sizeFix[1]):
            for x in range(sizeFix[0]):
                heights[x*gridSize, y*gridSize] = fixField[x, y]
            row = heights[:, y*gridSize]
            self.smoothLine(row, indexes)

        indexes = [y*gridSize for y in range(sizeFix[1])]
        for x in range(bx):
            col = heights[x, :]
            self.smoothLine(col, indexes)

        self.heights = np.copy(heights[:sizeX, :sizeY])

    def getImage(self):
        """vraci posledni vygenerovany obrazek"""
        return Image.frombytes("L", self.size, self.heights.tobytes("F"))


