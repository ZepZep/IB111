from time import strftime
from tkinter import *

from terrainview import TerrainView
from generators import generators
from imageshower import show
from utils import mkdir


class TerrainGen(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.generator = None
        self.createWidgets()
        self.setGenerator(list(generators.keys())[0])
        self.showMap()

    def createWidgets(self):
        self.master.title("Terrain")

        frameCnt = Frame(self, width=200)

        Label(frameCnt, text="Generator:").grid(row=0, column=0)
        var = StringVar(frameCnt)
        optionNames = list(generators.keys())
        var.set(optionNames[0])
        option = OptionMenu(frameCnt, var, *optionNames, command=self.setGenerator)
        option.grid(row=0, column=1)

        self.frameOptions = Frame(frameCnt)
        self.frameOptions.grid(row=1, column=0, columnspan=2)

        self.frameButtons = Frame(frameCnt)
        self.frameButtons.grid(row=2, column=0, columnspan=2)

        b = Button(self.frameButtons, text="Generate")
        b["command"] = self.generateMap
        b.pack(pady=5)

        b = Button(self.frameButtons, text="Show popup")
        b["command"] = self.popupMap
        b.pack(pady=5)

        b = Button(self.frameButtons, text="Save PNG")
        b["command"] = self.savePNG
        b.pack(pady=5)

        frameCnt.pack(side=RIGHT, fill="y")

        self.frameCnt = frameCnt

        self.canvas = TerrainView(self, None, width=700, height=700)
        self.canvas.pack(side=RIGHT)

    def setGenerator(self, name):
        self.generator = generators[name](self.showMap)
        self.clearOptionsFrame()
        self.generator.drawControls(self.frameOptions)
        self.frameOptions.grid(row=1, column=0, columnspan=2, pady=10)
        self.generateMap()

    def clearOptionsFrame(self):
        for w in self.frameOptions.grid_slaves():
            w.grid_forget()

    def generateMap(self):
        self.generator.generate()
        self.showMap()

    def showMap(self):
        img = self.generator.getImage()
        self.canvas.drawImage(img)

    def popupMap(self):
        img = self.generator.getImage()
        show(img, "aaa")

    def savePNG(self):
        directory = "png"
        mkdir(directory)

        filename = directory + "/img" + strftime("%y-%m-%d-%H-%M-%S") + ".png"
        self.canvas.img.save(filename)
