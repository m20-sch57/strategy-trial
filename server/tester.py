from server.structures import ProblemState, StrategyState, UserType
from server.structures import User, Rules, Problem, Submission, Tournament
from server.storage import storage
from server.gameStuff import StrategyVerdict, Result, InvocationResult
from server.commonFunctions import printToFile, unixTime
import os
import server.judge as judge
import sys

#TODO: same name of modules

def loadSources(sources):
    for source in sources:
        path = source[0]
        printToFile(source[1], path)

def loadProblem(problem):
    problempath = "problems/" + str(problem.id)
    loadSources(problem.rules.sources)

def loadProblemDownloads(problem):
    loadSources(problem.rules.downloads)

def getName(submission):
    return "sub" + str(submission.id)

def getModuleName(submission):
    return "problems." + str(submission.probId) + "." + getName(submission)

def getFilename(submission):
    return getName(submission) + ".py"

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
    scores = [[0, subs[i].id] for i in range(subCnt)]

    for i in range(subCnt):
        loadSubmission(subs[i], problem)

    for i in range(subCnt):
        for j in range(subCnt):
            if (i != j):
                print("judging ", i, j)
                invocationResult = judge.run(
                    "problems." + str(problemId) + ".game",
                    "problems." + str(problemId) + ".classes",
                    [getModuleName(subs[i]), getModuleName(subs[j])]
                )
                scores[i][0] += invocationResult.results[0].score
                scores[j][0] += invocationResult.results[1].score

    scores.sort(reverse = True)
    newTournament = Tournament(-1, unixTime(), scores)
    newTournamentId = storage.saveTournament(newTournament)
    problem.tournaments.append(newTournamentId)
    storage.saveProblem(problem)
    return newTournamentId
