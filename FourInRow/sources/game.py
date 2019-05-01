from classes import *
from server.gameStuff import *

class FullGameState:
    def __init__(self):
        self.field = [['.' for i in range(6)] for i in range(7)]

'''
.......
.......
.......
.......
.......
.......
'''

def check(gameState: FullGameState) -> str:
    winner = '.'


def makeTurn(gameState: FullGameState, playerId: int, turn: Turn, logs = None) -> list:
    charList = ['X', 'O']
    if turn.column not in range(0, 7):
        return [turnState.Incorrect, gameState, nextPlayer(playerId)]
    if gameState.field[turn.column][-1] != '.':
        return [turnState.Incorrect, gameState, nextPlayer(playerId)]
    winner = check(gameState)
    //
