import server.useCasesAPI as useCasesAPI
from app.forRoutes.info import info
from app.forRoutes import parser

def sendMessage(form, info):
	if (form.validate_on_submit() and form.submit.data):
		useCasesAPI.createMessage(parser.parser(form.contentField.data), info)
		return 1
	else:
		return 0
