from server.structures import ProblemState, StrategyState, UserType
from server.structures import User, Rules, Problem, Submission, Tournament
from server.commonFunctions import readFile, printToFile
import os
import shutil
#from app.forRoutes.hash import keygen

try:
    os.remove('database.db')
except:
    pass

from server.storage import storage
import server.useCasesAPI as useCasesAPI

#keygen()

StrategyCnt = 10

import server.parser as parser
shutil.make_archive('tic_tac_toe', 'zip', 'tic_tac_toe')
parsingResult = parser.parseArchive('tic_tac_toe.zip')
if (parsingResult['ok'] != 1):
    print("Can't parse archive tic_tac_toe")
    sys.exit(0)

root = User(-1, "root", "123", UserType.Admin, {}, "ROOT", "ROOT") # It's hard coded user, type can't be changed
storage.saveUser(root)

subs = [i for i in range(10)]

for i in range(StrategyCnt):
    user = User(-1, "hlebushek" + str(i), "12345", UserType.Default, {0 : []}, "HLEBUSHEK" + str(i), "HLEBUSHEK")
    storage.saveUser(user)

for i in range(StrategyCnt):
    useCasesAPI.addSubmission(i + 1, 0, readFile("ticTacToeStrategies/st" + str(i + 1) + ".py"))
    useCasesAPI.changeMainSubmission(i + 1, i)

useCasesAPI.addSubmission(0, 0, readFile("ticTacToeStrategies/st1.py"))
useCasesAPI.addSubmission(0, 0, readFile("ticTacToeStrategies/st2.py"))
useCasesAPI.addSubmission(0, 0, readFile("ticTacToeStrategies/st3.py"))
