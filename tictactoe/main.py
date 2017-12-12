from playField import *
from visualiser import *
from playerRand import PlayerRand
from playerReact import PlayerReact
from playerUnbeat import PlayerUnbeat
from playerNeural import PlayerNeural
from time import sleep
import sys
import numpy as np

playField = PlayField(3, 3, 3)
visualiser = Visualiser(playField, (800, 900))

curPlayer = 1
numPlayers = 2
visualiser.addPlayer(1, "img/circle.png")
visualiser.addPlayer(2, "img/cross.png")
visualiser.show()
visualiser.setNextPlayer(curPlayer)

aiPlayers = {}
# aiPlayers[1] = PlayerReact(playField, 1)
# aiPlayers[1] = PlayerUnbeat(playField, 1)
aiPlayers[2] = PlayerUnbeat(playField, 2)
# aiPlayers[2] = PlayerNeural()
# aiPlayers[2].setStrategy(np.random.random(10*10+10*9) - 0.5)


def nextPlayer(advance=True):
    if advance:
        global curPlayer
        curPlayer %= 2
        curPlayer += 1
        visualiser.setNextPlayer(curPlayer)

    while curPlayer in aiPlayers:
        player = aiPlayers[curPlayer]
        pos = player.nextMove()
        try:
            playField.addMove(curPlayer, pos)
        except InvalidPos:
            print("Invalid move from ", curPlayer)
            curPlayer %= 2
            curPlayer += 1
            visualiser.setNextPlayer(curPlayer)
            continue

        sleep(0.2)
        visualiser.addMark(curPlayer, pos)
        pygame.display.flip()
        if checkWin():
            waitForPress()
            resetGame()
            return

        curPlayer %= 2
        curPlayer += 1
        visualiser.setNextPlayer(curPlayer)


def waitForPress():
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            break
        elif event.type == pygame.KEYDOWN:
            break


def checkWin():
    winToup = playField.getWinner()
    if winToup:
        winner, line = winToup
        print("Player ", winner, " wins!")
        visualiser.drawWin(winner, line[0], line[1])
        return True


def resetGame():
    playField.clear()
    visualiser.clear()
    global curPlayer
    curPlayer = 1
    visualiser.setNextPlayer(curPlayer)


while True:
    nextPlayer(False)
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
        mousePos = pygame.mouse.get_pos()
        pos = visualiser.getCellFromPoint(Pos(mousePos[0], mousePos[1]))

        if pos:
            try:
                playField.addMove(curPlayer, pos)
            except InvalidPos:
                print("Invalid move")
                nextPlayer()
                continue

            visualiser.addMark(curPlayer, pos)
            pygame.display.flip()
            if checkWin():
                waitForPress()
                resetGame()
            else:
                nextPlayer()
