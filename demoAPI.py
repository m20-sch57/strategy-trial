from commonFunctions import readFile
from structures import *
from gameStuff import Result
from storage import storage
import tester

def addStrategy(code: str):
	submisson = Submission(-1, 0, 0, code, StrategyState.NonMain, Result())
	storage.saveSubmission(submisson)

def addMainStrategy(code: str):
	submisson = Submission(-1, 0, 0, code, StrategyState.Main, Result())
	id = storage.saveSubmission(submisson)
	problem0 = storage.getProblem(0)
	problem0.submissions.append(id)
	storage.saveProblem(problem0)

def addStrategyByPath(path: str):
	addStrategy(readFile(path))

def addMainStrategyByPath(path: str):
	addMainStrategy(readFile(path))

def getStrategyCode(id: int):
	submisson = storage.getSubmission(id)
	return submisson.code

def judge(id1: int, id2: int):
	invocationResult = tester.testStrategies(id1, id2, saveLogs = True)
	return invocationResult

def tournament():
	tester.tournament(0)
	problem = storage.getProblem(0)
	for subid in problem.submissions:
		sub = storage.getSubmission(subid)
		print(sub.result.goodStr(100))
