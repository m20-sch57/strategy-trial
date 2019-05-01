from app.forms import AddProblemForm
from server.parser import parseArchive
import os
from server.commonFunctions import printToFile

def AddProblem(form: AddProblemForm) -> list:
    if form.validate_on_submit():
        archiveName = "./.tmp.new_problem.zip"
        arch = form.selectfile.data
        arch.save(archiveName)
        dictRes = parseArchive(archiveName)
        os.remove(archiveName)
        if (dictRes['ok'] == 0):
            return [0, (dictRes['error'], 'message red')]
        else:
            return [1, ("Problem successfully added", 'message green')]
    return [0, ("", 'message blue')]
