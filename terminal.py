import server.useCasesAPI as useCasesAPI
import server.parser as parser
from server.commonFunctions import readFile
from server.storage import storage

def isInt(x):
    try:
        y = int(x)
    except ValueError:
        return False
    return True

while (True):
    try:
        line = input()
    except KeyboardInterrupt:
        break

    params = line.split()
    command = params[0]

    if (command == 'look'):
        if (len(params) < 3 or (not isInt(params[2]))):
            continue

        if (params[1][0] == 'u'):
            id = int(params[2])
            resp = storage.getUser(id)

        if (params[1][0] == 'p'):
            id = int(params[2])
            resp = storage.getProblem(id)

        if (params[1][0] == 's'):
            id = int(params[2])
            resp = storage.getSubmission(id)

        if (params[1][0] == 't'):
            id = int(params[2])
            resp = storage.getTournament(id)

        if (resp is not None):
            resp.print()

    if (command == 'add'):
        if (len(params) < 2):
            continue

        if (params[1][0] == 's'):
            if (len(params) < 5):
                continue

            if ((not isInt(params[2])) or (not isInt(params[3]))):
                continue

            filename = params[4]
            userId = int(params[2])
            problemId = int(params[3])
            useCasesAPI.addSubmission(userId, problemId, readFile(params[4]))

        if (params[1][0] == 'u'):
            if (len(params) < 4):
                continue

            useCasesAPI.addUser(params[2], params[3])

    if (command == 'ch'):
        if (len(params) < 3 or (not isInt(params[1])) or (not isInt(params[2]))):
            continue

        useCasesAPI.changeMainSubmission(int(params[1]), int(params[2]))

    if (command == 'tour'):
        if (len(params) < 2 or (not isInt(params[1]))):
            continue

        probId = int(params[1])
        useCasesAPI.tournament(probId)

    if (command == 'judge'):
        if (len(params) < 3 or (not isInt(params[1])) or (not isInt(params[2]))):
            continue

        id1 = int(params[1])
        id2 = int(params[2])
        invocationResult = useCasesAPI.judge(id1, id2)
        print(invocationResult.results[0].goodStr())
        print(invocationResult.results[1].goodStr())

    if (command == 'problemset'):
        res = storage.getProblemset()
        print(res)

    if (command == 'subs'):
        if (len(params) == 2 and isInt(params[1])):
            res = storage.getSubmissionListU(int(params[1]))
            print(res)

        if (len(params) == 3 and isInt(params[1]) and isInt(params[2])):
            res = storage.getSubmissionListUP(int(params[1]), int(params[2]))
            print(res)

    if (command == 'parse'):
        if (len(params) == 2):
            parser.parseArchive(params[1])

    if (command == 'close'):
        break
