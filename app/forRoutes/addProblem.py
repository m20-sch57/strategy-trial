from app.forms import AddProblemForm
from server.parser import parseArchive
import os
from server.commonFunctions import printToFile

def AddProblem(form: AddProblemForm) -> list:
    if form.validate_on_submit():
        archiveName = "./.tmp.new_problem.zip"
        arch = form.selectfile.data
        printToFile(arch, archiveName)
        parseArchive(archiveName)
        os.remove(archiveName)
        return [1, "Problem successfully added"]
    return [0, ""]
