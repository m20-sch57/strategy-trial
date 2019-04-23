from server.commonFunctions import unixTime
from server.storage import storage
import server.tester as tester

#runs every second, checks if a turnament should be started
def update():
	time = unixTime()
	problemCnt = storage.getProblemsCount()
	for i in range(problemCnt):
		tourTime = storage.getCertainField('problems', i, 'nextTournament')
		if (tourTime != -1 and tourTime <= time):
			tester.tournament(i)
			prob = storage.getProblem(i)
			prob.nextTournament = -1
			storage.saveProblem(prob)
