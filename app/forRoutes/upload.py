import server.storage as storage
from app.forms import ProblemsetID
from werkzeug import secure_filename
from server.useCasesAPI import addSubmission
from server.commonFunctions import readFile

def Upload(userId, problemId, form: ProblemsetID) -> str:
    if form.validate_on_submit():
        f = form.selectfile.data
        f.save('upload.py')
        addSubmission(userId, problemId, readFile('upload.py'))
        return 'Your submission succesfully saved'
    return ''
