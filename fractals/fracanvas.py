from tkinter import *
import svgwrite
import os
import errno


def lines(points, chirs):
    """Takes list of points and chirs and makes them into lines with chir"""
    isFirst = True
    x0 = y0 = 0
    lineNum = 0
    for (x, y) in points:
        if isFirst:
            x0 = x
            y0 = y
            isFirst = False
        else:
            yield x0, y0, x, y, chirs[lineNum]
            x0, y0 = x, y
            lineNum += 1


class FraCanvas(Canvas):
    def __init__(self, root, fractal, width=700, height=700):
        Canvas.__init__(self, root,  width=700, height=700)
        self.width = width
        self.height = height
        self.level = 0
        self.lineColor = Label().cget("fg")

        self.setFractal(fractal)

    def setFractal(self, fractal):
        self.fractal = fractal
        self.initial, self.chirs = fractal.initial(self.width, self.height)
        self.points = self.initial

        self.drawLines()

    def setLevel(self, level):
        self.level = level
        self.points = []
        for (x0, y0, x1, y1, chir) in lines(self.initial, self.chirs):
            start = (x0, y0)
            end = (x1, y1)
            self.points.extend(self.fractal.segment(start, end, chir, level))

        self.drawLines()

    def drawLines(self):
        self.delete("all")
        self.create_line(self.points, width=1, fill=self.lineColor)

    def saveSvg(self):
        print("Making SVG")
        directory = "svg"

        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        for i in range(17):
            filename = directory + "/dragon%03d.svg" % i
            dwg = svgwrite.Drawing(filename)
            print("svg", len(self.points))
            pline = dwg.polyline(self.points)
            pline["stroke"] = "black"
            pline["stroke-width"] = "1"
            pline["fill"] = "none"
            dwg.add(pline)
            dwg.save()
            self.setLevel(self.level + 1)
