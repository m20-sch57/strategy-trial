from app.forms import TournamentForm
import server.useCasesAPI as useCasesAPI
from server.storage import storage
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
            return [0, ("No problem with this id!", "message red")]
        if (startTimeStr == ''):
            useCasesAPI.makeTournament(id)
            return [1, "Tournament Successfully created."]
        else:
            try:
                startTime = int(startTimeStr)
            except ValueError:
                return [0, "Incorrect time", ("message red")]
            if (startTime < unixTime()):
                return [0, ("Too early", "message red")]
            useCasesAPI.createDelayedTournament(id, startTime)
            return [1, ("Looking forward for tournament start", "message green")]
    return [0, ("Enter id of problem", "message blue")]

