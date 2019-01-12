from flask import render_template, flash, redirect, make_response, request
from app import app
from app.forms import LoginForm, SignUp, Submit, StrategyTester
import demoAPI
import storage, structures
list_problems = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]

@app.route("/")
@app.route("/home")
def home():
    title = "ST Home Page"
    return render_template('home.html', title = title, info = [request.cookies.get("logged_in"), request.cookies.get("username")])

@app.route("/problemset")
def problemset():
    title = "Problems"
    return render_template('problemset.html', problems = list_problems, title = title, info = [request.cookies.get("logged_in"), request.cookies.get("username")])

@app.route("/problemset/<task_id>")
def problemset_id(task_id):
    if task_id not in list_problems:
        return redirect('/home')
    return render_template('problemset_id.html', title = task_id, task_id = task_id, info = [request.cookies.get("logged_in"), request.cookies.get("username")])

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route("/strategy_tester", methods = ["GET", "POST"])
def strategy_tester():
    form = StrategyTester()
    if form.validate_on_submit():
        id1 = form.id1.data
        id2 = form.id2.data
        return redirect('/test?id1=' + str(id1) + '&id2=' + str(id2))
    return render_template('strategy_tester.html', title = "Strategy Tester", form = form, info = [request.cookies.get("logged_in"), request.cookies.get("username")])

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if storage.storage.getUserByName(username).password == password:
            resp = make_response(redirect('/home'))
            resp.set_cookie("logged_in", '1')
            resp.set_cookie("username", username)
            return resp
        flash("Failed to log in")
    return render_template('login.html', title = "Sign In", form = form, info = [request.cookies.get("logged_in"), request.cookies.get("username")])

@app.route("/logout")
def logout():
    resp = make_response(redirect("/home"))
    resp.set_cookie("logged_in", "0")
    resp.set_cookie("username", "guest")
    return resp

@app.route("/sign_up", methods = ["GET", "POST"])
def sign_up():
    form = SignUp()
    if form.validate_on_submit():
        name = form.name.data
        secondname = form.secondname.data
        username = form.username.data
        password = form.password.data
        passwordRet = form.passwordRet.data
        if storage.storage.getUserByName(username) == None and password == passwordRet:
            user = structures.User(storage.storage.getUsersCount(), username, password, [])
            storage.storage.saveUser(user)
#        remember_me = form.remember_me.data
            return redirect('/home')
        if storage.storage.getUserByName(username) != None:
            flash("There is a user with this username")
            print("username")
        else:
            flash("Passwords don't match")
            print("password")
    return render_template('sign_up.html', title = "Sign Up", form = form, info = [request.cookies.get("logged_in"), request.cookies.get("username")])

@app.route("/test")
def showTestPage():
    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    if (id1 == None or id2 == None):
        return "..."

    invocationResult = demoAPI.judge(id1, id2)
    return invocationResult.logs.show()

@app.route("/source")
def showSource():
    id = request.args.get('id')
    if (id == None):
        return "..."

    return render_template('source.html.j2', id = id, code = demoAPI.getStrategyCode(id), info = [request.cookies.get("logged_in"), request.cookies.get("username")])

    """TODO return!!!!"""

"""#??? and other like /problem/"id_problem"/statement, submit, submissions
t = 9083927398
@app.route("/problem/" + t + "/statement")#???
def statement():
    return None"""

@app.route("/submissions")
def submissions():
    return render_template('submissions.html', title = "Submissions", info = [request.cookies.get("logged_in"), request.cookies.get("username")])

@app.route("/submit", methods = ["GET", "POST"])
def submit():
    form = Submit()
    if form.validate_on_submit():
        text_code = form.textfield.data
        demoAPI.addStrategy(text_code)
        return redirect('/home')
    return render_template('submit.html', title = "Send a task", form = form, info = [request.cookies.get("logged_in"), request.cookies.get("username")])

#__________________________________
#for admin
#__________________________________

@app.route("/add_user")
def add_user():
    if request.cookies.get("username") != "root":
        flash("You don't have permission to do this!")
        return redirect("/home")
    return render_template('add_user.html', title = "Add user", info = [request.cookies.get("logged_in"), request.cookies.get("username")])

@app.route("/add_problem")
def add_problem():
    if request.cookies.get("username") != "root":
        flash("You don't have permission to do this!")
        return redirect("/home")
    return render_template('add_problem.html', title = "Add problem", info = [request.cookies.get("logged_in"), request.cookies.get("username")])

@app.route("/users_list")
def users_list():
    if request.cookies.get("username") != "root":
        flash("You don't have permission to do this!")
        return redirect("/home")
    return render_template('users_list.html', title = "Users list", info = [request.cookies.get("logged_in"), request.cookies.get("username")])

"""@app.route("/edit_user/id_user")
def edit_user():
    return None"""

"""@app.route("/edit_problem/id_problem")
def edit_problem():
    return None"""

