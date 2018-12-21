import json

def readFile(path):
    with open(path, 'r') as myfile:
        data = str(myfile.read())
        return data

def printToFile(text: str, path: str):
    with open(path, 'w') as file:
        file.write(text)

def jsonParser(s):
    print("PARSING")
    print(s)
    s = s.replace("'", "\"")
    return json.loads(s)
