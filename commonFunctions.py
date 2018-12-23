import json
import os.path

def readFile(path):
	with open(path, 'r') as myfile:
		data = str(myfile.read())
		return data

def createFile(path):
    containingFolderPath = os.path.dirname(path)
    os.makedirs(containingFolderPath, exist_ok = True)

def printToFile(text: str, path: str):
	createFile(path)
	with open(path, 'w') as file:
		file.write(text)

def jsonParser(s):
	s = s.replace("'", "\"")
	return json.loads(s)
