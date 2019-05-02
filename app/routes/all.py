from app.forRoutes.info import info
import app.forRoutes.mainChanger as mainChanger
from flask import render_template, redirect, send_file, request, flash, url_for
from app import app
from app.forRoutes.problemsetId import problemsetId
from app.forRoutes.upload import Upload
from app.forms import ProblemsetID
from server.storage import storage
from server.commonFunctions import stringTime
import server.useCasesAPI as useCasesAPI
import server.tester as tester
import server.structures as structures
import json

@app.route("/")
@app.route("/home")
def home():
    title = "ST Home Page"
    return render_template('home.html.j2', title = title, info = info())

@app.route("/problemset")
def problemset():
    title = "Problems"
    problemList = useCasesAPI.getProblemset()
    return render_template('problemset.html.j2', problemList = problemList[::-1], title = title, info = info())

@app.route("/problemset/<strId>", methods = ["GET", "POST"])
def problemset_id(strId):
    mainChanger.applyChange(request)

    form = ProblemsetID()
    success, paths, problem, subList, tourList = problemsetId(strId)
    if not success:
        return redirect("/home")

    userId, problemId = info()['id'], int(strId)
    message = Upload(userId, problemId, form)
    flash(message[0], message[1])

    nextTournamentStrTime = ''
    if (problem.nextTournament != -1):
        nextTournamentStrTime = stringTime(problem.nextTournament)

    nextTournamentStrTime = ''
    if (problem.nextTournament != -1):
        nextTournamentStrTime = stringTime(problem.nextTournament)

    return render_template('problem.html.j2', form = form, title = problem.rules.name, 
        problem = problem, subList = subList[::-1], paths = paths, tourList = tourList, 
        nextTournamentTime = nextTournamentStrTime, info = info())

@app.route("/source/<subId>")
def showSource(subId):
    submission = storage.getSubmission(subId)
    if (submission is None):
        flash('No such submission', 'message red')
        return redirect('/home')
    Info = info()
    title = "Code #" + subId
    if (Info['logged_in'] == 1 and Info['id'] == submission.userId):
        return render_template('source.html.j2', id = subId, code = useCasesAPI.getSubmissionCode(subId), info = info())
    return render_template('message.html.j2', text = "You can't see this source :)", info = info())

@app.route("/download")
def download():
    #TODO if no file redirect home
    return send_file(request.args.get('path'), as_attachment = True)

@app.route("/tournament/<strId>")
def showStandings(strId):
    try:
        tourId = int(strId)
    except ValueError:
        flash('Incorrect tournament id', 'message red')
        return redirect('/home')

    tourDict = useCasesAPI.getTournament(tourId)
    if (tourDict is None):
        flash('Incorrect tournament id', 'message red')
        return redirect('/home')

    title = 'Standings #' + strId
    strtime = stringTime(tourDict['time'])
    probId = storage.getCertainField('tournaments', tourId, 'probId')
    return render_template('standings.html.j2', standings = tourDict['list'],
        time = strtime, probId = probId, title = title, info = info())


#returns page where user can choose which strategies he wants to run
#strId - id of problem (string)
@app.route("/problemset/<strId>/run", methods = ["GET", "POST"])
def runPage(strId):
    if (request.method == 'POST'):
        st1 = request.form.get('st1')
        st2 = request.form.get('st2')
        if ((st1 is not None) and (st2 is not None)):
            return redirect('/test?id1=' + st1 + '&id2=' + st2)

    try:
        probId = int(strId)
        idList = json.loads(storage.getCertainField('problems', probId, 'allSubmissions'))
    except:
        flash('Incorrect problem id', 'message red')
        return redirect('/home')

    probName = storage.getCertainField('problems', probId, 'name')
    subList = []
    for id in idList:
        submission = storage.getSubmission(id)
        subList.append({'id': id, 'username': storage.getCertainField('users', submission.userId, 'username'),
            'probName': probName, 'type': structures.visualize(submission.type)})

    return render_template('runPage.html.j2', subList = subList, probId = probId, info = info(), title = 'Run invocation')
  
@app.route("/test")
def test():
    strId1 = request.args.get('id1')
    strId2 = request.args.get('id2')
    try:
        id1 = int(strId1)
        id2 = int(strId2)
    except (ValueError, TypeError) as error:
        flash('Incorrect strategy id', 'message red')
        return redirect('/home')

    probId1 = storage.getCertainField('submissions', id1, 'probId')
    probId2 = storage.getCertainField('submissions', id2, 'probId')
    if ((probId1 is None) or (probId2 is None) or probId1 != probId2):
        flash('Incorrect pair of strategies', 'message red')
        return redirect('/home')

    title = strId1 + ' vs ' + strId2
    invocationResult = tester.testStrategies(id1, id2, saveLogs = True)
    return invocationResult.logs.show(probId1, {'info': info(), 'title': title})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html.j2', info = info()), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('error500.html.j2'), 500
