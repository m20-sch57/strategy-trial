import server.structures as structures
import sqlite3

DatabasePath = 'database.db'

class Storage:
    def __init__(self):
        self.connection = sqlite3.connect(DatabasePath, check_same_thread=False)
        structures.createUsersTable(self.connection)
        structures.createProblemsTable(self.connection)
        structures.createSubmissionsTable(self.connection)
        structures.createTournamentsTable(self.connection)
        structures.createMessagesTable(self.connection)
        self.connection.commit()

    def getSize(self, tableName):
        return structures.execute(self.connection, structures.DatabaseQueryType.Fetchone0,
            'SELECT COUNT (*) FROM ' + tableName)

    def getUsersCount(self):
        return self.getSize('users')

    def getProblemsCount(self):
        return self.getSize('problems')

    def getSubmissionsCount(self):
        return self.getSize('submissions')

    def getTournamentsCount(self):
        return self.getSize('tournaments')

    def getMessagesCount(self):
        return self.getSize('messages')

    def updateId(self, obj, tableName):
        if (obj.id == -1):
            size = self.getSize(tableName)
            obj.id = size

    def getUser(self, id):
        return structures.getUser(self.connection, id)

    def getProblem(self, id):
        return structures.getProblem(self.connection, id)

    def getSubmission(self, id):
        return structures.getSubmission(self.connection, id)

    def getTournament(self, id):
        return structures.getTournament(self.connection, id)

    def getMessage(self, id):
        return structures.getMessage(self.connection, id)

    def getUserByName(self, username):
        return structures.getUserByName(self.connection, username)

    def getProblemByName(self, name):
        return structures.getProblemByName(self.connection, name)

    def getAllUsers(self):
        return structures.getAllUsers(self.connection)

    def saveUser(self, user):
        self.updateId(user, 'users')
        user.save(self.connection)
        self.connection.commit()
        return user.id

    def saveProblem(self, problem):
        self.updateId(problem, 'problems')
        problem.save(self.connection)
        self.connection.commit()
        return problem.id

    def saveSubmission(self, submission):
        self.updateId(submission, 'submissions')
        submission.save(self.connection)
        self.connection.commit()
        return submission.id

    def saveTournament(self, tournament):
        self.updateId(tournament, 'tournaments')
        tournament.save(self.connection)
        self.connection.commit()
        return tournament.id

    def saveMessage(self, message):
        self.updateId(message, 'messages')
        message.save(self.connection)
        self.connection.commit()
        return message.id

    def getProblemset(self):
        response = structures.getProblemset(self.connection)
        dictResponse = [
            {'id' : response[i][0], 'name' : response[i][1]}
            for i in range(len(response))
        ]
        return dictResponse

    def getSubmissionListU(self, userId):
        return structures.getSubmissionListU(self.connection, userId)

    def getSubmissionListUP(self, userId, probId):
        return structures.getSubmissionListUP(self.connection, userId, probId)

    def getCertainField(self, tableName, id, fieldName):
        return structures.getCertainField(self.connection, tableName, id, fieldName)

    def getSubDict(subId, probName):
        return structures.getSubDict(self.connection, subId, probName)

class Status:
    def __init__(self):
        self.runningTournament = False # don't change them manually, call special functions
        self.runningTournamentId = -1
    
    def tournamentStarted(self, tournamentId: int) -> None:
        self.runningTournament = True
        self.runningTournamentId = tournamentId

    def tournamentStopped(self, tournamentId: int) -> None:
        if self.runningTournamentId == tournamentId:
            self.runningTournament = False
            self.runningTournamentId = -1
        else:
            raise ValueError("Invalid tournament Id")

    def RunningTournament(self) -> bool:
        return self.runningTournament

storage = Storage()
status = Status()
