from tkinter import *
from fracanvas import FraCanvas
from fractals import Triangle
from fractals import fractalTypes


class FractalSim(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.level = 0
        self.fractalIndex = 0
        self.createWidgets()
        self.initFractalTypes()

    def createWidgets(self):
        self.master.title("Fractals")

        self.canvas = FraCanvas(self, Triangle, width=700, height=700)
        self.canvas.pack(fill=BOTH, expand=True)

        # Fractal control
        layFractals = Frame()
        pbPrevF = Button(layFractals, text="<")
        pbPrevF.pack(side=LEFT, padx=5)
        pbPrevF["command"] = self.prevFractal
        lFracName = Label(layFractals, text="0", font=("mono", 16))
        lFracName.pack(side=LEFT, padx=5)
        pbNextF = Button(layFractals, text=">")
        pbNextF.pack(side=LEFT, padx=5)
        pbNextF["command"] = self.nextFractal
        layFractals.pack()

        # Level control
        layButtons = Frame()
        pbLess = Button(layButtons, text="<")
        pbLess.pack(side=LEFT, padx=5)
        pbLess["command"] = self.prevLevel
        lLevel = Label(layButtons, text="0", font=("mono", 16))
        lLevel.pack(side=LEFT, padx=5)
        pbMore = Button(layButtons, text=">")
        pbMore.pack(side=LEFT, padx=5)
        pbMore["command"] = self.nextLevel

        # SVG control
        pbSvg = Button(layButtons, text="SVG")
        pbSvg.pack(side=RIGHT, padx=15)
        pbSvg["command"] = self.canvas.saveSvg
        layButtons.pack()

        self.lLevel = lLevel
        self.lFracName = lFracName

    def initFractalTypes(self):
        name, fractal = fractalTypes[0]
        self.canvas.setFractal(fractal)
        self.lFracName["text"] = name

    def nextFractal(self):
        self.fractalIndex += 1
        if self.fractalIndex >= len(fractalTypes):
            self.fractalIndex = len(fractalTypes) - 1
        else:
            name, fractal = fractalTypes[self.fractalIndex]
            self.canvas.setFractal(fractal)
            self.lFracName["text"] = name
            self.level = 0
            self.lLevel["text"] = str(self.level)

    def prevFractal(self):
        self.fractalIndex -= 1
        if self.fractalIndex < 0:
            self.fractalIndex = 0
        else:
            name, fractal = fractalTypes[self.fractalIndex]
            self.canvas.setFractal(fractal)
            self.lFracName["text"] = name
            self.level = 0
            self.lLevel["text"] = str(self.level)

    def nextLevel(self):
        self.level += 1
        self.canvas.setLevel(self.level)
        self.lLevel["text"] = str(self.level)

    def prevLevel(self):
        if self.level <= 0:
            self.level = 0
        else:
            self.level -= 1
            self.canvas.setLevel(self.level)
        self.lLevel["text"] = str(self.level)
