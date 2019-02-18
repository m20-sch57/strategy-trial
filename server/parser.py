from server.structures import Problem, Rules
from zipfile import ZipFile

SaveFolder = 'tmp'

def parseArchive(archivePath):
	os.removedirs(SaveFolder)
	zip = ZipFile(archivePath)
	zip.extractall(path = SaveFolder)
	
