from playField import *
from playerRand import PlayerRand


class TicTacToe:
    def __init__(self):
        self.playField = PlayField(3, 3, 3)
        self.players = []
        self.curPlayer = 0
        self.playerMarkers = {0: 1, 1: 2}
        self.placed = [0, 0]
        self.turnNum = 0

        self.score = []

    def simulate(self, players):
        self.playField.clear()
        self.score = [0, 0]
        self.placed = [0, 0]
        self.turnNum = 0
        self.curPlayer = 0
        self.players = [p(self.playField, i+1) for i, p in enumerate(players)]

        playing = True
        while playing:
            self.turnNum += 1
            player = self.players[self.curPlayer]
            playerId = self.playerMarkers[self.curPlayer]
            pos = player.nextMove()

            try:
                self.playField.addMove(playerId, pos)
            except InvalidPos:
                pass
            else:
                self.placed[self.curPlayer] += 1
                if self.checkWin():
                    playing = False

            self.nextTurn()

        return self.score, self.turnNum

    def checkWin(self):
        winToup = self.playField.getWinner()
        if winToup:
            winner, line = winToup
            if winner == "draw":
                self.score[0] += 0.5
                self.score[1] += 0.5
                return True
            else:
                for playerId, mark in self.playerMarkers.items():
                    if mark == winner:
                        self.score[playerId] += 1
                        return True
        return False

    def nextTurn(self):
        self.curPlayer += 1
        self.curPlayer %= len(self.players)


if __name__ == "__main__":
    myPlayers = [PlayerRand, PlayerRand]
    game = TicTacToe()

    score, turns = game.simulate(myPlayers)

    print(score)
    print(turns, ",  ", sum(score))
