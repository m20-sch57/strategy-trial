from app.forRoutes.info import info
from flask import make_response, render_template, redirect
from app import app
import server.useCasesAPI as useCasesAPI

@app.route("/settings")
def settings():
    return render_template('settings.html', title = "Settings", info = info())

@app.route("/logout")
def logout():
    resp = make_response(redirect("/home"))
    resp.set_cookie("logged_in", "0")
    resp.set_cookie("username", "Guest")
    resp.set_cookie("user_id", "-1")
    return resp

@app.route("/submissions")
def submissions():
    userId = info()[2]
    if userId == -1:
        return "..."

    lst = useCasesAPI.getSubmissionsU(userId)
    return render_template('submissions.html', title = "Submissions", info = info(), subList = lst)

