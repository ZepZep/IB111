class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def touple(self):
        return self.x, self.y

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Pos(self.x*other, self.y*other)

    def __repr__(self):
        return "Pos(" + str(self.x) + ", " + str(self.y) + ")"

    def __str__(self):
        return self.__repr__()


class InvalidPos(Exception):
    pass


def prepYield(line, pos, direction, withPos):
    if withPos:
        return line, pos, direction
    else:
        return line


class PlayField:
    def __init__(self, sizeX, sizeY, winNum):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.winNum = winNum
        self.field = [[0 for x in range(self.sizeX)] for y in range(self.sizeY)]

    def size(self):
        return self.sizeX, self.sizeY

    def clear(self):
        self.field = [[0 for x in range(self.sizeX)] for y in range(self.sizeY)]

    def getField(self):
        return self.field

    def addMove(self, playerID, pos):
        if self.field[pos.y][pos.x] == 0:
            self.field[pos.y][pos.x] = playerID
        else:
            raise InvalidPos

    def getWinner(self):
        freeCells = 0
        for line, pos, direction in self.lines(True):
            lastPlayer = 0
            lastCount = 0
            for i, cell in enumerate(line):
                if cell == 0:
                    freeCells += 1
                if cell == lastPlayer:
                    lastCount += 1
                else:
                    lastPlayer = cell
                    lastCount = 1

                if lastCount >= self.winNum and lastPlayer != 0:
                    winStart = pos + direction * (i - self.winNum + 1)
                    winEnd = pos + (direction * i)
                    return lastPlayer, (winStart.touple(), winEnd.touple())

        if freeCells == 0:
            return "draw", ((0, 0), (0, 0))

        return None

    def printField(self):
        for line in self.field:
            print(line)

    def lines(self, withPos=False):
        """returns a  generator that goes through each line exactly once"""
        for row in self.rows(withPos):
            yield row

        for col in self.columns(withPos):
            yield col

        for diagonal in self.diagonals(withPos):
            yield diagonal

    def rows(self, withPos=False):
        for y, row in enumerate(self.field):
            yield prepYield(row, Pos(0, y), Pos(1, 0), withPos)

    def columns(self, withPos=False):
        for col in range(len(self.field[0])):
            line = [self.field[row][col] for row in range(len(self.field))]
            yield prepYield(line, Pos(col, 0), Pos(0, 1), withPos)

    def diagonals(self, withPos=False):
        sizeX = len(self.field[0])
        sizeY = len(self.field)
        # bottom left -> top left
        pos = Pos(0, sizeY-1)
        while pos.y > 0:
            line = [self.field[pos.y + d][pos.x + d] for d in range(min(sizeX-pos.x, sizeY-pos.y))]
            yield prepYield(line, pos, Pos(1, 1), withPos)
            pos.y -= 1

        # top left -> top right
        while pos.x < sizeX:
            line = [self.field[pos.y + d][pos.x + d] for d in range(min(sizeX - pos.x, sizeY - pos.y))]
            yield prepYield(line, pos, Pos(1, 1), withPos)

            line = [self.field[pos.y + d][pos.x - d] for d in range(min(pos.x + 1, sizeY - pos.y))]
            yield prepYield(line, pos, Pos(-1, 1), withPos)
            pos.x += 1

        # top right -> bottom right
        pos.x -= 1
        pos.y += 1
        while pos.y < sizeY:
            line = [self.field[pos.y + d][pos.x - d] for d in range(min(pos.x + 1, sizeY - pos.y))]
            yield prepYield(line, pos, Pos(-1, 1), withPos)
            pos.y += 1
