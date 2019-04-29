from app.forRoutes.info import info
from flask import make_response, render_template, redirect, flash, request
from app import app
import server.useCasesAPI as useCasesAPI
import app.forRoutes.mainChanger as mainChanger
from app.forRoutes.hash import *
from random import randint
from app.forRoutes.changePassword import ChangePassword
from app.forms import ChangePasswordForm

@app.route("/settings", methods = ["GET", "POST"])
def settings():
    if info()["id"] == -1:
        flash("You haven't logged in, so you can't change your password")
        return redirect("/home")
    form = ChangePasswordForm()
    success, message = ChangePassword(form)
    flash(message)
    if success:
        return redirect("/home")
    return render_template("settings.html.j2", title = "Settings", info = info(), form = form)

@app.route("/logout")
def logout():
    resp = make_response(redirect("/home"))
    flash("Logged out successfully")
    resp.set_cookie("all", encrypt("0 Guest -1 " + str(randint(0, 100000))))
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

