from structures import ProblemState, StrategyState
from structures import User, Rules, Problem, Submission, Tournament
from storage import storage

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
    for anotherSubmissionId in user.submissions[probId]:
        anotherSubmission = storage.getSubmission(anotherSubmissionId)
        if (anotherSubmission.type = StrategyState.Main):
            anotherSubmission.type = StrategyState.NonMain
            storage.saveSubmission(anotherSubmission)
    newMainSubmission.type = StrategyState.Main
    storage.saveSubmission(newMainSubmission)
