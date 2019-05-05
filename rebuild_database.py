from server.structures import ProblemState, StrategyState, UserType
from server.structures import User, Rules, Problem, Submission, Tournament
from server.commonFunctions import readFile, printToFile
import os
import shutil
import sys
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
shutil.make_archive('trust_evolution', 'zip', 'trust_evolution')
shutil.make_archive("FourInRow", "zip", "FourInRow")
parsingResult = parser.parseArchive('tic_tac_toe.zip')
if (parsingResult['ok'] != 1):
    print("Can't parse archive tic_tac_toe")
    sys.exit(0)
parsingResult = parser.parseArchive('trust_evolution.zip')
if (parsingResult['ok'] != 1):
    print("Can't parse archive trust_evolution")
    sys.exit(0)
parsingResult = parser.parseArchive('FourInRow.zip')
if (parsingResult['ok'] != 1):
    print("Can't parse archive trust_evolution")
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
useCasesAPI.addSubmission(1, 1, readFile("trustEvolutionStrategies/st1.py"))
useCasesAPI.addSubmission(2, 1, readFile("trustEvolutionStrategies/st2.py"))
useCasesAPI.addSubmission(3, 1, readFile("trustEvolutionStrategies/copy.py"))
useCasesAPI.addSubmission(4, 1, readFile("trustEvolutionStrategies/change.py"))
useCasesAPI.addSubmission(5, 1, readFile("trustEvolutionStrategies/random.py"))
useCasesAPI.addSubmission(0, 2, readFile("FourInRowStrategies/random.py"))
useCasesAPI.addSubmission(1, 2, readFile("FourInRowStrategies/importError.py"))
useCasesAPI.addSubmission(2, 2, readFile("FourInRowStrategies/st1.py"))
useCasesAPI.changeMainSubmission(1, 13)
useCasesAPI.changeMainSubmission(2, 14)
useCasesAPI.changeMainSubmission(3, 15)
useCasesAPI.changeMainSubmission(4, 16)
useCasesAPI.changeMainSubmission(5, 17)
useCasesAPI.changeMainSubmission(0, 18)
useCasesAPI.changeMainSubmission(1, 19)
useCasesAPI.changeMainSubmission(2, 20)

