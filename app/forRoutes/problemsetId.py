from app.forRoutes.info import info
from app.forms import ProblemsetID
import tester
import useCasesAPI
from storage import storage
import structures

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

    paths = [path[0] for path in problem.rules.downloads]
    #paths - список путей до файлов, которые пользователь может скачать
    #print(paths)

    return [1, paths, problem, subList]

