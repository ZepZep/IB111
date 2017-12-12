from playField import Pos
# from playField import PlayField
from playerRand import PlayerRand


def incrementDictPos(pos, dict):
    key = pos.touple()
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1


def checkCellMode(winNum, lastCount, isMine, freeLastPos, freePrePos, mode):
    """Checks if is current cell fits into mode"""
    if mode == "other-1":
        if lastCount == winNum - 1 and not isMine:
            return freeLastPos if freeLastPos else freePrePos
    elif mode == "other-2":
        if lastCount == winNum - 2 and not isMine:
            return freeLastPos if freeLastPos and freePrePos else None
    elif mode == "own-1":
        if lastCount == winNum - 1 and isMine:
            return freeLastPos if freeLastPos else freePrePos
    elif mode == "own-2":
        if lastCount == winNum - 2 and isMine:
            return freeLastPos if freeLastPos and freePrePos else None


class PlayerReact(PlayerRand):
    def nextMove(self):
        move = self._move()
        if move is not None:
            return move

        return super().nextMove()

    def _move(self):
        # moje -1 -> nejvetsi cislo
        # jeho -1
        # moje -2 -> nejvetsi cislo
        # jeho -2

        mode = "own-1"
        ownCandidates = {}
        for pos in self.suitableCells(mode):
            incrementDictPos(pos, ownCandidates)
        if len(ownCandidates) > 0:
            bestPosTup = max(ownCandidates, key=ownCandidates.get)
            return Pos(bestPosTup[0], bestPosTup[1])

        mode = "other-1"
        for pos in self.suitableCells(mode):
            return pos

        # mode = "own-2"
        # ownCandidates = {}
        # for pos in self.suitableCells(mode):
        #     incrementDictPos(pos, ownCandidates)
        # if len(ownCandidates) > 0:
        #     bestPos = max(ownCandidates, key=ownCandidates.get)
        #     return bestPos

        # mode = "other-2"
        # for pos in self.suitableCells(mode):
        #     return pos

    def suitableCells(self, mode):
        myID = self.myID
        playField = self.playField
        otherID = myID % 2
        otherID += 1

        for line, pos, direction in playField.lines(True):
            lastPlayer = 0
            lastCount = 0
            freePre = False
            freeLast = False
            for i, cell in enumerate(line):
                if cell != 0:
                    if cell == lastPlayer:
                        lastCount += 1
                        if freeLast:
                            freePre = True
                    else:
                        if lastPlayer != 0:
                            freePre = False
                        lastPlayer = cell
                        lastCount = 1

                freeLast = cell == 0

                freeLastPos = pos + (direction * i) if freeLast else None
                freePrePos = pos + (direction * (i - playField.winNum + 1)) if freePre else None

                # print(playField.winNum, lastCount, lastPlayer==myID, freeLastPos, freePrePos, mode)
                outCell = checkCellMode(playField.winNum, lastCount, lastPlayer==myID,
                                        freeLastPos, freePrePos, mode)
                if outCell is not None:
                    yield outCell

                if cell == 0:
                    lastPlayer = 0
                    lastCount = 0
                    freePre = True
