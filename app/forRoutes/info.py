from flask import request

def info() -> list:
    logged_in = request.cookies.get("logged_in")
    username = request.cookies.get("username")
    id = request.cookies.get("user_id")
    if logged_in == None:
        logged_in = '0'
        username = "Guest"
        id = -1
    return [logged_in, username, id]

