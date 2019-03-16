import server.useCasesAPI as useCasesAPI


def changeType(request):
    strUserId = request.args.get("chUserId")
    if strUserId == None:
        return ""
    try:
        userId = int(strUserId)
    except:
        return "Id must be an integer"
    return useCasesAPI.changeUserType(userId)

