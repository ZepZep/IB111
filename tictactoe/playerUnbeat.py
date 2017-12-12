from playField import Pos
from playerRand import PlayerRand
from playerReact import PlayerReact
from random import shuffle


class PlayerUnbeat(PlayerReact):
    def nextMove(self):
        field = self.playField.getField()
        sizeX = len(field[0])
        sizeY = len(field)
        if sizeX == sizeY == 3:
            # try win and block move
            move = super()._move()
            if move is not None:
                return move

            # try other moves
            move = self.move3x3()
            return move

        return PlayerRand(self.playField, self.myID).nextMove()

    def move3x3(self):
        """Unbeatable strategy only for 3x3 playfield"""
        myID = self.myID
        field = self.playField.getField()
        otherID = myID % 2
        otherID += 1

        # Fork:
        # Block fork:
        #     Option 1:

        #     Option 2:

        # Center:
        if field[1][1] == 0:
            return Pos(1, 1)

        # Opposite corner:
        corners = [Pos(0, 0), Pos(0, 2), Pos(2, 0), Pos(2, 2)]
        shuffle(corners)
        for pos in corners:
            if field[pos.y][pos.x] == otherID:
                opposite = Pos(-pos.x + 2, -pos.y + 2)
                if field[opposite.y][opposite.x] == 0:
                    return opposite

        # Empty corner:
        for pos in corners:
            if field[pos.y][pos.x] == 0:
                return pos

        # Empty side:
        sides = [Pos(1, 0), Pos(0, 1), Pos(2, 1), Pos(1, 2)]
        shuffle(sides)
        for pos in sides:
            if field[pos.y][pos.x] == 0:
                return pos

        return Pos(0, 0)

    # @staticmethod
    # def getForkNumbers(id, playField):
    #     sizeX = len(playField[0])
    #     sizeY = len(playField)
    #
    #     cellNums = [[0 for x in range(sizeX)] for y in range(sizeY)]
    #
    #     for rowNum, row in enumerate(PlayField.rows(playField)):
    #         for colNum, c in enumerate(row):
    #             lasts = ()
    #             if len(lasts) < 3:
    #                 lasts = lasts + (c,)
    #             else:
    #                 lasts = lasts[1:] + (c,)
    #
    #             if len(lasts) == 3:
    #                 print("lasts")
    #                 l2, l1, l0 = lasts
    #
    #                 if l1 == id:
    #                     if l2 == 0 and l0 == 0:
    #                         cellNums[rowNum][colNum - 2] += 1
    #                         cellNums[rowNum][colNum - 0] += 1
    #
    #     for colNum, col in enumerate(PlayField.columns(playField)):
    #         for rowNum, c in enumerate(col):
    #             lasts = ()
    #             if len(lasts) < 3:
    #                 lasts = lasts + (c,)
    #             else:
    #                 lasts = lasts[1:] + (c,)
    #
    #             if len(lasts) == 3:
    #                 print("lasts")
    #                 l2, l1, l0 = lasts
    #
    #                 if l1 == id:
    #                     if l2 == 0 and l0 == 0:
    #                         cellNums[rowNum - 2][colNum] += 1
    #                         cellNums[rowNum - 0][colNum] += 1
    #
    #
    #     #     if PlayerReact._sumIfIn(id, col) == 2:
    #     #         rowNum = PlayerReact._tryPlace(col)
    #     #         if rowNum is not None:
    #     #             return Pos(colNum, rowNum)
    #     #
    #     # for diag, pos, isXPositive in PlayField.diagonalsPos(playField):