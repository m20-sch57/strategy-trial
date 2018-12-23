from structures import *
from storage import storage
from gameStuff import TurnState
from gameStuff import StrategyVerdict
from gameStuff import Result
from commonFunctions import printToFile
from gameStuff import InvocationResult
import os
import judge

def rewriteTmp():
	os.system("rm -r tmp")
	os.system("mkdir tmp")

def rewriteTemplateTmp():
	os.system("rm -r app/templates/tmp")
	os.system("mkdir app/templates/tmp")

def loadProblem(id, saveLogs):
	problem = storage.getProblem(id)
	sources = problem.rules.sources
	for source in sources:
		path = "tmp/" + source[0]
		printToFile(source[1], path)

	if (saveLogs):
		rewriteTemplateTmp()
		for template in problem.rules.templates:
			path = "app/templates/tmp/" + template[0]
			printToFile(template[1], path)

def loadSubmission(submission, filename):
	printToFile(submission.code, filename)

def testStrategies(id1, id2, saveLogs = False):
	rewriteTmp()
	sub1 = storage.getSubmission(id1)
	sub2 = storage.getSubmission(id2)

	if (sub1.probId != sub2.probId):
		raise Exception('Trying to judge two strategies for different problems')

	problemId = sub1.probId
	loadProblem(problemId, saveLogs)

	loadSubmission(sub1, "tmp/0.py")
	loadSubmission(sub2, "tmp/1.py")
	invocationResult = judge.run("game.py", "classes.py", ["0.py", "1.py"], saveLogs = saveLogs)
	return invocationResult
