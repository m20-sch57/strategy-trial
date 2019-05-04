def getPageId(nextPageForm, prevPageForm, curPageId):
	if (nextPageForm.validate_on_submit()):
		return curPageId + 1
	if (prevPageForm.validate_on_submit()):
		return curPageId - 1
	return None
