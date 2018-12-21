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
		self.usersCnt = 0
		self.problemsCnt = 0
		self.submissionsCnt = 0

	def updateId(self, obj, tableName):
		#TODO: change to sql query
		if (tableName == 'users'):
			obj.id = self.usersCnt
			self.usersCnt += 1
		if (tableName == 'problems'):
			obj.id = self.problemsCnt
			self.problemsCnt += 1
		if (tableName == 'submissions'):
			obj.id = self.submissionsCnt
			self.submissionsCnt += 1

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
