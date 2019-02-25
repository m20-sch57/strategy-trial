from app.forRoutes.info import info
from flask import make_response, render_template, redirect, flash, request
from app import app
import server.useCasesAPI as useCasesAPI
import app.forRoutes.mainChanger as mainChanger

@app.route("/settings")
def settings():
    return render_template('settings.html.j2', title = "Settings", info = info())

@app.route("/logout")
def logout():
    resp = make_response(redirect("/home"))
    flash("Logged out successfully")
    resp.set_cookie("logged_in", "0")
    resp.set_cookie("username", "Guest")
    resp.set_cookie("user_id", "-1")
    return resp

@app.route("/submissions")
def submissions():
    mainChanger.applyChange(request)
    
    userId = info()['id']
    if userId == -1:
        flash("You haven't logged in, so you can't see your submissions")
        return redirect('/home')

    lst = useCasesAPI.getSubmissionsU(userId)
    return render_template('submissions.html.j2', title = "Submissions", info = info(), subList = lst[::-1])

