from flask import request
from server.structures import UserType
from server.storage import storage

def unauthorized():
    return {
        'logged_in' : 0,
        'username' : 'Guest',
        'id' : -1,
        'admin' : 0
    }

def info() -> list:
    loggedInStr = request.cookies.get("logged_in")
    username = request.cookies.get("username")
    strId = request.cookies.get("user_id")
    if loggedInStr == None:
        return unauthorized()
    else:
        try:
            id = int(strId)
            logged_in = int(loggedInStr)
        except ValueError:
            return unauthorized()

    if (logged_in == 0):
        return unauthorized()

    intUserType = storage.getCertainField('users', id, 'type')
    userType = UserType(intUserType)
    if (userType == UserType.Admin):
        admin = 1
    else:
        admin = 0

    return {
        'logged_in' : logged_in,
        'username' : username,
        'id' : id,
        'admin' : admin
    }

def isAdmin() -> bool:
    user = storage.getUserByName(info()[1])
    if user == None:
        return False
    return user.type

