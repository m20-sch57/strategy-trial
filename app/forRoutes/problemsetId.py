from app.forRoutes.info import info
from app.forms import ProblemsetID
import server.tester as tester
import server.useCasesAPI as useCasesAPI
from server.storage import storage
import server.structures as structures
import os

def convertPathForApp(path):
    arr = path.split(os.sep)
    return os.path.join(*arr[1:])

def problemsetId(form: ProblemsetID, strId: str) -> list:
    try:
        probId = int(strId)
    except ValueError:
        return [0, [], None, None]
    problem = storage.getProblem(probId)
    if (problem is None):
        return [0, [], None, None]

    userId = info()[2]
    if userId == -1:
        subList = []
    else:
        subList = useCasesAPI.getSubmissionsUP(userId, probId)

    tester.loadProblemDownloads(problem)

    paths = [convertPathForApp(path[0]) for path in problem.rules.downloads]
    #paths - список путей до файлов, которые пользователь может скачать
    #print(paths)

    return [1, paths, problem, subList]

