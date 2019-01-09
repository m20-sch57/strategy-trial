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

def rewriteStaticTmp():
	os.system("rm -r app/static/tmp")
	os.system("mkdir app/static/tmp")

def loadProblem(problem, saveLogs):
	sources = problem.rules.sources
	for source in sources:
		path = "tmp/" + source[0]
		printToFile(source[1], path)

	if (saveLogs):
		rewriteTemplateTmp()
		for template in problem.rules.templates:
			path = "app/templates/tmp/" + template[0]
			printToFile(template[1], path)
		rewriteStaticTmp()
		for static in problem.rules.static:
			path = "app/static/tmp/" + static[0]
			printToFile(static[1], path)

def getFilename(submission):
	return str(submission.id) + ".py"

def loadSubmission(submission):
	filename = "tmp/" + getFilename(submission)
	printToFile(submission.code, filename)

def testStrategies(id1, id2, saveLogs = False):
	rewriteTmp()
	sub1 = storage.getSubmission(id1)
	sub2 = storage.getSubmission(id2)

	if (sub1.probId != sub2.probId):
		raise Exception('Trying to judge two strategies for different problems')

	problemId = sub1.probId
	problem = storage.getProblem(id)
	loadProblem(problem, saveLogs)

	loadSubmission(sub1)
	loadSubmission(sub2)
	invocationResult = judge.run("game.py", "classes.py", [getFilename(sub1), getFilename(sub2)], saveLogs = saveLogs)
	return invocationResult

def resultsMerge(result1: Result, result2: Result):
	if (result2.verdict != StrategyVerdict.Ok):
		result1.verdict = result2.verdict
		result1.score = 0
	else:
		result1.score += result2.score

def doubleMerge(old_result1, old_result2, result1, result2):
	if (result1.verdict != StrategyVerdict.Ok):
		resultsMerge(old_result1, result1)
	if (result2.verdict != StrategyVerdict.Ok):
		resultsMerge(old_result2, result2)
	if (result1.verdict == StrategyVerdict.Ok and result2.verdict == StrategyVerdict.Ok):
		resultsMerge(old_result1, result1)
		resultsMerge(old_result2, result2)

def tournament(problemId: int):
	rewriteTmp()

	problem = storage.getProblem(problemId)
	problem.type = ProblemState.Testing
	storage.saveProblem(problem)
	loadProblem(problem, False)

	subCnt = len(problem.submissions)
	subs = [storage.getSubmission(problem.submissions[i]) for i in range(subCnt)]
	results = [Result() for i in range(subCnt)]

	for i in range(subCnt):
		loadSubmission(subs[i])

	for i in range(subCnt):
		for j in range(subCnt):
			if (i != j and results[i].verdict == StrategyVerdict.Ok and results[j].verdict == StrategyVerdict.Ok):
				invocationResult = judge.run("game.py", "classes.py", [getFilename(subs[i]), getFilename(subs[j])])
				doubleMerge(results[i], results[j], invocationResult.results[0], invocationResult.results[1])

	for i in range(subCnt):
		if (results[i].verdict != StrategyVerdict.Ok):
			subs[i].type = StrategyState.Failed
		subs[i].result = results[i]
		storage.saveSubmission(subs[i])

	problem.type = ProblemState.Upsolving
	storage.saveProblem(problem)
