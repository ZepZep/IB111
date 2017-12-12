from playField import Pos
from random import randint as ri


class PlayerRand:
    def __init__(self, playField, myID):
        self.myID = myID
        self.playField = playField

    def start(self, playField, myID):
        self.myID = myID
        self.playField = playField

    def nextMove(self):
        playFieldList = self.playField.getField()
        freeCellNum = 0
        for line in playFieldList:
            for cell in line:
                if cell == 0:
                    freeCellNum += 1

        selectedIndex = ri(1, freeCellNum)
        height = len(playFieldList)
        width = len(playFieldList[0])

        for x in range(height):
            for y in range(width):
                if playFieldList[y][x] == 0:
                    selectedIndex -= 1
                    if selectedIndex == 0:
                        return Pos(x, y)
