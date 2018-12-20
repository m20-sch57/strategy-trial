from enum import Enum

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
		return str(self.verdict) + " " + str(self.score)

class InvocationResult:
	pass
