from enum import Enum
from gameStuff import StrategyVerdict
from gameStuff import Result
import json

class ProblemState(Enum):
    Running = 0
    Upsolving = 1
    Testing = 2

class StrategyState(Enum):
    Main = 0
    NonMain = 1

def jsonParser(s):
    s = s.replace("'", "\"")
    return json.loads(s)

# definition of user

class User:
    def __init__(self, Id: int, username: str, password: str, submissions: list, results: dict):
        self.id = Id # id of user
        self.username = username # username of user
        self.password = password # password of user
        self.submissions = submissions # list of user's ids of submissions
        self.results = results # dict prob_id into result of user's strategies

def createUsersTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, username TEXT, password TEXT, submissions TEXT, results TEXT''')

class Rules:
    def __init__(self, ProbId: int, Sources, statement: str):
        self.probId = ProbId # id of problem
        self.sources = Sources #list of ["name.py", code: str]
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

def createProblemsTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS problems (id integer PRIMARY KEY, name TEXT, sources TEXT, statement TEXT, type integer, startTime integer, endTime integer, submissions TEXT, standings TEXT''')


# defination of submission

class Submission:
    def __init__(self, Id: int, UserId: int, ProbId: int, Code: str, ttype: StrategyState, result: Result):
        self.id = Id # id of submission
        self.userId = UserId # id of owner
        self.probId = ProbId # id of problem that it solves
        self.code = Code
        self.type = ttype # type of strategy (e.g. main or nonmain)
        self.result = result # result of strategy

def createSubmissionsTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS submissions (id integer PRIMARY KEY, userId integer, probId integer, code TEXT, type integer, result TEXT''')
