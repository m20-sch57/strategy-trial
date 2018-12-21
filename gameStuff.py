from enum import Enum
from commonFunctions import jsonParser

class TurnState(Enum):
	Correct = 0
	Incorrect = 1
	Last = 2

class StrategyVerdict(Enum):
	Ok = 0
	IncorrectTurn = 1
	TimeLimitExceeded = 2
	Failed = 3

def nextPlayer(playerId: int) -> int:
	return 1 - playerId

class Result:
	def __init__(self, Verdict: StrategyVerdict = StrategyVerdict.Ok, Score: int = 0):
		self.verdict = Verdict # is this strategy working correct, or it gets TL, WA or RE?
		self.score = Score # points, which the strategy has got
	
	def __str__(self):
		dictionary = {'verdict' : int(self.verdict), 'score' : self.score}
		return str(dictionary)

def resultFromStr(s: str):
	dictionary = jsonParser(s)
	return Result(dictionary['verdict'], dictionary['score'])

class InvocationResult:
	pass
