from structures import ProblemState, StrategyState, UserType
from structures import User, Rules, Problem, Submission, Tournament
from storage import storage
from tester import tournament, testStrategies

def addSubmission(userId, problemId, code):
    user = storage.getUser(userId)
    newSubmission = Submission(-1, userId, problemId, code, StrategyState.NonMain)
    idOfNewSubmission = storage.saveSubmission(newSubmission)
    user.submissions[problemId].append(idOfNewSubmission)
    storage.saveUser(user)
    return idOfNewSubmission

def changeMainSubmission(userId, subId):
    newMainSubmission = storage.getSubmission(subId)
    user = storage.getUser(userId)
    probId = newSubmission.probId
    problem = storage.getProblem(probId)
    for anotherSubmissionId in user.submissions[probId]:
        anotherSubmission = storage.getSubmission(anotherSubmissionId)
        if (anotherSubmission.type == StrategyState.Main):
            anotherSubmission.type = StrategyState.NonMain
            storage.saveSubmission(anotherSubmission)
            problem.submissions.erase(anotherSubmissionId)
    newMainSubmission.type = StrategyState.Main
    storage.saveSubmission(newMainSubmission)
    problem.submissions.insert(subId)
    storage.saveProblem(problem)

def addUser(username, password):
    newUser = User(-1, username, password, UserType.Defalut, dict())
    idOfNewUser = storage.saveUser(newUser)
    return idOfNewUser

def getProblemset():
    return storage.getProblemset()

def getSubmissionsU(userId):
    return storage.getSubmissionListU(userId)

def getSubmissionsUP(userId, probId):
    return storage.getSubmissionListUP(userId, probId)

def makeTornament(probId):
    return tournament(subId)

def judge(id1, id2):
    return testStrategies(id1, id2, saveLogs = True)
