from app.forRoutes.info import info
from flask import render_template, redirect, send_file, request, flash
from app import app
from app.forRoutes.problemsetId import problemsetId
from app.forms import ProblemsetID
from server.storage import storage
from server.commonFunctions import stringTime
import server.useCasesAPI as useCasesAPI

@app.route("/")
@app.route("/home")
def home():
    title = "ST Home Page"
    return render_template('home.html', title = title, info = info())

@app.route("/problemset")
def problemset():
    title = "Problems"
    problemList = useCasesAPI.getProblemset()
    return render_template('problemset.html', problemList = problemList[::-1], title = title, info = info())

@app.route("/problemset/<strId>", methods = ["GET", "POST"])
def problemset_id(strId):
    form = ProblemsetID()
    success, paths, problem, subList, tourList = problemsetId(strId)
    if not success:
        return redirect("/home")
#    smth with paths...
    return render_template('problem.html.j2', form = form, title = problem.rules.name, 
        problem = problem, subList = subList[::-1], paths = paths, tourList = tourList, info = info())

@app.route("/source/<subId>")
def showSource(subId):
    submission = storage.getSubmission(subId)
    Info = info()
    title = "Code #" + subId
    if (Info.logged_in == 1 and Info.id == submission.userId):
        return render_template('source.html.j2', id = subId, code = useCasesAPI.getSubmissionCode(subId), info = info())
    return render_template('message.html.j2', text = "You can't see this source :)", info = info())

@app.route("/download")
def download():
    #TODO if no file redirect home
    return send_file(request.args.get('path'), as_attachment = True)

@app.route("/tournament/<strId>")
def test(strId):
    try:
        tourId = int(strId)
    except ValueError:
        flash('Incorrect tournament id')
        return redirect('/home')

    tourDict = useCasesAPI.getTournament(tourId)
    if (tourDict is None):
        flash('Incorrect tournament id')
        return redirect('/home')

    title = 'Standings #' + strId
    strtime = stringTime(tourDict['time'])
    probId = storage.getCertainField('tournaments', tourId, 'probId')
    return render_template('standings.html.j2', standings = tourDict['list'],
        time = strtime, probId = probId, title = title, info = info())
  
