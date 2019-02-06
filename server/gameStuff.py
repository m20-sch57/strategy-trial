from enum import IntEnum
from server.commonFunctions import jsonParser

class TurnState(IntEnum):
    Correct = 0
    Incorrect = 1
    Last = 2

verdictStringDictionary = {}

class StrategyVerdict(IntEnum):
    Ok = 0
    IncorrectTurn = 1
    TimeLimitExceeded = 2
    Failed = 3
    ImportFail = 4
    PresentationError = 5
    #TODO: SecurityViolation

verdictStringDictionary = {
    StrategyVerdict.Ok : 'OK',
    StrategyVerdict.IncorrectTurn : 'Incorrect turn',
    StrategyVerdict.TimeLimitExceeded : 'Time limit exceeded',
    StrategyVerdict.Failed : 'Failed',
    StrategyVerdict.ImportFail : 'Import failed',
    StrategyVerdict.PresentationError : 'Presentation Error'
}

def nextPlayer(playerId: int) -> int:
    return 1 - playerId

class Result:
    def __init__(self, Verdict: StrategyVerdict = StrategyVerdict.Ok, Score: int = 0):
        self.verdict = Verdict # is this strategy working correct, or it gets TL, WA or RE?
        self.score = Score # points, which the strategy has got
    
    def __str__(self):
        dictionary = {'verdict' : int(self.verdict), 'score' : self.score}
        return str(dictionary)

    def goodStr(self):
        res = str(self.score) + " (" + verdictStringDictionary[self.verdict] + ")"
        return res

def resultFromStr(s: str):
    dictionary = jsonParser(s)
    return Result(dictionary['verdict'], dictionary['score'])

class InvocationResult:
    pass
