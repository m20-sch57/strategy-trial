from server.structures import ProblemState, StrategyState, UserType
from server.structures import User, Rules, Problem, Submission, Tournament
from server.commonFunctions import readFile, printToFile
import os

try:
    os.remove('database.db')
except:
    pass

from server.storage import storage
import server.useCasesAPI as useCasesAPI

StrategyCnt = 10

import server.parser as parser
parser.parseArchive('tic_tac_toe.zip')

subs = [i for i in range(10)]

for i in range(StrategyCnt):
    user = User(-1, "hlebushek" + str(i), "12345", UserType.Default, {0 : [i]})
    storage.saveUser(user)

for i in range(StrategyCnt):
    sub = Submission(-1, i, 0, readFile("ticTacToeStrategies/st" + str(i + 1) + ".py"), StrategyState.Main)
    storage.saveSubmission(sub)

root = User(-1, "test", "123", UserType.Admin, {})
storage.saveUser(root)
useCasesAPI.addSubmission(10, 0, readFile("ticTacToeStrategies/st1.py"))
useCasesAPI.addSubmission(10, 0, readFile("ticTacToeStrategies/st2.py"))
useCasesAPI.addSubmission(10, 0, readFile("ticTacToeStrategies/st3.py"))