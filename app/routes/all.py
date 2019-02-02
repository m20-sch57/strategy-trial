from app.forRoutes.info import info
from flask import render_template, redirect
from app import app
from app.forRoutes.problemsetId import problemsetId
from app.forms import ProblemsetID
import useCasesAPI

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
    success, paths = problemsetId(form, strId)
    if not success:
        return redirect("/home")
#    smth with paths...
    return render_template('problem.html.j2', form = form, title = problem.rules.name, problem = problem, subList = subList, info = info())

