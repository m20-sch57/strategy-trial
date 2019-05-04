def getPageId(nextPageForm, prevPageForm, curPageId):
	print(nextPageForm.submit.data)
	print(prevPageForm.submit.data)
	if (nextPageForm.submit.data):
		print("fuck")
		return curPageId + 1
	if (prevPageForm.submit.data):
		print("fuuck")
		return curPageId - 1
	return None
