from enum import Enum

class TurnState(Enum):
	Correct = 0
	Incorrect = 1
	Last = 2

class StratrgyVerdict(Enum):
	Ok = 0
	IncorrectTurn = 1
	TimeLimitExceeded = 2
	Failed = 3

def nextPlayer(playerId: int) -> int:
	return 1 - playerId

class Result:
    def __init__(self, Verdict: StratrgyVerdict = StratrgyVerdict.Ok, Score: int = 0):
        self.verdict = Verdict # is this strategy working correct, or it gets TL, WA or RE?
        self.score = Score # points, which the strategy has got
