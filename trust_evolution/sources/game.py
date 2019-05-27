from classes import *
from server.gameStuff import *
from app import app
from flask import render_template
from copy import deepcopy
import os.path

InitCoinsCnt = 20

class Logs:
    def __init__(self):
        pass

    def processResults(self, results):
        self.results = results

    def endGame(self, finalState):
        self.finalState = finalState

    def show(self, probId, baseParams):
        with app.app_context():
            logPath = os.path.join('problems', str(probId), 'logs.html.j2')
            data = render_template(logPath, 
                turns = self.finalState.turns, coins = [x - InitCoinsCnt for x in self.finalState.coins],
                res1 = self.results[0].goodStr(), res2 = self.results[1].goodStr(),
                strId = str(probId), **baseParams
            )
        return data

class FullGameState:
    def __init__(self):
        self.turns = [[], []]
        self.coins = [InitCoinsCnt, InitCoinsCnt]

def gameStateRep(full: FullGameState, playerId: int) -> GameState:
    result = GameState()
    result.turns = deepcopy(full.turns)
    if (len(result.turns[0]) > len(result.turns[1])):
        del result.turns[0][-1]
    return result

MaxScore = 100
TimeLimit = 1
TurnLimit = 100
GameEnd = 5

def makeTurn(gameState: FullGameState, playerId: int, turn: Turn, logs = None) -> list:
    if (turn.trust < 0 or turn.trust > 1):
        return [TurnState.Incorrect]
    gameState.turns[playerId].append(turn.trust)
    if (turn.trust == 1):
        gameState.coins[playerId] -= 1
        gameState.coins[nextPlayer(playerId)] += 3
    if (len(gameState.turns[0]) == GameEnd and playerId == 1):
        if (logs is not None):
            logs.endGame(gameState)
        return [TurnState.Last, [Result(StrategyVerdict.Ok, gameState.coins[0] * 5 // 2), Result(StrategyVerdict.Ok, gameState.coins[1] * 5 // 2)]]
    return [TurnState.Correct, gameState, nextPlayer(playerId)]
