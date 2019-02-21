from flask import request
import server.structures as structures
from server.storage import storage

def unauthorized():
    return ['0', 'Guest', -1]

def info() -> list:
    logged_in = request.cookies.get("logged_in")
    username = request.cookies.get("username")
    strId = request.cookies.get("user_id")
    if logged_in == None:
        return unauthorized()
    else:
        try:
            id = int(strId)
        except ValueError:
            return unauthorized()

    return [logged_in, username, id]

def isAdmin() -> bool:
    user = storage.getUserByName(info()[1])
    if user == None:
        return False
    return user.type

