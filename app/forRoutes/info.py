from flask import request

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

