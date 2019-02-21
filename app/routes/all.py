from app.forRoutes.info import info
from flask import render_template, redirect, send_file, request
from app import app
from app.forRoutes.problemsetId import problemsetId
from app.forms import ProblemsetID
from server.storage import storage
import server.useCasesAPI as useCasesAPI
from datetime import datetime

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
    success, paths, problem, subList = problemsetId(form, strId)
    if not success:
        return redirect("/home")
#    smth with paths...
    return render_template('problem.html.j2', form = form, title = problem.rules.name, problem = problem, subList = subList[::-1], paths = paths, info = info())

@app.route("/source/<subId>")
def showSource(subId):
    submission = storage.getSubmission(subId)
    Info = info()
    title = "Code #" + subId
    print(Info)
    if Info[0] and Info[2] == submission.userId:
        return render_template('source.html.j2', id = subId, code = useCasesAPI.getSubmissionCode(subId), info = info(), title = title)
    return render_template('ban.html.j2', info = info())

@app.route("/download")
def download():
    #TODO if no file redirect home
    return send_file(request.args.get('path'), as_attachment = True)

@app.route("/tournament/<strId>")
def test(strId):
    try:
        tourId = int(strId)
    except ValueError:
        return redirect('/home')

    tourDict = useCasesAPI.getTournament(tourId)
    if (tourDict is None):
        return redirect('/home')

    strtime = datetime.utcfromtimestamp(tourDict['time']).strftime(
        '%d %b %Y %H.%M %p')
    return render_template('standings.html.j2', standings = tourDict['list'],
        time = strtime, info = info())
