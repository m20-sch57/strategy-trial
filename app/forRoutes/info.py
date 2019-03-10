from flask import request
from server.structures import UserType, SecurityError
from server.storage import storage
from app.forRoutes import *
from app.forRoutes.hash import *

def unauthorized():
    return {
        'logged_in' : 0,
        'username' : 'Guest',
        'id' : -1,
        'admin' : 0
    }

def info() -> list:
    cookies = request.cookies.get("all")
    if cookies == None:
        return unauthorized()
    a = decrypt(cookies).split()
    if len(a) != 4:
        raise SecurityError("You are trying to forge a cookie! YOU GOT BAN!!!")
    loggedInStr, username, strId = a[0], a[1], a[2]
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

    # intUserType = storage.getCertainField('users', id, 'type')
    user = storage.getUser(id)
    if username != user.username and username != "Guest":
        raise SecurityError("You are trying to forge a cookie! YOU GOT BAN!!!")
    userType = user.type #UserType(intUserType)
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
    return info()["admin"]

