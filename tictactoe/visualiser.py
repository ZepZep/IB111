import pygame
from playField import Pos


white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


class Visualiser:
    def __init__(self, playField, size):
        self.playField = playField
        self.players = {}
        self.size = size
        self.isShown = False
        self.screen = None
        self.font = None
        self.innerSide = 0
        self.side = 0
        self.marginLeft = 0
        self.marginTop = 100

    def show(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe")
        self.font = pygame.font.SysFont("monospace", 100)
        self.clear()

    def clear(self):
        self.screen.fill(white)
        self.drawGrid()
        pygame.display.flip()

    def setPlayField(self, playField):
        self.playField = playField

    def addPlayer(self, playerId, imagePath):
        image = pygame.image.load(imagePath)
        self.players[playerId] = image

    def drawGrid(self):
        gridSize = self.playField.size()

        margin = 10
        withBounds = True
        statusBarSize = 100

        horizontalSpace = self.size[0] - 2*margin
        hside = horizontalSpace // gridSize[0]
        verticalSpace = self.size[1] - 2*margin - statusBarSize
        vside = verticalSpace // gridSize[1]

        side = min(hside, vside)

        horizontalSpace = gridSize[0] * side
        verticalSpace = gridSize[1] * side
        marginLeft = (self.size[0] - horizontalSpace) // 2
        marginTop = (self.size[1] - verticalSpace - statusBarSize) // 2 + statusBarSize

        for x in range(marginLeft + side, marginLeft + (gridSize[0]) * side, side):
            pygame.draw.line(self.screen, black, (x, marginTop), (x, marginTop+verticalSpace), 3)

        for y in range(marginTop + side, marginTop + (gridSize[1]) * side, side):
            pygame.draw.line(self.screen, black, (marginLeft, y), (marginLeft + horizontalSpace, y), 3)

        if withBounds:
            rect = (marginLeft, marginTop, gridSize[0]*side, gridSize[1]*side)
            pygame.draw.rect(self.screen, black, rect, 3)

        self.innerSide = side - 3
        self.side = side

        self.marginLeft = marginLeft
        self.marginTop = marginTop

    def addMark(self, playerId, pos):
        try:
            img = self.players[playerId]
            img = pygame.transform.scale(img, (self.innerSide, self.innerSide))
            topLeft = (self.marginLeft + pos.x * self.side + 2, self.marginTop + pos.y * self.side + 2)
            self.screen.blit(img, topLeft)
        except KeyError:
            print("Invalid player")

    def setNextPlayer(self, playerId):
        margin = 10
        sbSize = 100 - 2*margin
        pygame.draw.rect(self.screen, white, (0, 0, self.size[0], 100))
        label = self.font.render("Hraje", 1, black)
        self.screen.blit(label, (margin, 2*margin))

        img = self.players[playerId]
        img = pygame.transform.scale(img, (sbSize, sbSize))
        topLeft = (self.marginLeft + 2*margin + label.get_rect()[2], margin)
        self.screen.blit(img, topLeft)
        pygame.display.flip()

    def drawWin(self, playerId, tl, br):
        margin = 10
        sbSize = 100 - 2 * margin
        pygame.draw.rect(self.screen, white, (0, 0, self.size[0], 100))
        if playerId in self.players:
            label = self.font.render("Vyhrálo", 1, red)
            self.screen.blit(label, (margin, 2 * margin))
            img = self.players[playerId]
            img = pygame.transform.scale(img, (sbSize, sbSize))
            topLeft = (self.marginLeft + 2 * margin + label.get_rect()[2], margin)
            self.screen.blit(img, topLeft)

            tlPoint = self.getCenterFromCell(tl)
            brPoint = self.getCenterFromCell(br)
            pygame.draw.line(self.screen, red, tlPoint, brPoint, 8)

        else:
            label = self.font.render("Remíza", 1, red)
            self.screen.blit(label, (margin, 2 * margin))

        pygame.display.flip()

    def getCellFromPoint(self, point):
        x = (point.x - self.marginLeft) // self.side
        y = (point.y - self.marginTop) // self.side

        gridSize = self.playField.size()
        if x > gridSize[0] or y > gridSize[1]:
            return None
        if x < 0 or y < 0:
            return None
        return Pos(x, y)

    def getCenterFromCell(self, pos):
        x = self.marginLeft + pos[0] * self.side + self.innerSide // 2
        y = self.marginTop + pos[1] * self.side + self.innerSide // 2

        return x, y
