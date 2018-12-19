from structures import *
from storage import *
from gameStuff import TurnState
from gameStuff import StrategyVerdict
from gameStuff import Result
from commonFunctions import printToFile
import os

def rewriteTmp():
	os.system("rm -r tmp")
	os.system("mkdir tmp")

def loadProblem(storage, id):
	problem = storage.getProblem(id)
	sources = problem.rules.sources
	for source in sources:
		path = "tmp/" + source[0]
		printToFile(path, source[1])

def loadSubmission(submission, filename):
	printToFile(filename, submission.code)

def testStrategies(storage, id1, id2):
	rewriteTmp()
	sub1 = storage.getSubmission(id1)
	sub2 = storage.getSubmission(id2)

	if (sub1.probId != sub2.probId):
		raise Exception('Trying to judge two strategies for different problems')

	problemId = sub1.probId
	loadProblem(storage, problemId)

	loadSubmission(sub1, "0.py")
	loadSubmission(sub2, "1.py")

	