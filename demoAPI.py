from commonFunctions import readFile
from structures import *
from gameStuff import Result
from storage import storage
import tester

def addStrategy(code: str):
	submisson = Submission(-1, 0, 0, code, StrategyState.NonMain, Result())
	storage.saveSubmission(submisson)

def addStrategyByPath(path: str):
	addStrategy(readFile(path))

def getStrategyCode(id: int):
	submisson = storage.getSubmission(id)
	return submisson.code
