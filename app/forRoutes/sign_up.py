import server.storage as storage
import server.structures as structures
from app.forms import SignUp
import re

def validateUsername(username):
    return (re.fullmatch('[0-9a-zA-Z._-]+', username) is not None)

def Sign_up(form: SignUp) -> list:
    if form.validate_on_submit():
        name = form.name.data
        secondname = form.secondname.data
        username = form.username.data
        password = form.password.data
        passwordRet = form.passwordRet.data
        if (not validateUsername(username)):
            return [0, ("Username is not correct", 'message red')]
        if storage.storage.getUserByName(username) != None:
            return [0, ("There is a user with this username", 'message red')]
        if password != passwordRet:
            return [0, ("Passwords don't match", 'message red')]
        user = structures.User(storage.storage.getUsersCount(), username, password, structures.UserType.Default, {}, name, secondname)
        storage.storage.saveUser(user)
        return [1, ("Signed up successfully", 'message green')]
    return [0, ("You must fill all fields with *", 'message blue')]

