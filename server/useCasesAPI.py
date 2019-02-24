from server.structures import ProblemState, StrategyState, UserType
from server.structures import User, Rules, Problem, Submission, Tournament
from server.storage import storage
from server.tester import tournament, testStrategies
from server.tester import loadProblemDownloads as TesterLPD
from server.commonFunctions import stringTime
import json

def addSubmission(userId, problemId, code):
    user = storage.getUser(userId)
    newSubmission = Submission(-1, userId, problemId, code, StrategyState.NonMain)
    idOfNewSubmission = storage.saveSubmission(newSubmission)
    if (problemId not in user.submissions):
        user.submissions[problemId] = []
    user.submissions[problemId].append(idOfNewSubmission)
    storage.saveUser(user)
    return idOfNewSubmission

# returns:
# 0 if this solution doesn't belong to this user
# 1 if the main solution became nonMain
# 2 if the main solution changed p
def changeMainSubmission(userId, subId):
    newMainSubmission = storage.getSubmission(subId)
    if ((newMainSubmission is None) or newMainSubmission.userId != userId):
        return 0
    user = storage.getUser(userId)
    probId = newMainSubmission.probId
    problem = storage.getProblem(probId)
    if newMainSubmission.type == StrategyState.Main:
        newMainSubmission.type = StrategyState.NonMain
        problem.submissions.remove(subId)
        returnCode = 1
    else:
        for anotherSubmissionId in user.submissions[probId]:
            anotherSubmission = storage.getSubmission(anotherSubmissionId)
            if (anotherSubmission.type == StrategyState.Main):
                anotherSubmission.type = StrategyState.NonMain
                storage.saveSubmission(anotherSubmission)
                problem.submissions.remove(anotherSubmissionId)
        newMainSubmission.type = StrategyState.Main
        problem.submissions.add(subId)
        returnCode = 2

    storage.saveSubmission(newMainSubmission)
    storage.saveProblem(problem)
    return returnCode

def addUser(username, password):
    newUser = User(-1, username, password, UserType.Default, dict())
    idOfNewUser = storage.saveUser(newUser)
    return idOfNewUser

def getProblemset():
    return storage.getProblemset()

def getSubmissionsU(userId):
    return storage.getSubmissionListU(userId)

def getSubmissionsUP(userId, probId):
    return storage.getSubmissionListUP(userId, probId)

def makeTornament(probId):
    return tournament(probId)

def judge(id1, id2):
    return testStrategies(id1, id2, saveLogs = True)

def getSubmissionCode(subId):
    submission = storage.getSubmission(subId)
    if (submission is None):
        return ""
    else:
        return submission.code

def getProbTournaments(probId):
    lst = json.loads(storage.getCertainField('problems', probId, 'tournaments'))
    res = [
        {
            'id' : len(lst) - i, 
            'tour_id' : lst[i], 
            'time' : stringTime(storage.getCertainField('tournaments', lst[i], 'time'))
        }
        for i in range(len(lst) - 1, -1, -1)
    ]
    return res

def getTournament(tourId):
    tournament = storage.getTournament(tourId)
    if (tournament is None):
        return None
    lst = []
    for i in range(len(tournament.standings)):
        position = tournament.standings[i]
        userId = storage.getCertainField('submissions', position[1], 'userId')
        lst.append([i + 1, position[0], storage.getCertainField('users', userId, 'username')])
    return {'time' : tournament.time, 'list' : lst}
