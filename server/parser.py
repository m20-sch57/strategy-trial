from server.structures import Problem, Rules
from zipfile import ZipFile
from enum import IntEnum
from server.storage import storage
import os
import shutil

SaveFolder = 'tmp'

class FolderType(IntEnum):
    Correct = 0
    OnTheWay = 1
    Bad = 2

FoldersList = ['downloads', 'sources', 'static', 'templates']
FilesList = ['config.json', 'statement']

def getFolderType(path):
    lst = os.listdir(path)
    if (len(lst) == 1 and os.path.isdir(os.path.join(path, lst[0]))):
        return {'type' : FolderType.OnTheWay, 'go' : lst[0]}
    for folder in FoldersList:
        if (not os.path.isdir(os.path.join(path, folder))):
            return {'type' : FolderType.Bad}
    for file in FilesList:
        if (not os.path.isfile(os.path.join(path, file))):
            return {'type' : FolderType.Bad}
    return {'type' : FolderType.Correct}



def parseArchive(archivePath):
    if (not os.path.isfile(archivePath)):
        return {'success' : 0, 'error' : 'No such archive (internal error)'}
    if (os.path.isdir(SaveFolder)):
        shutil.rmtree(SaveFolder)
    zip = ZipFile(archivePath)
    zip.extractall(path = SaveFolder)
    problemPath = SaveFolder

    while (True):
        typeDict = getFolderType(problemPath)
        if (typeDict['type'] == FolderType.Correct):
            break
        elif (typeDict['type'] == FolderType.Bad):
            return {'success' : 0, 'error' : "Archive isn't correct"}
        else:
            problemPath = os.path.join(problemPath, typeDict['go'])

    print(problemPath)

