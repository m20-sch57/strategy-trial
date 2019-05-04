import server.useCasesAPI as useCasesAPI
from app.forRoutes.info import info

def sendMessage(form, info):
	if (form.validate_on_submit() and form.submit.data):
		useCasesAPI.createMessage(form.contentField.data, info)
		return 1
	else:
		return 0
