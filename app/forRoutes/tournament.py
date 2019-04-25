from app.forms import TournamentForm
import server.useCasesAPI as useCasesAPI
from server.storage import storage, status
from server.commonFunctions import unixTime

def Tournament(form: TournamentForm) -> list:
    if form.validate_on_submit():
        probId = form.probId.data
        startTimeStr = form.start.data
        id = None
        try:
            id = int(probId)
            if storage.getProblem(id) == None:
                raise ValueError()
        except ValueError:
            return [0, "No problem with this id!"]
        if (startTimeStr == ''):
            while (status.RunningTournament()):
                pass
            status.tournamentStarted(id)
            useCasesAPI.tournament(id)
            status.tournamentStopped(id)
            return [1, "Tournament Successfully created."]
        else:
            try:
                startTime = int(startTimeStr)
            except ValueError:
                return [0, "Incorrect time"]
            if (startTime < unixTime()):
                return [0, "Too early"]
            problem = storage.getProblem(id)
            problem.nextTournament = startTime
            storage.saveProblem(problem)
            return [1, "Looking forward for tournament start"]
    return [0, "Enter id of problem."]

