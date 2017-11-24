import random
import numpy as np
from PIL import Image
from tkinter import Entry, Label, StringVar, IntVar, Scale, OptionMenu, Button, Checkbutton, HORIZONTAL

from numpyperlin import perlin, interpolatefcns
from utils import mkdir


class GenPerlin:
    def __init__(self, updateViewCallback, size=(500, 500)):
        self.updateView = updateViewCallback
        self.size = size
        self.uiroot = None
        self.interFcn = list(interpolatefcns.items())[0]

        self.lastImg = None
        self.heights = np.zeros(size, dtype=np.uint8)
        self.contours = np.zeros(size, dtype=np.int8)
        self.seaHeight = 100

    def generate(self):
        """generuje mapu"""
        if self.uiroot is not None:
            self.loadValues()
        random.seed(self.seed)
        np.random.seed(self.seed)
        self._genHeights()
        self._genContours(self.contDelta, self.contOff)

    def drawControls(self, root):
        """vykresli kontrolni panel"""
        self.uiroot = root
        seedLabel = Label(root, text="Seed:")
        seedLabel.grid(row=2, column=0)

        Label(root, text="Seed:").grid(row=2, column=0)
        self.sliderSeed = Scale(root, orient=HORIZONTAL, length=80, sliderlength=10,
                                from_=1, to=500, command=self.updateMap)
        self.sliderSeed.set(1)
        self.sliderSeed.grid(row=2, column=1)

        Label(root, text="Frequency:").grid(row=3, column=0)
        self.sliderFreq = Scale(root, orient=HORIZONTAL, length=80, sliderlength=10,
                                from_=1, to=40, command=self.updateMap)
        self.sliderFreq.set(10)
        self.sliderFreq.grid(row=3, column=1)

        Label(root, text="Octaves:").grid(row=4, column=0)
        self.sliderOct = Scale(root, orient=HORIZONTAL, length=80, sliderlength=10,
                                from_=1, to=10, command=self.updateMap)
        self.sliderOct.set(2)
        self.sliderOct.grid(row=4, column=1)

        Label(root, text="Interpolate:").grid(row=5, column=0)
        self.interFcnVar = StringVar()
        optionNames = list(interpolatefcns.keys())
        self.interFcnVar.set(optionNames[0])
        option = OptionMenu(root, self.interFcnVar, *optionNames, command=self.updateMap)
        option.grid(row=5, column=1)

        self.chbContoursVar = StringVar()
        self.chbContoursVar.set(0)
        self.chbContours = Checkbutton(root, text="Color image", variable=self.chbContoursVar,
                                       onvalue="RGB", offvalue="L")
        self.chbContours.grid(row=6, column=0, columnspan=2)

        Label(root, text="Contour delta:").grid(row=7, column=0)
        self.sliderContDelta = Scale(root, orient=HORIZONTAL, length=80, sliderlength=10,
                               from_=5, to=50, command=self.updateMap)
        self.sliderContDelta.set(25)
        self.sliderContDelta.grid(row=7, column=1)

        Label(root, text="Contour delta:").grid(row=8, column=0)
        self.sliderContOff = Scale(root, orient=HORIZONTAL, length=80, sliderlength=10,
                                     from_=0, to=25, command=self.updateMap)
        self.sliderContOff.set(0)
        self.sliderContOff.grid(row=8, column=1)

        self.butGif = Button(root, text="Gif Contour")
        self.butGif["command"] = self.makeGifCont
        self.butGif.grid(row=9, column=0)

        self.butGifSea = Button(root, text="Gif Sea")
        self.butGifSea["command"] = self.makeGifSea
        self.butGifSea.grid(row=9, column=1)

    def loadValues(self):
        """nacte hodnoty z kontrolniho panelu"""
        self.seed = int(self.sliderSeed.get())
        self.freq = 1.2 ** self.sliderFreq.get()
        self.numOct = self.sliderOct.get()
        self.interFcn = interpolatefcns[self.interFcnVar.get()]
        self.contDelta = self.sliderContDelta.get()
        if self.contDelta <= self.sliderContOff["to"]:
            self.sliderContOff.set(self.sliderContOff.get() % self.contDelta)
        self.sliderContOff["to"] = self.contDelta - 1
        self.contOff = self.sliderContOff.get()

    def updateMap(self, val=None):
        """updatuje mapu po zmene nastaveni"""
        self.generate()
        self.updateView()

    def _genHeights(self):
        """generuje pole vysek"""
        p = perlin(self.size, self.freq, self.numOct, interFunc=self.interFcn)
        p = (p + 1) * 255 / 2
        self.heights = p.astype(np.uint8)

    def _genContours(self, step=25, offset=0):
        """generuje vrstevnice"""
        self.contours = np.zeros(self.heights.shape, dtype=np.int8)
        for contHeight in range(offset, 255, step):
            self.contours[self.heights == contHeight] = contHeight

    def colorMap(self):
        """generuje barevnou vrstvu mapy"""
        seaH = self.seaHeight
        beachH = 110
        forestH = 140
        rockH = 160

        # timto zpusobem to delam kvuli tomu, aby to bylo vektorizovane -> rychlejsi
        sea = np.zeros(self.heights.shape, dtype=np.bool)
        sea[self.heights < seaH] = True

        beach = np.zeros(self.heights.shape, dtype=np.bool)
        beach[(seaH <= self.heights) & (self.heights < beachH)] = True

        forest = np.zeros(self.heights.shape, dtype=np.bool)
        forest[(beachH <= self.heights) & (self.heights < forestH)] = True

        rock = np.zeros(self.heights.shape, dtype=np.bool)
        rock[(forestH <= self.heights) & (self.heights < rockH)] = True

        snow = np.zeros(self.heights.shape, dtype=np.bool)
        snow[rockH <= self.heights] = True

        base = np.zeros(self.size + (3,), dtype=np.int8)
        base[..., 0] = self.heights
        base[..., 1] = self.heights
        base[..., 2] = self.heights
        base[sea, 2] = 200
        base[beach, 0] = 170
        base[beach, 1] = 150
        base[forest, 0] = 20
        base[forest, 1] = 150
        base[forest, 2] = 20
        base[rock, 0] = 100
        base[rock, 1] = 90
        base[rock, 2] = 80
        # base[snow, :] = 255

        return base

    def mergeImages(self):
        """sjednocuje ruzne vrstvy mapy"""
        doColors = True
        doContous = True

        if doColors:
            base = self.colorMap()
        else:
            base = np.stack((self.heights, self.heights, self.heights), 2)

        if doContous:
            base[self.contours != 0, :] = 0

        img = Image.frombytes("RGB", self.size, base.tobytes("C"))
        self.lastImg = img

        return img

    def getImage(self):
        """vraci posledni vygenerovany obrazek"""
        return self.mergeImages()


    def makeGifCont(self):
        """vytvari "GIF" posunovanim vrstevnic"""
        print("Making GIF")
        directory = "gif"
        mkdir(directory)

        for i in range(self.contDelta):
            self.sliderContOff.set(i)
            self.uiroot.update()

            filename = directory + "/cont%03d.png" % i
            self.lastImg.save(filename)

    def makeGifSea(self):
        """vytvari "GIF" zmenou vysky more"""
        print("Making GIF")
        directory = "gifSea"
        mkdir(directory)

        seaStates = list(range(0, 10)) + list(range(8, -10, -1)) + list(range(-8, 0))
        for i, dh in enumerate(seaStates):
            self.seaHeight = 100 + dh
            self.updateMap()
            self.uiroot.update()

            filename = directory + "/sea%03d.png" % i
            self.lastImg.save(filename)
