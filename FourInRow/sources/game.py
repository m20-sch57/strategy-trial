from classes import *
from server.gameStuff import *

class FullGameState(GameState):
    pass

def gameStateRep(full: FullGameState, playerId: int) -> GameState:
    result = GameState()
    result.field = full.field
    return result

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
