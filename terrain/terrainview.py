from tkinter import *
from PIL import ImageTk


class TerrainView(Canvas):
    def __init__(self, root, map, width=550, height=550):
        Canvas.__init__(self, root,  width=width, height=height)
        self.width = width
        self.height = height
        self.level = 0
        self.lineColor = Label().cget("fg")
        self.img = None
        self.tkimg = None
        self.imagesprite = None


    def drawImage(self, img):
        """Kresli img na canvas"""
        # musim si ulozit reference na PhotoImage a imagesprite,
        # jinak mi je garbage collector sezere a nic se nezobrazi
        self.delete("all")
        self.img = img
        self.tkimg = ImageTk.PhotoImage(img)
        ipos = (self.width/2, self.height/2)
        self.imagesprite = self.create_image(ipos, image=self.tkimg)

