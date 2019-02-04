from structures import ProblemState, StrategyState, UserType
from structures import User, Rules, Problem, Submission, Tournament
from storage import storage
from gameStuff import StrategyVerdict, Result, InvocationResult
from commonFunctions import printToFile, unixTime
import os
import judge
import sys

#TODO: same name of modules

def loadSources(sources):
    for source in sources:
        path = source[0]
        printToFile(source[1], path)

def loadProblem(problem):
    problempath = "problems/" + str(problem.id)
    sys.path.append(problempath)
    sys.path.append(problempath + "/strategies")
    loadSources(problem.rules.sources)

def loadProblemDownloads(problem):
    loadSources(problem.rules.downloads)

def getFilename(submission):
    return "sub" + str(submission.id) + ".py"

def loadSubmission(submission, problem):
    #TODO use os.path.join
    filename = "problems/" + str(problem.id) + "/strategies/" + getFilename(submission)
    print(filename)
    printToFile(submission.code, filename)

def testStrategies(id1, id2, saveLogs = False):
    sub1 = storage.getSubmission(id1)
    sub2 = storage.getSubmission(id2)

    if (sub1.probId != sub2.probId):
        raise Exception('Trying to judge two strategies for different problems')

    problemId = sub1.probId
    problem = storage.getProblem(problemId)
    loadProblem(problem)

    loadSubmission(sub1, problem)
    loadSubmission(sub2, problem)
    invocationResult = judge.run("game.py", "classes.py", [getFilename(sub1), getFilename(sub2)], saveLogs = saveLogs)
    return invocationResult

def tournament(problemId):
    problem = storage.getProblem(problemId)
    problem.type = ProblemState.Testing
    storage.saveProblem(problem)
    loadProblem(problem)

    subCnt = len(problem.submissions)
    subs = [storage.getSubmission(subId) for subId in problem.submissions]
    scores = [[0, i] for i in range(subCnt)]

    for i in range(subCnt):
        loadSubmission(subs[i], problem)

    for i in range(subCnt):
        for j in range(subCnt):
            if (i != j):
                print("judging ", i, j)
                invocationResult = judge.run("game.py", "classes.py", [getFilename(subs[i]), getFilename(subs[j])])
                scores[i][0] += invocationResult.results[0].score
                scores[j][0] += invocationResult.results[1].score

    scores.sort(reverse = True)
    newTournament = Tournament(-1, unixTime(), scores)
    newTournamentId = storage.saveTournament(newTournament)
    problem.tournaments.append(newTournamentId)
    storage.saveProblem(problem)
    return newTournamentId
