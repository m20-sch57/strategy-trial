from flask import request
import server.structures as structures
from server.storage import storage

def unauthorized():
    return {
        'logged_in' : 0,
        'username' : 'Guest',
        'id' : -1
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

    return {
        'logged_in' : logged_in,
        'username' : username,
        'id' : id
    }

def isAdmin() -> bool:
    user = storage.getUserByName(info()[1])
    if user == None:
        return False
    return user.type

