from enum import IntEnum
from gameStuff import StrategyVerdict
from gameStuff import Result
from gameStuff import resultFromStr
from commonFunctions import jsonParser
import json


#additional structures

class ProblemState(IntEnum):
    Running = 0
    Upsolving = 1
    Testing = 2

class StrategyState(IntEnum):
    Main = 0
    NonMain = 1


#database functions

def saveList(cursor, tableName, lst):
    cursor.execute('DELETE FROM ' + tableName + ' WHERE id=?', [lst[0]])
    strArr = '(' + '?, ' * (len(lst) - 1) + '?)'
    cursor.execute('INSERT INTO ' + tableName + ' VALUES ' + strArr, lst)

def getFromDatabase(cursor, tableName, id: int):
    cursor.execute('SELECT * FROM ' + tableName + ' WHERE id=?', [id])
    return cursor.fetchone();


#user
#saving: [id, username, password, submissions]

def createUsersTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, 
        username TEXT, password TEXT, submissions TEXT)''')

class User:
    def __init__(self, Id, username, password, submissions):
        self.id = Id # id of user
        self.username = username # username of user
        self.password = password # password of user
        self.submissions = submissions # dictionary {problemId : list of submissions}

    def getList(self):
        return [self.id, self.username, self.password, str(self.submissions)]

    def save(self, cursor):
        lst = self.getList()
        saveList(cursor, 'users', self.getList())

def userFromList(lst):
    return User(lst[0], lst[1], lst[2], json.dumps(lst[3]))

def getUser(cursor, id):
    lst = getFromDatabase(cursor, 'users', id)
    return userFromList(lst)

def getUserByName(cursor, username):
    cursor.execute('SELECT * FROM users WHERE username=?', [username])
    lst = cursor.fetchone()
    if lst == None:
        return None
    return userFromList(lst)


#problem
#saving: [id, name, sources, downloads, statement, submissions, tournaments]

def createProblemsTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS problems 
        (id integer PRIMARY KEY, name TEXT, sources TEXT, downloads TEXT, statement TEXT, submissions TEXT, tournaments TEXT)''')

class Rules:
    def __init__(self, Name, Sources, Downloads, statement):
        self.name = Name # title of problem
        self.sources = Sources # list of ["name.py", code: str]
        self.downloads = Downloads # same
        self.statement = statement # text needed to be published (in html)

class Problem:
    def __init__(self, Id, rules, submissions, tournaments):
        self.id = Id # id of problem
        self.rules = rules # description of rules, interaction with strategy
        self.submissions = submissions # list of strategies' ids (startegies that will play with each other, selected by user)
        self.tournaments = tournaments # standings: sortedby score list of results of all strategies

    def getList(self):
        return [
            self.id, self.rules.name, json.dumps(self.rules.sources),
            json.dumps(self.rules.downloads), self.rules.statement,
            json.dumps(self.submissions), json.dumps(self.tournaments)
        ]

    def save(self, cursor):
        saveList(cursor, 'problems', self.getList())

def problemFromList(lst):
    return Problem(lst[0], Rules(lst[1], json.loads(lst[2]), json.loads(lst[3]), lst[4]), 
        json.loads(lst[5]), json.loads(lst[6]))

def getProblem(cursor, id):
    lst = getFromDatabase(cursor, 'problems', id)
    return problemFromList(lst)


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

def submissionFromList(lst):
    return Submission(lst[0], lst[1], lst[2], lst[3], StrategyState(lst[4]))

def getSubmission(cursor, id):
    lst = getFromDatabase(cursor, 'submissions', id)
    return submissionFromList(lst)


#tournament
#saving: [id, time, standings]

def createTournamentsTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS tournaments (id integer PRIMARY KEY, 
        t integer, standings TEXT)''')

class Tournament:
    def __init__(self, id, time, standings):
        self.id = id
        self.time = time
        self.standings = standings

    def getList(self):
        return [self.id, self.time, json.dumps(self.standings)]

    def save(self, cursor):
        saveList(cursor, 'tournaments', self.getList())

def tournamentFromList(lst):
    return Tournament(lst[0], lst[1], json.loads(lst[2]))

def getTournament(cursor, id):
    lst = getFromDatabase(cursor, 'tournaments', id)
    return tournamentFromList(lst)
