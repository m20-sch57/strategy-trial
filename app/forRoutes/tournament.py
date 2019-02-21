from app.forms import TournamentForm
import server.useCasesAPI as useCasesAPI

def Tournament(form: TournamentForm) -> list:
    if form.validate_on_submit():
        probId = form.probId.data
        id = None
        try:
            id = int(probId)
        except ValueError:
            return [0, "No problem with this id!"]
        useCasesAPI.tournament(id)
        return [1, "Tournament Successfully created."]
    return [0, "Enter id of problem."]

