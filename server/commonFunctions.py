import json
import time
import os.path
from datetime import datetime

def readFile(path):
    with open(path, 'r', encoding="utf8") as myfile: #cp1251
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

def unixTime():
    return int(time.time())

def stringTime(unixTime):
    return datetime.utcfromtimestamp(unixTime).strftime(
        '%d %b %Y %I.%M %p')

def problemFolder(probId):
    return "prob" + str(probId)

def splitPath(path):
    path = os.path.normpath(path)
    return path.split(os.sep)
