from server.gameStuff import StrategyVerdict
from server.gameStuff import TurnState
from server.gameStuff import Result
from server.gameStuff import InvocationResult
from server.stringStuff import *

import subprocess

def runStrategy(game, gameState, playerId: int, logs):
    partialGameState = game.gameStateRep(gameState, playerId)
    result = [StrategyVerdict.Ok]
    process = subprocess.Popen(["python3", "shell.py"], bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    inp = partialGameState.toString() + '\n' + playerId.toString()
    try:
        out, err = process.communicate(input=inp, timeout=game.TimeLimit)
    except subprocess.TimeoutExpired:
        out, err = process.communicate()
        process.kill()
        result[0] = StrategyVerdict.TimeLimitExceeded
        return result
    if process.returncode != 0:
        result[0] = StrategyVerdict.Failed
    turn = classes.Turn()
    turn.fromString(out)
    if err != "":
        result[0] = StrategyVerdict.PresentationError
    result.append(turn)
    return result

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

def removePathes(importPathes):
    for path in importPathes:
        sys.path.remove(path)

def endJudge(pools, logs, results, importPathes):
    removePathes(importPathes)
    updateLogs(logs, results)

def badStrategy(game, i, verdict, result, logs, importPathes):
    removePathes(importPathes)
    result.results = strategyFailResults(game, i, verdict)
    updateLogs(logs, result.results)

def run(gamePath, classesPath, strategyPathes, importPathes, saveLogs = False):
    for path in importPathes:
        sys.path.append(path)
    classes = __import__(classesPath)
    game = __import__(gamePath)
    result = InvocationResult()
    logs = None
    if (saveLogs):
        logs = game.Logs()
        result.logs = logs
    '''
    strategies = []
    for i in range(len(strategyPathes)):
        try:
            strategies.append(__import__(strategyPathes[i]))
        except Exception:
            badStrategy(game, i, StrategyVerdict.ImportFail, result, logs, importPathes)
            return result
        if ("Strategy" not in dir(strategies[i])):
            badStrategy(game, i, StrategyVerdict.PresentationError, result, logs, importPathes)
        return result
    '''
    fullGameState = game.FullGameState()
    whoseTurn = 0
    for i in range(game.TurnLimit):
        turnList = runStrategy(classes, game, fullGameState, whoseTurn, logs)
        if (turnList[0] != StrategyVerdict.Ok):
            result.results = strategyFailResults(game, whoseTurn, turnList[0])
            endJudge(pools, logs, result.results, importPathes)
            return result
        turnResult = game.makeTurn(fullGameState, whoseTurn, turnList[1], logs)
        if (turnResult[0] == TurnState.Incorrect):
            result.results = strategyFailResults(game, whoseTurn, StrategyVerdict.IncorrectTurn)
            endJudge(pools, logs, result.results, importPathes)
            return result
        if (turnResult[0] == TurnState.Last):
            result.results = turnResult[1]
            endJudge(pools, logs, result.results, importPathes)
            return result
        fullGameState = turnResult[1]
        whoseTurn = turnResult[2]
    result.results = [Result() for i in range(PlayesCount)]
    endJudge(pools, logs, result.results, importPathes)
    return resul

if __name__ == '__main__':
    gamePath = input()
    classesPath = input()
    st1 = input()
    st2 = input()
    res = run(gamePath, classesPath, [st1, st2])
    for x in res:
        print(x)

