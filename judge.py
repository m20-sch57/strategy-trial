from gameStuff import StrategyVerdict
from gameStuff import TurnState
from gameStuff import Result
from gameStuff import InvocationResult
import os

import sys
sys.path.append("tmp")

def importPath(path: str):
	path = os.path.splitext(path)[0]
	return __import__(path)

def runStrategy(game, strategy, gameState, playerId: int, logs):
	import signal

	class TimeoutError(Exception):
		pass

	def handler(signum, frame):
		raise TimeoutError()

	partialGameState = game.gameStateRep(gameState, playerId)
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(game.TimeLimit)
	result = [StrategyVerdict.Ok]

	try:
		turn = strategy.Strategy(partialGameState, playerId, logs)
	except TimeoutError:
		result[0] = [StrategyVerdict.TimeLimitExceeded]
	except Exception:
		result[0] = [StrategyVerdict.Failed]
	finally:
		signal.alarm(0)

	if (result[0] == StrategyVerdict.Ok):
		result.append(turn)
	else:
		if (logs is not None):
			logs.unexpectedVerdict(result[0])

	return result

PlayesCount = 2

def strategyFailResults(game, strategyId : int, verdict) -> list:
	results = [Result() for i in range(PlayesCount)]
	for i in range(len(results)):
		results[i].score = game.MaxScore
	results[strategyId].score = 0
	results[strategyId].verdict = verdict
	return results

def run(gamePath: str, classesPath: str, strategyPathes : list, saveLogs = False) -> InvocationResult:
	classes = importPath(classesPath)
	game = importPath(gamePath)
	strategies = []
	for st in strategyPathes:
		strategies.append(importPath(st))
	result = InvocationResult()
	logs = None
	if (saveLogs):
		logs = game.Logs()
		result.logs = logs

	fullGameState = game.FullGameState()
	whoseTurn = 0

	for i in range(game.TurnLimit):
		turnList = runStrategy(game, strategies[whoseTurn], fullGameState, whoseTurn)
		if (turnList[0] != StrategyVerdict.Ok):
			result.results = strategyFailResults(game, whoseTurn, turnList[0])
			return result
		
		turnResult = game.makeTurn(fullGameState, whoseTurn, turnList[1])
		if (turnResult[0] == TurnState.Incorrect):
			result.results = strategyFailResults(game, whoseTurn, StrategyVerdict.Incorrect)
			logs.unexpectedVerdict(StrategyVerdict.Incorrect)
			return result

		if (turnResult[0] == TurnState.Last):
			result.results = turnResult[1]
			return result

		fullGameState = turnResult[1]
		whoseTurn = turnResult[2]

	result.results = [Result() for i in range(PlayesCount)]
	return result

if __name__ == '__main__':
	gamePath = input()
	classesPath = input()
	st1 = input()
	st2 = input()
	res = run(gamePath, classesPath, [st1, st2])
	for x in res:
		print(x)
