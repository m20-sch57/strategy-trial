import server.useCasesAPI as useCasesAPI


def changeType(request):
    strUserId = request.args.get("chUserId")
    try:
        userId = int(strUserId)
    except:
        return "Id must be an integer"
    return useCasesAPI.changeUserType(userId)

