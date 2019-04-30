import server.useCasesAPI as useCasesAPI
from app.forRoutes.info import info

def changeType(request):
    strUserId = request.args.get("chUserId")
    if strUserId == None:
        return ("", 'message blue')
    try:
        userId = int(strUserId)
    except:
        return ("Id must be an integer", 'message red')
    Info = info()
    if Info["id"] == userId:
        return ("You don't want to change your type to default!", 'message red')
    return useCasesAPI.changeUserType(userId)

