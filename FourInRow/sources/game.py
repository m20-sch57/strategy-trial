from classes import *
from server.gameStuff import *
from app import app
from flask import render_template
import os

class FullGameState(GameState):
    pass

def gameStateRep(full: FullGameState, playerId: int) -> GameState:
    result = GameState()
    result.field = full.field
    return result

class Logs:
    def __init__(self):
        pass

    def processResults(self, results):
        self.results = results

    def show(self, probId, baseParams):
        with app.app_context():
            logPath = os.path.join('problems', str(probId), 'logs.html.j2')
            data = render_template(logPath, results = self.results, strId = str(probId), **baseParams)
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
    for i in range(4):
        if (gameState.field[x][y] != ans):
            return '.'
        x += dx
        y += dy
        if ((x < 0 or x > 6 or y < 0 or y > 5) and i != 3):
            return '.'
    return ans

def check(gameState: FullGameState) -> str:
    winner = '.'
    DIR = [[1, 0], [1, 1], [0, 1]]
    for i in range(4):
        for j in range(3):
            for Dir in DIR:
                winner = lineCheck(gameState, i, j, Dir[0], Dir[1])
                if winner != '.':
                    return winner
        for j in range(3, 7):
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
    if turn.column not in range(0, 7):
        return [turnState.Incorrect]
    if gameState.field[turn.column][-1] != '.':
        return [turnState.Incorrect] #gameState.field[turn.column]
    for i in range(6):
        if gameState.field[turn.column] == '.':
            gameState.field[turn.column] = charList[playerId]
            break
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
    return [TurnState.Last, [Result()]]

