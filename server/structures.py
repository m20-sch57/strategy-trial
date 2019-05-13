from enum import IntEnum
from server.gameStuff import StrategyVerdict
from server.gameStuff import Result
from server.gameStuff import resultFromStr
from server.commonFunctions import jsonParser
import json
import threading

#corrcet execute

class DatabaseQueryType(IntEnum):
    Commit = 0
    Fetchall = 1
    Fetchone = 2
    Fetchone0 = 3

lock = threading.Lock()

def execute(connection, queryType, *args):
    try:
        lock.acquire(True)
        cursor = connection.cursor()
        cursor.execute(*args)
        if (queryType == DatabaseQueryType.Commit):
            connection.commit()
        elif (queryType == DatabaseQueryType.Fetchall):
            return cursor.fetchall()
        elif (queryType == DatabaseQueryType.Fetchone):
            return cursor.fetchone()
        elif (queryType == DatabaseQueryType.Fetchone0):
            return cursor.fetchone()[0]
    finally:
        lock.release()

#additional structures

class ProblemState(IntEnum):
    Running = 0
    Upsolving = 1
    Testing = 2

class StrategyState(IntEnum):
    Main = 0
    NonMain = 1

def visualize(strategyState):
    if (strategyState == StrategyState.Main):
        return 'Main'
    else:
        return 'NonMain'

class UserType(IntEnum):
    Default = 0
    Admin = 1

class SecurityError(Exception):
    status_code = 999
    message = ""

    def __init__(self, message):
        self.message = message
        Exception.__init__(self)

#database functions

def saveList(connection, tableName, lst):
    execute(connection, DatabaseQueryType.Commit, 
        'DELETE FROM ' + tableName + ' WHERE id=?', [lst[0]])
    strArr = '(' + '?, ' * (len(lst) - 1) + '?)'
    execute(connection, DatabaseQueryType.Commit, 
        'INSERT INTO ' + tableName + ' VALUES ' + strArr, lst)

def getFromDatabase(connection, tableName, id: int):
    return execute(connection, DatabaseQueryType.Fetchone, 
        'SELECT * FROM ' + tableName + ' WHERE id=?', [id])

def getCertainField(connection, tableName, id, fieldName):
    lst = execute(connection, DatabaseQueryType.Fetchone, 
        'SELECT ' + fieldName + ' FROM ' + tableName + ' WHERE id=?', [id])
    if (lst is None):
        return None
    else:
        return lst[0]


#user
#saving: [id, username, password, type, submissions]

def createUsersTable(connection):
    execute(connection, DatabaseQueryType.Commit, 
        '''CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, 
        username TEXT, password TEXT, type integer, submissions TEXT, name TEXT, secondname TEXT)''')

def toJSON(submissions):
    stringDict = {}
    for sub in submissions.items():
        stringDict[str(sub[0])] = sub[1]
    return json.dumps(stringDict)

def fromJSON(string):
    stringDict = json.loads(string)
    res = {}
    for sub in stringDict.items():
        res[int(sub[0])] = sub[1]
    return res

class User:
    def __init__(self, Id, username, password, userType, submissions, name, secondname):
        self.id = Id # id of user
        self.username = username # username of user
        self.password = password # password of user
        self.type = userType # type of user (Defalut or Admin)
        self.submissions = submissions # dictionary {problemId : list of submissions}
        self.name = name
        self.secondname = secondname

    def getList(self):
        return [self.id, self.username, self.password, int(self.type), 
            toJSON(self.submissions), self.name, self.secondname]

    def save(self, connection):
        saveList(connection, 'users', self.getList())

    def print(self):
        print("id:", self.id)
        print("username:", self.username)
        print("password:", self.password)
        print("type:", self.type)
        print("submissions:", self.submissions)
        print("name:", self.name)
        print("second name:", self.secondname)

def userFromList(lst):
    return User(lst[0], lst[1], lst[2], UserType(lst[3]), fromJSON(lst[4]), lst[5], lst[6])

def getUser(connection, id):
    lst = getFromDatabase(connection, 'users', id)
    if (lst is None):
        return None
    return userFromList(lst)

def getUserByName(connection, username):
    lst = execute(connection, DatabaseQueryType.Fetchone,
        'SELECT * FROM users WHERE username=?', [username])
    if lst == None:
        return None
    return userFromList(lst)

def getAllUsers(connection):
    return execute(connection, DatabaseQueryType.Fetchall,
        "SELECT id, username, type, name, secondname FROM users")

#problem
#saving: [id, name, sources, downloads, statement, submissions, allSubmissions, tournaments, nextTournament]

def createProblemsTable(connection):
    execute(connection, DatabaseQueryType.Commit, 
        '''CREATE TABLE IF NOT EXISTS problems 
        (id integer PRIMARY KEY, name TEXT, sources TEXT, downloads TEXT, 
        statement TEXT, submissions TEXT, allSubmissions TEXT, 
        tournaments TEXT, nextTournament INT, revisionId INT)''')

class Rules:
    def __init__(self, Name, Sources, Downloads, statement):
        self.name = Name # title of problem
        self.sources = Sources # list of ["name.py", code: str]
        self.downloads = Downloads # same
        self.statement = statement # text needed to be published (in html)

class Problem:
    def __init__(self, Id, rules, submissions, allSubmissions, tournaments, nextTournament, revisionId):
        self.id = Id # id of problem
        self.rules = rules # description of rules, interaction with strategy
        self.submissions = submissions # set of main strategies' ids (startegies that will play with each other, selected by user)
        self.allSubmissions = allSubmissions # list of all sent strategies
        self.tournaments = tournaments # standings: sortedby score list of results of all strategies
        self.nextTournament = nextTournament
        self.revisionId = revisionId

    def getList(self):
        return [
            self.id, self.rules.name, json.dumps(self.rules.sources),
            json.dumps(self.rules.downloads), self.rules.statement,
            json.dumps(list(self.submissions)), json.dumps(self.allSubmissions),
            json.dumps(self.tournaments), self.nextTournament, self.revisionId
        ]

    def save(self, connection):
        saveList(connection, 'problems', self.getList())

    def print(self):
        print("id:", self.id)
        print("name:", self.rules.name)
        print("sources...")
        print(self.rules.sources)
        print("downloads...")
        print(self.rules.downloads)
        print("statement:", self.rules.statement)
        print("submissions:", self.submissions)
        print("allSubmissions: ", self.allSubmissions)
        print("tournaments:", self.tournaments)
        print("nextTournament:", self.nextTournament)
        print("revisionId:", self.revisionId)

def problemFromList(lst):
    return Problem(lst[0], Rules(lst[1], json.loads(lst[2]), json.loads(lst[3]), lst[4]), 
        set(json.loads(lst[5])), json.loads(lst[6]), json.loads(lst[7]), lst[8], lst[9])

def getProblem(connection, id):
    lst = getFromDatabase(connection, 'problems', id)
    if (lst is None):
        return None
    return problemFromList(lst)

def getProblemByName(connection, name):
    return execute(connection, DatabaseQueryType.Fetchone,
        'SELECT * FROM problems WHERE name=?', [name])

def getProblemset(connection):
    return execute(connection, DatabaseQueryType.Fetchall,
        'SELECT id, name FROM problems')

#submission
#saving: [id, userId, probId, code, type]

def createSubmissionsTable(connection):
    execute(connection, DatabaseQueryType.Commit,
        '''CREATE TABLE IF NOT EXISTS submissions (id integer PRIMARY KEY, 
        userId integer, probId integer, code TEXT, type integer)''')

class Submission:
    def __init__(self, Id, userId, probId, code, Type):
        self.id = Id # id of submission
        self.userId = userId # id of owner
        self.probId = probId # id of problem that it solves
        self.code = code # code of submission
        self.type = Type # type of strategy (e.g. main or nonmain)

    def getList(self):
        return [self.id, self.userId, self.probId, self.code, int(self.type)]

    def save(self, connection):
        saveList(connection, 'submissions', self.getList())

    def print(self):
        print("id:", self.id)
        print("userId:", self.userId)
        print("probId:", self.probId)
        print("code...")
        print(self.code)
        print("type:", self.type)

def submissionFromList(lst):
    return Submission(lst[0], lst[1], lst[2], lst[3], StrategyState(lst[4]))

def getSubmission(connection, id):
    lst = getFromDatabase(connection, 'submissions', id)
    if (lst is None):
        return None
    return submissionFromList(lst)


#tournament
#saving: [id, probId, probRev, time, standings]

def createTournamentsTable(connection):
    execute(connection, DatabaseQueryType.Commit,
        '''CREATE TABLE IF NOT EXISTS tournaments (id INT PRIMARY KEY, 
        probId INT, probRev INT, time INT, standings TEXT)''')

class Tournament:
    def __init__(self, id, probId, probRev, time, standings):
        self.id = id
        self.probId = probId
        self.probRev = probRev
        self.time = time
        self.standings = standings

    def getList(self):
        return [self.id, self.probId, self.probRev, self.time, json.dumps(self.standings)]

    def save(self, connection):
        saveList(connection, 'tournaments', self.getList())

    def print(self):
        print("id:", self.id)
        print("probId:", self.probId)
        print("probRev:", self.probRev)
        print("time:", self.time)
        print("standings:", self.standings)

def tournamentFromList(lst):
    return Tournament(lst[0], lst[1], lst[2], lst[3], json.loads(lst[4]))

def getTournament(connection, id):
    lst = getFromDatabase(connection, 'tournaments', id)
    if (lst is None):
        return None
    return tournamentFromList(lst)


#message
#saving: [id, userId, time, content]

def createMessagesTable(connection):
    execute(connection, DatabaseQueryType.Commit,
        '''CREATE TABLE IF NOT EXISTS messages (id INT PRIMARY KEY, 
        userId INT, time INT, content TEXT)''')

class Message:
    def __init__(self, id, userId, time, content):
        self.id = id
        self.userId = userId
        self.time = time
        self.content = content

    def getList(self):
        return [self.id, self.userId, self.time, self.content]

    def save(self, connection):
        saveList(connection, 'messages', self.getList())

    def print(self):
        print("id:", self.id)
        print("userId:", self.userId)
        print("time:", self.time)
        print("content:", self.content)

def messageFromList(lst):
    return Message(lst[0], lst[1], lst[2], lst[3])

def getMessage(connection, id):
    lst = getFromDatabase(connection, 'messages', id)
    if (lst is None):
        return None
    return messageFromList(lst)


#getSumissionLists

def getProblemName(connection, probId):
    return execute(connection, DatabaseQueryType.Fetchone0,
        'SELECT name FROM problems WHERE id=?', [probId])

def getSubDict(connection, subId, probName):
    status = execute(connection, DatabaseQueryType.Fetchone0,
        'SELECT type FROM submissions WHERE id=?', [subId])
    return {'id' : subId, 'probName' : probName, 'type' : visualize(status)}

def getSubmissionListUP(connection, userId, probId):
    result = []
    user = getUser(connection, userId)
    probName = getProblemName(connection, probId)
    if (probId in user.submissions):
        for subId in user.submissions[probId]:
            result.append(getSubDict(connection, subId, probName))

    return result

def getSubmissionListU(connection, userId):
    result = []
    user = getUser(connection, userId)
    for item in user.submissions.items():
        probId = item[0]
        probName = getProblemName(connection, probId)
        subList = item[1]
        for subId in subList:
            result.append(getSubDict(connection, subId, probName))

    return result
