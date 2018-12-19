def readFile(path):
    with open(path, 'r') as myfile:
        data = myfile.read()
        return data

def printToFile(text: str, path: str):
    with open(path, 'w') as file:
        file.write(text)
