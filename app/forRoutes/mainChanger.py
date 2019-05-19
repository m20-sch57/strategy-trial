from app.forRoutes.info import info
import server.useCasesAPI as useCasesAPI

def applyChange(request):
    Info = info()
    try:
        chSubId = int(request.args.get('chSubId'))
        ret = useCasesAPI.changeMainSubmission(Info['id'], chSubId)
        return ret
    except:
        return -1
