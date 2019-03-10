from flask import render_template, make_response, redirect, flash
from app import app
from app.forRoutes.info import info
from app.forms import LoginForm, SignUp
from app.forRoutes.login import Login
from app.forRoutes.sign_up import Sign_up
from app.forRoutes.hash import *

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    success, message, username, userId = Login(form)
    flash(message)
    if success:
        resp = make_response(redirect('/home'))
        resp.set_cookie("all", encrypt("1 " + username + ' ' + str(userId)))
        return resp
    return render_template('login.html.j2', title = "Sign In", form = form, info = info())

@app.route("/sign_up", methods = ["GET", "POST"])
def sign_up():
    form = SignUp()
    success, message = Sign_up(form)
    flash(message)
    if success:
        return redirect("home")
    return render_template('sign_up.html.j2', title = "Sign Up", form = form, info = info())

