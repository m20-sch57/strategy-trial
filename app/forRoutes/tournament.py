from app.forms import TournamentForm
import server.useCasesAPI as useCasesAPI
from server.storage import storage, status

def Tournament(form: TournamentForm) -> list:
    if form.validate_on_submit():
        probId = form.probId.data
        id = None
        try:
            id = int(probId)
            if storage.getProblem(id) == None:
                raise ValueError()
        except ValueError:
            return [0, ("No problem with this id!", 'message red')]
        while (status.RunningTournament()):
            pass
        status.tournamentStarted(id)
        useCasesAPI.tournament(id)
        status.tournamentStopped(id)
        return [1, ("Tournament Successfully created", 'message green')]
    return [0, ("Enter id of problem", 'message blue')]

