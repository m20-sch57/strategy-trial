
import structures
import sqlite3

DatabasePath = 'database.db'

class Storage:
	def __init__(self):
		self.connection = sqlite3.connect(DatabasePath, check_same_thread=False)
		self.cursor = self.connection.cursor()
		structures.createUsersTable(self.cursor)
		structures.createProblemsTable(self.cursor)
		structures.createSubmissionsTable(self.cursor)
		self.connection.commit()

	def getSize(self, tableName):
		self.cursor.execute('SELECT COUNT (*) FROM ' + tableName)
		size = self.cursor.fetchone()
		return size[0]

	def getUsersCount(self):
		return getSize('users')

	def getProblemsCount(self):
		return getSize('problems')

	def getSubmissionsCount(self):
		return getSize('submissions')

	def updateId(self, obj, tableName):
		if (obj.id == -1):
			size = self.getSize(tableName)
			obj.id = size

	def getUser(self, id):
		return structures.getUser(self.cursor, id)

	def getProblem(self, id):
		return structures.getProblem(self.cursor, id)

	def getSubmission(self, id):
		return structures.getSubmission(self.cursor, id)

	def getUserByName(self, username):
		return structures.getUserByName(self.cursor, username)

	def saveUser(self, user):
		self.updateId(user, 'users')
		user.save(self.cursor)
		self.connection.commit()

	def saveProblem(self, problem):
		self.updateId(problem, 'problems')
		problem.save(self.cursor)
		self.connection.commit()

	def saveSubmission(self, submission):
		self.updateId(submission, 'submissions')
		submission.save(self.cursor)
		self.connection.commit()

storage = Storage()
