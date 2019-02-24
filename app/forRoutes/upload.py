import os
import server.storage as storage
from app.forms import ProblemsetID
from werkzeug import secure_filename
from server.useCasesAPI import addSubmission

def Upload(form: ProblemsetID) -> str:
    if form.validate_on_submit():
        f = form.selectfile.data
        #TODO: not save! but AddSubmission 
        f.save(os.path.join(form.selectfile.data.filename))
        return 'Your submission succesfully saved'
    return ''
