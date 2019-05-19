import server.storage as storage
from app.forms import ProblemsetID
# from werkzeug import secure_filename
from server.useCasesAPI import addSubmission
from server.commonFunctions import readFile
import os

def Upload(userId, problemId, form: ProblemsetID) -> str:
    if form.validate_on_submit():
        f = form.selectfile.data
        if f.filename.split('.')[-1] != 'py':
            return [0, ('You can send only python files!', 'message red')]
        if type(f) == str:
            return 'Select file!'
        f.save('upload.py')
        addSubmission(userId, problemId, readFile('upload.py'))
        os.remove("upload.py")
        return [1, ('Your submission succesfully saved', 'message green')]
    return [0, ('', 'message blue')]

