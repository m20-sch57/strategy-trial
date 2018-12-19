from commonFunctions import readFile
from structures import *
from gameStuff import Result
import tester

def addStrategy(storage, code: str):
	submisson = Submisson(-1, 0, 0, code, StrategyState.NonMain, Result())
	storage.saveSubmission(submisson)

def addStrategyByPath(storage, path: str):
	addStrategy(storage, readFile(path))

def getStrategyCode(storage, id: int):
	submisson = storage.getSubmission(id)
	return submisson.code
