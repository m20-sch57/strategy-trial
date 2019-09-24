from server.gameStuff import *
from app import app
from flask import render_template
import os
from server.commonFunctions import problemFolder

class GameState:
    def __init__(self):
        self.field = [['.' for i in range(6)] for i in range(7)]

    def toString(self):
        ans = []
        for i in self.field:
            ans += i
        return ' '.join(ans)

    def fromString(self, s):
        a = s.split()
        for i in range(7):
            self.field[i] = a[6*i:6*(i+1)]

# Field is a list of columns, enumerarted from 0 to 6, from left to right
# each column is a list of cells, enumerated from 0 to 5, from DOWN to UP.
# each sell represents it's state, if it has '.' it's unused.
# In other cases it has 'X' or 'O' that represents it's owner.

class Turn:
    def __init__(self, column=0):
        self.column = column

    def toString(self):
        return str(self.column)

    def fromString(self, s):
        self.column = int(s)


class FullGameState:
    def __init__(self):
        self.field = [['.' for i in range(6)] for i in range(7)]

def gameStateRep(full: FullGameState, playerId: int) -> GameState:
    result = GameState()
    result.field = full.field
    return result

class Logs:
    def __init__(self):
        self.logs = []

    def processResults(self, results):
        self.results = results

    def update(self, game: FullGameState, fullTurn: list):
        new_field = [['.' for i in range(7)] for i in range(6)]
        for i in range(7):
            for j in range(6):
                new_field[j][i] = [game.field[i][5 - j]]
                if [j, i] == fullTurn:
                    new_field[j][i].append(1)
        self.logs.append(new_field)

    def show(self, probId, baseParams):
        with app.app_context():
            logPath = os.path.join('problems', problemFolder(probId), 'logs.html.j2')
            data = render_template(logPath, logs = self.logs, res1 = self.results[0].goodStr(), res2 = self.results[1].goodStr(), strId = problemFolder(probId), **baseParams)
        return data

'''
.......
.......
.......
.......
.......
.......
'''

MaxScore = 100
TimeLimit = 1
TurnLimit = 100

def lineCheck(gameState: FullGameState, x: int, y: int, dx: int, dy: int) -> str: # x - column, y - row
    ans = gameState.field[x][y]
    for i in range(3):
        x += dx
        y += dy
        if ((x < 0 or x > 6 or y < 0 or y > 5)):
            return '.'
        if (gameState.field[x][y] != ans):
            return '.'
    return ans

def check(gameState: FullGameState) -> str:
    winner = '.'
    DIR = [[1, 0], [1, 1], [0, 1], [1, -1]]
    for i in range(7):
        for j in range(6):
            for Dir in DIR:
                winner = lineCheck(gameState, i, j, Dir[0], Dir[1])
                if winner != '.':
                    return winner
        for j in range(3, 6):
            winner = lineCheck(gameState, i, j, 1, 0)
            if winner != '.':
                return winner
    for i in range(4, 7):
        for j in range(3):
            winner = lineCheck(gameState, i, j, 0, 1)
            if winner != '.':
                return winner
    return winner

def nextPlayer(playerId: int) -> int:
    return 1 - playerId

def makeTurn(gameState: FullGameState, playerId: int, turn: Turn, logs = None) -> list:
    charList = ['X', 'O']
    fullTurn = [None, turn.column]
    if turn.column not in range(0, 7):
        return [TurnState.Incorrect]
    if gameState.field[turn.column][-1] != '.':
        return [TurnState.Incorrect] #gameState.field[turn.column]
    for i in range(6):
        if gameState.field[turn.column][i] == '.':
            gameState.field[turn.column][i] = charList[playerId]
            fullTurn[0] = 5 - i
            break
    if (logs != None):
        logs.update(gameState, fullTurn)
    full = 1
    for i in range(7):
        if gameState.field[i][-1] == '.':
            full = 0
            break
    if full:
        return [TurnState.Last, Result(StrategyVerdict.Ok, MaxScore // 2), Result(StrategyVerdict.Ok, MaxScore // 2)]
    winner = check(gameState)
    if winner == '.':
        return [TurnState.Correct, gameState, nextPlayer(playerId)]
    result = [Result(StrategyVerdict.Ok, 0), Result(StrategyVerdict.Ok, 0)]
    if charList[playerId] == winner:
        result[playerId].score = MaxScore
    else:
        result[nextPlayer(playerId)].score = MaxScore
    return [TurnState.Last, result]

