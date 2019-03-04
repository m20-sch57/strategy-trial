from app.forRoutes.info import info
from flask import render_template, redirect, send_file, request
from app import app
from app.forRoutes.problemsetId import problemsetId
from app.forms import ProblemsetID
from server.storage import storage
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
    return render_template('problemset.html', problemList = problemList, title = title, info = info())

@app.route("/problemset/<strId>", methods = ["GET", "POST"])
def problemset_id(strId):
    form = ProblemsetID()
    success, paths, problem, subList = problemsetId(form, strId)
    if not success:
        return redirect("/home")
#    smth with paths...
    return render_template('problem.html.j2', form = form, title = problem.rules.name, problem = problem, subList = subList, paths = paths, info = info())

@app.route("/source/<subId>")
def showSource(subId):
    submission = storage.getSubmission(subId)
    Info = info()
    title = "Code #" + subId
    print(Info)
    if Info[0] and Info[2] == submission.userId:
        return render_template('source.html.j2', id = subId, code = useCasesAPI.getSubmissionCode(subId), info = info())
    return render_template('ban.html.j2', info = info())

@app.route("/download")
def download():
    #TODO if no file redirect home
    return send_file(request.args.get('path'), as_attachment = True)

@app.route("/test")
def test():
    standings = [[1,2,'dfberfvbrf'],[3,4,'dwecwefwe'],[5,6,'sdfvbdjfv'],[7,8,'scvwef'],[9,10,'cvb df f']]
    return render_template('temp.html', standings = standings, info = info())
