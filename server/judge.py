from server.gameStuff import StrategyVerdict
from server.gameStuff import TurnState
from server.gameStuff import Result
from server.gameStuff import InvocationResult
import sys
import importlib

import subprocess

shellRoute = "shell.py"

def runStrategy(game, gameModule, gameState, playerId: int, strategyModule):
    partialGameState = game.gameStateRep(gameState, playerId)
    result = [StrategyVerdict.Ok]
    process = subprocess.Popen(["python3", shellRoute], bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    inp = '\n'.join([strategyModule, gameModule, partialGameState.toString(), str(playerId)])
    """
        gameState must have method toString that converts object to string WITHOUT '\n' and fromString that converts string without '\n' to object.
        turn --- the same
    """
    try:
        out, err = process.communicate(input=inp, timeout=game.TimeLimit)
    except subprocess.TimeoutExpired:
        out, err = process.communicate()
        process.kill()
        result[0] = StrategyVerdict.TimeLimitExceeded
        return result
    if process.returncode != 0:
        print(out)
        print(err)
        return [StrategyVerdict.Failed]
    turn = game.Turn()
    turn.fromString(out)
    result.append(turn)
    return result

PlayesCount = 2

def strategyFailResults(game, strategyId : int, verdict) -> list:
    results = [Result() for i in range(PlayesCount)]
    for i in range(len(results)):
        results[i].score = game.MaxScore
    results[strategyId].score = 0
    results[strategyId].verdict = verdict
    return results

def updateLogs(logs, results):
    if (logs is not None):
        logs.processResults(results)

def endJudge(logs, results):
    updateLogs(logs, results)

def run(gameModule, strategyModules, saveLogs = False):
    print(gameModule)
    print(strategyModules)
    game = importlib.import_module(gameModule)
    result = InvocationResult()
    logs = None
    if (saveLogs):
        logs = game.Logs()
        result.logs = logs
    fullGameState = game.FullGameState()
    whoseTurn = 0
    for i in range(game.TurnLimit):
        turnList = runStrategy(game, gameModule, fullGameState, whoseTurn, strategyModules[whoseTurn])
        if (turnList[0] != StrategyVerdict.Ok):
            result.results = strategyFailResults(game, whoseTurn, turnList[0])
            endJudge(logs, result.results)
            return result
        turnResult = game.makeTurn(fullGameState, whoseTurn, turnList[1], logs)
        if (turnResult[0] == TurnState.Incorrect):
            result.results = strategyFailResults(game, whoseTurn, StrategyVerdict.IncorrectTurn)
            endJudge(logs, result.results)
            return result
        if (turnResult[0] == TurnState.Last):
            result.results = turnResult[1]
            endJudge(logs, result.results)
            return result
        fullGameState = turnResult[1]
        whoseTurn = turnResult[2]
    result.results = [Result() for i in range(PlayesCount)]
    endJudge(logs, result.results)
    return result

