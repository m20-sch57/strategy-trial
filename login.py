import storage
from app.forms import LoginForm

def Login(form: LoginForm) -> list:
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = storage.storage.getUserByName(username)
        if user == None:
            return [0, "There is no registred user with this username", "Guest"]
        if user.password != password:
            return [0, "Incorrect password", "Guest"]
        return [1, "Logged in successfully", username]
    return [0, "", "Guest"]

