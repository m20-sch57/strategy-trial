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
    problempath = os.path.join('problems', str(problem.id))
    loadSources(problem.rules.sources)

def loadProblemDownloads(problem):
    loadSources(problem.rules.downloads)

def getName(submission):
    return "sub" + str(submission.id)

def getModuleName(submission):
    return getName(submission)

def getFilename(submission):
    return getName(submission) + ".py"

def loadSubmission(submission, problem):
    filename = os.path.join('problems', str(problem.id),
        'strategies', getFilename(submission))
    print(filename)
    printToFile(submission.code, filename)

def getProblemPath(probId):
    return os.path.join('problems', str(probId))

def getProblemStrategiesPath(probId):
    return os.path.join(getProblemPath(probId), 'strategies')

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

    invocationResult = judge.run(
        'game',
        'classes',
        [getModuleName(sub1), getModuleName(sub2)],
        [getProblemPath(problemId), getProblemStrategiesPath(problemId)],
        saveLogs = saveLogs
    )
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

    problemPath = os.path.join('problems', str(problemId))

    for i in range(subCnt):
        for j in range(subCnt):
            if (i != j):
                print("judging ", i, j)
                invocationResult = judge.run(
                    'game',
                    'classes',
                    [getModuleName(subs[i]), getModuleName(subs[j])],
                    [getProblemPath(problemId), getProblemStrategiesPath(problemId)]
                )
                print(invocationResult.results[0].goodStr())
                print(invocationResult.results[1].goodStr())
                scores[i][0] += invocationResult.results[0].score
                scores[j][0] += invocationResult.results[1].score

    scores.sort(reverse = True)
    newTournament = Tournament(-1, problemId, unixTime(), scores)
    newTournamentId = storage.saveTournament(newTournament)
    problem.tournaments.append(newTournamentId)
    storage.saveProblem(problem)
    return newTournamentId
