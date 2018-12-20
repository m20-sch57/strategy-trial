import structures
import sqlite3

DatabasePath = 'database.db'

class Storage:
	def __init__(self):
		self.connection = sqlite3.connect(DatabasePath)
		self.cursor = self.connection.cursor()
		structures.createUsersTable(self.cursor)
		structures.createProblemsTable(self.cursor)
		structures.createSubmissionsTable(self.cursor)
		self.connection.commit()

	def updateId(self, obj, tableName):
		size = self.cursor.execute('''SELECT COUNT * FROM ''' + tableName)
		if (obj.id == -1):
			obj.id = obj.id = size

	def getUser(self, id):
		return self.get(id, self.users)

	def getProblem(self, id):
		return self.get(id, self.problems)

	def getSubmission(self, id):
		return self.get(id, self.submissions)

	def getUserByName(self, username):
		id = self.map[username]
		return self.getUser(id)

	def saveUser(self, user):
		self.map[user.username] = user.id
		self.save(user, self.users)

	def saveProblem(self, problem):
		self.save(problem, self.problems)

	def saveSubmission(self, submission):
		self.save(submission, self.submissions)

storage = Storage("")