from app.forRoutes.info import info
from flask import render_template, redirect, flash
from app import app

@app.route("/add_user")
def add_user():
    if request.cookies.get("username") != "root":
        flash("You don't have permission to do this!")
        return redirect("/home")
    return render_template('add_user.html', title = "Add user", info = info())

@app.route("/add_problem")
def add_problem():
    if request.cookies.get("username") != "root":
        flash("You don't have permission to do this!")
        return redirect("/home")
    return render_template('add_problem.html', title = "Add problem", info = info())

@app.route("/users_list")
def users_list():
    if request.cookies.get("username") != "root":
        flash("You don't have permission to do this!")
        return redirect("/home")
    return render_template('users_list.html', title = "Users list", info = info())

