import storage
import structures
from app.forms import SignUp

def Sign_up(form: SignUp) -> list:
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        passwordRet = form.passwordRet.data
        if storage.storage.getUserByName(username) != None:
            print("u")
            return [0, "There is a user with this username"]
        if password != passwordRet:
            print("p")
            return [0, "Passwords don't match"]
        user = structures.User(storage.storage.getUsersCount(), username, password, structures.UserType.Default, {})
        storage.storage.saveUser(user)
        return [1, "Signed up successfully"]
    return [0, ""]

