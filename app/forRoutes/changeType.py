import server.useCasesAPI as useCasesAPI
from app.forRoutes.info import info

def changeType(request) -> list:
    strUserId = request.args.get("chUserId")
    if strUserId == None:
        return [0, ("", 'message blue')]
    try:
        userId = int(strUserId)
    except:
        return [0, ("Id must be an integer", 'message red')]
    Info = info()
    if Info["id"] == userId:
        return [0, ("You don't want to change your type to default!", 'message red')]
    return [1, useCasesAPI.changeUserType(userId)]

