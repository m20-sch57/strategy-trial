from enum import IntEnum
from server.gameStuff import StrategyVerdict
from server.gameStuff import Result
from server.gameStuff import resultFromStr
from server.commonFunctions import jsonParser
import json


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

    def __init__(self, message):
        Exception.__init__(self)

#database functions

def saveList(cursor, tableName, lst):
    cursor.execute('DELETE FROM ' + tableName + ' WHERE id=?', [lst[0]])
    strArr = '(' + '?, ' * (len(lst) - 1) + '?)'
    cursor.execute('INSERT INTO ' + tableName + ' VALUES ' + strArr, lst)

def getFromDatabase(cursor, tableName, id: int):
    cursor.execute('SELECT * FROM ' + tableName + ' WHERE id=?', [id])
    return cursor.fetchone();

def getCertainField(cursor, tableName, id, fieldName):
    cursor.execute('SELECT ' + fieldName + ' FROM ' + tableName + ' WHERE id=?', [id])
    lst = cursor.fetchone()
    if (lst is None):
        return None
    else:
        return lst[0]


#user
#saving: [id, username, password, type, submissions]

def createUsersTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, 
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

    def save(self, cursor):
        saveList(cursor, 'users', self.getList())

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

def getUser(cursor, id):
    lst = getFromDatabase(cursor, 'users', id)
    if (lst is None):
        return None
    return userFromList(lst)

def getUserByName(cursor, username):
    cursor.execute('SELECT * FROM users WHERE username=?', [username])
    lst = cursor.fetchone()
    if lst == None:
        return None
    return userFromList(lst)

def getAllUsers(cursor):
    cursor.execute("SELECT id, username, type, name, secondname FROM users")
    return cursor.fetchall()

#problem
#saving: [id, name, sources, downloads, statement, submissions, allSubmissions, tournaments, nextTournament]

def createProblemsTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS problems 
        (id integer PRIMARY KEY, name TEXT, sources TEXT, downloads TEXT, statement TEXT, submissions TEXT, allSubmissions TEXT, tournaments TEXT, nextTournament INT)''')

class Rules:
    def __init__(self, Name, Sources, Downloads, statement):
        self.name = Name # title of problem
        self.sources = Sources # list of ["name.py", code: str]
        self.downloads = Downloads # same
        self.statement = statement # text needed to be published (in html)

class Problem:
    def __init__(self, Id, rules, submissions, allSubmissions, tournaments, nextTournament):
        self.id = Id # id of problem
        self.rules = rules # description of rules, interaction with strategy
        self.submissions = submissions # set of main strategies' ids (startegies that will play with each other, selected by user)
        self.allSubmissions = allSubmissions # list of all sent strategies
        self.tournaments = tournaments # standings: sortedby score list of results of all strategies
        self.nextTournament = nextTournament

    def getList(self):
        return [
            self.id, self.rules.name, json.dumps(self.rules.sources),
            json.dumps(self.rules.downloads), self.rules.statement,
            json.dumps(list(self.submissions)), json.dumps(self.allSubmissions),
            json.dumps(self.tournaments), self.nextTournament
        ]

    def save(self, cursor):
        saveList(cursor, 'problems', self.getList())

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
        print("nextTournament: ", self.nextTournament)

def problemFromList(lst):
    return Problem(lst[0], Rules(lst[1], json.loads(lst[2]), json.loads(lst[3]), lst[4]), 
        set(json.loads(lst[5])), json.loads(lst[6]), json.loads(lst[7]), lst[8])

def getProblem(cursor, id):
    lst = getFromDatabase(cursor, 'problems', id)
    if (lst is None):
        return None
    return problemFromList(lst)

def getProblemset(cursor):
    cursor.execute('SELECT id, name FROM problems')
    response = cursor.fetchall()
    return response

#submission
#saving: [id, userId, probId, code, type]

def createSubmissionsTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS submissions (id integer PRIMARY KEY, 
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

    def save(self, cursor):
        saveList(cursor, 'submissions', self.getList())

    def print(self):
        print("id:", self.id)
        print("userId:", self.userId)
        print("probId:", self.probId)
        print("code...")
        print(self.code)
        print("type:", self.type)

def submissionFromList(lst):
    return Submission(lst[0], lst[1], lst[2], lst[3], StrategyState(lst[4]))

def getSubmission(cursor, id):
    lst = getFromDatabase(cursor, 'submissions', id)
    if (lst is None):
        return None
    return submissionFromList(lst)


#tournament
#saving: [id, probId, time, standings]

def createTournamentsTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS tournaments (id integer PRIMARY KEY, 
        probId integer, time integer, standings TEXT)''')

class Tournament:
    def __init__(self, id, probId, time, standings):
        self.id = id
        self.probId = probId
        self.time = time
        self.standings = standings

    def getList(self):
        return [self.id, self.probId, self.time, json.dumps(self.standings)]

    def save(self, cursor):
        saveList(cursor, 'tournaments', self.getList())

    def print(self):
        print("id:", self.id)
        print("probId:", self.probId)
        print("time:", self.time)
        print("standings:", self.standings)

def tournamentFromList(lst):
    return Tournament(lst[0], lst[1], lst[2], json.loads(lst[3]))

def getTournament(cursor, id):
    lst = getFromDatabase(cursor, 'tournaments', id)
    if (lst is None):
        return None
    return tournamentFromList(lst)


#getSumissionLists

def getProblemName(cursor, probId):
    cursor.execute('SELECT name FROM problems WHERE id=?', [probId])
    return cursor.fetchone()[0]

def getSubDict(cursor, subId, probName):
    cursor.execute('SELECT type FROM submissions WHERE id=?', [subId])
    status = cursor.fetchone()[0]
    return {'id' : subId, 'probName' : probName, 'type' : visualize(status)}

def getSubmissionListUP(cursor, userId, probId):
    result = []
    user = getUser(cursor, userId)
    probName = getProblemName(cursor, probId)
    if (probId in user.submissions):
        for subId in user.submissions[probId]:
            result.append(getSubDict(cursor, subId, probName))

    return result

def getSubmissionListU(cursor, userId):
    result = []
    user = getUser(cursor, userId)
    for item in user.submissions.items():
        probId = item[0]
        probName = getProblemName(cursor, probId)
        subList = item[1]
        for subId in subList:
            result.append(getSubDict(cursor, subId, probName))

    return result
