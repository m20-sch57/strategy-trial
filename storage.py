
import structures

class Storage:
    def load(self, path):
        pass

    def __init__(self, path):
        self.load(path)
        self.users = []
        self.map = {}
        self.problems = []
        self.submissions = []

    def get(self, id, listOfObjects):
        return listOfObjects[id]

    def save(self, obj, listOfObjects):
        if (obj.id == -1):
            obj.id = len(obj)
            listOfObjects.append(obj)
        else:
            listOfObjects[obj.id] = obj

    def getUser(self, id):
        return self.get(id, users)

    def getProblem(self, id):
        return self.get(id, problems)

    def getSubmission(self, id):
        return self.get(id, submissions)

    def getUserByName(self, username):
        id = self.map[username]
        return self.getUser(id)

    def saveUser(self, user):
        self.map[user.username] = user.id
        self.save(user, users)

    def saveProblem(self, problem):
        self.save(problem, problems)

    def saveSubmission(self, submission):
        self.save(submission, submissions)