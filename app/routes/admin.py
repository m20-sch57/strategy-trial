from app.forRoutes.info import info, isAdmin
from flask import render_template, redirect, flash
from app import app
from app.forms import TournamentForm
from app.forRoutes.tournament import Tournament

@app.route("/add_user")
def add_user():
    if not isAdmin():
        flash("You don't have permission to do this!")
        return redirect("/home")
    return render_template('add_user.html', title = "Add user", info = info())

@app.route("/add_problem")
def add_problem():
    if not isAdmin():
        flash("You don't have permission to do this!")
        return redirect("/home")
    return render_template('add_problem.html', title = "Add problem", info = info())

@app.route("/users_list")
def users_list():
    if not isAdmin():
        flash("You don't have permission to do this!")
        return redirect("/home")
    return render_template('users_list.html', title = "Users list", info = info())

@app.route("/add_tournament", methods = ["GET", "POST"])
def add_tournament():
    if not isAdmin():
        flash("You don't have permission to do this!")
        return redirect("/home")
    form = TournamentForm()
    success, message = Tournament(form)
    flash(message)
    if success:
        return redirect("/home")
    return render_template("add_tournament.html", title = "Add tournament", form = form, info = info())

