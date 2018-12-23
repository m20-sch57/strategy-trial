from enum import IntEnum
from gameStuff import StrategyVerdict
from gameStuff import Result
from gameStuff import resultFromStr
from commonFunctions import jsonParser
import json

class ProblemState(IntEnum):
    Running = 0
    Upsolving = 1
    Testing = 2

class StrategyState(IntEnum):
    Main = 0
    NonMain = 1

# definition of user

def saveList(cursor, tableName, lst):
    cursor.execute('DELETE FROM ' + tableName + ' WHERE id=?', [lst[0]])
    strArr = '(' + '?, ' * (len(lst) - 1) + '?)'
    cursor.execute('INSERT INTO ' + tableName + ' VALUES ' + strArr, lst)

def getFromDatabase(cursor, tableName, id):
    cursor.execute('SELECT * FROM ' + tableName + ' WHERE id=?', [id])
    return cursor.fetchone()

class User:
    def __init__(self, Id: int, username: str, password: str, submissions: list, results: dict):
        self.id = Id # id of user
        self.username = username # username of user
        self.password = password # password of user
        self.submissions = submissions # list of user's ids of submissions
        self.results = results # dict prob_id into result of user's strategies

    def getList(self):
        return [self.id, self.username, self.password, str(self.submissions), str(self.results)]

    def save(self, cursor):
        lst = self.getList()
        saveList(cursor, 'users', self.getList())

def userFromList(lst):
    return User(lst[0], lst[1], lst[2], jsonParser(lst[3]), jsonParser(lst[4]))

def getUser(cursor, id):
    lst = getFromDatabase(cursor, 'users', id)
    return userFromList(lst)

def getUserByUsername(cursor, username):
    cursor.execute('SELECT * FROM ' + tableName + ' WHERE username=?', [username])
    lst = cursor.fetchone()
    return userFromList(lst)

def createUsersTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, username TEXT, password TEXT, submissions TEXT, results TEXT)''')

class Rules:
    def __init__(self, ProbId: int, Sources, Templates, statement: str):
        self.probId = ProbId # id of problem
        self.sources = Sources #list of ["name.py", code: str]
        self.templates = Templates #list of ["template.html", code: str]
        self.statement = statement # text needed to be published

# definition of problem

class Problem:
    def __init__(self, Id: int, name: str, rules: Rules, ttype: ProblemState, StartTime: int, EndTime: int, submissions: list, standings: list):
        self.id = Id # id of problem
        self.name = name # name of problem
        self.rules = rules # description of rules, interaction with strategy
        self.type = ttype # type (running/upsolving/testing)
        self.startTime = StartTime # time when users can send strategies
        self.endTime = EndTime # time when users stop sending strategies, time in milliseconds from 01.01.1970
        self.submissions = submissions #list of strategies' ids (startegies that will play with each other, selected by user)
        self.standings = standings # standings: sortedby score list of results of all strategies

    def getList(self):
        return [self.id, self.name, json.dumps(self.rules.sources), json.dumps(self.rules.templates), self.rules.statement, int(self.type),
        self.startTime, self.endTime, str(self.submissions), str(self.standings)]

    def save(self, cursor):
        saveList(cursor, 'problems', self.getList())

def problemFromList(lst):
    return Problem(lst[0], lst[1], Rules(lst[0], json.loads(lst[2]), json.loads(lst[3]), lst[4]), ProblemState(lst[5]), lst[6], lst[7], jsonParser(lst[8]), jsonParser(lst[9]))

def getProblem(cursor, id):
    lst = getFromDatabase(cursor, 'problems', id)
    return problemFromList(lst)

def createProblemsTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS problems (id integer PRIMARY KEY, name TEXT, sources TEXT, templates TEXT, statement TEXT, type integer, startTime integer, endTime integer, submissions TEXT, standings TEXT)''')


# defination of submission

class Submission:
    def __init__(self, Id: int, UserId: int, ProbId: int, Code: str, ttype: StrategyState, result: Result):
        self.id = Id # id of submission
        self.userId = UserId # id of owner
        self.probId = ProbId # id of problem that it solves
        self.code = Code
        self.type = ttype # type of strategy (e.g. main or nonmain)
        self.result = result # result of strategy

    def getList(self):
        return [self.id, self.userId, self.probId, self.code, int(self.type), str(self.result)]

    def save(self, cursor):
        saveList(cursor, 'submissions', self.getList())

def submissionFromList(lst):
    return Submission(lst[0], lst[1], lst[2], lst[3], StrategyState(lst[4]), resultFromStr(lst[5]))

def getSubmission(cursor, id):
    lst = getFromDatabase(cursor, 'submissions', id)
    return submissionFromList(lst)

def createSubmissionsTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS submissions (id integer PRIMARY KEY, userId integer, probId integer, code TEXT, type integer, result TEXT)''')

