def getPageId(nextPageForm, prevPageForm, curPageId):
	if (nextPageForm.submit.data):
		return curPageId + 1
	if (prevPageForm.submit.data):
		return curPageId - 1
	return None
