from app.forms import AddProblemForm
from server.parser import parseArchive
import os
from server.commonFunctions import printToFile
from server.storage import storage

def AddProblem(form: AddProblemForm) -> list:
    if form.validate_on_submit():
        strId = form.probId.data
        if (strId == ""):
            probId = -1
        else:
            try:
                probId = int(strId)
            except ValueError:
                return [0, ("Incorrect problem id", 'message red')]
            if (storage.getProblem(probId) is None):
                return [0, ("Incorrect problem id", 'message red')]
        archiveName = "./.tmp.new_problem.zip"
        arch = form.selectfile.data
        arch.save(archiveName)
        dictRes = parseArchive(archiveName, probId)
        os.remove(archiveName)
        if (dictRes['ok'] == 0):
            return [0, (dictRes['error'], 'message red')]
        else:
            return [1, ("Problemset successfully updated", 'message green')]
    return [0, ("", 'message blue')]
