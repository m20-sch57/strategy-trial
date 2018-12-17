from gameStuff import StrategyVerdict
from gameStuff import TurnState
from gameStuff import Result
import os

def importPath(path: str):
	path = os.path.splitext(path)[0]
	return __import__(path)

def runStrategy(game, strategy, gameState, playerId: int):
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
		turn = strategy.Strategy(partialGameState, playerId)
	except TimeoutError:
		result[0] = [StrategyVerdict.TimeLimitExceeded]
	except Exception:
		result[0] = [StrategyVerdict.Failed]
	finally:
		signal.alarm(0)

	if (result[0] == StrategyVerdict.Ok):
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

def run(gamePath: str, classesPath: str, strategyPathes : list) -> list:
	classes = importPath(classesPath)
	game = importPath(gamePath)
	strategies = []
	for st in strategyPathes:
		strategies.append(importPath(st))

	fullGameState = game.FullGameState()
	whoseTurn = 0

	for i in range(game.TurnLimit):
		turnList = runStrategy(game, strategies[whoseTurn], fullGameState, whoseTurn)
		if (turnList[0] != StrategyVerdict.Ok):
			return strategyFailResults(game, whoseTurn, turnList[0])
		
		turnResult = game.makeTurn(fullGameState, whoseTurn, turnList[1])
		if (turnResult[0] == TurnState.Incorrect):
			return strategyFailResults(game, whoseTurn, StrategyVerdict.Incorrect)

		if (turnResult[0] == TurnState.Last):
			return turnResult[1]

		fullGameState = turnResult[1]
		whoseTurn = turnResult[2]

	return [Result() for i in range(PlayesCount)]

if __name__ == '__main__':
	gamePath = input()
	classesPath = input()
	st1 = input()
	st2 = input()
	res = run(gamePath, classesPath, [st1, st2])
	for x in res:
		print(x)
