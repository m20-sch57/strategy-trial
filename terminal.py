import useCasesAPI
from commonFunctions import readFile
from storage import storage

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
			