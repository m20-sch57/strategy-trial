from server.structures import ProblemState, StrategyState, UserType
from server.structures import User, Rules, Problem, Submission, Tournament
from server.storage import storage, status
from server.tester import tournament, testStrategies
from server.tester import loadProblemDownloads as TesterLPD
from server.commonFunctions import stringTime
import json

def addSubmission(userId, problemId, code):
    user = storage.getUser(userId)
    problem = storage.getProblem(problemId)
    newSubmission = Submission(-1, userId, problemId, code, StrategyState.NonMain)
    idOfNewSubmission = storage.saveSubmission(newSubmission)
    if (problemId not in user.submissions):
        user.submissions[problemId] = []
    user.submissions[problemId].append(idOfNewSubmission)
    problem.allSubmissions.append(idOfNewSubmission)
    storage.saveUser(user)
    storage.saveProblem(problem)
    return idOfNewSubmission

# returns:
# 0 if this solution doesn't belong to this user
# 1 if the main solution became nonMain
# 2 if the main solution changed
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

def changeUserType(userId: int) -> str:
    user = storage.getUser(userId)
    if (user == None):
        return "There is no user with this id"
    if (user.username == "root" and user.id == 0):
        return "Type of root can't be changed!"
    if (user.type == UserType.Admin):
        user.type = UserType.Default
    else:
        user.type = UserType.Admin
    storage.saveUser(user)
    return "Type successfully changed"

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

def getAllUsers():
    return storage.getAllUsers()

def makeTournament(id):
    while (status.RunningTournament()):
        pass
    status.tournamentStarted(id)
    result = tournament(id)
    status.tournamentStopped(id)
    return result

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

def createDelayedTournament(probId, time):
    prob = storage.getProblem(probId)
    prob.nextTournament = time
    storage.saveProblem(prob)
