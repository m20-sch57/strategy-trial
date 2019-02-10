from server.structures import ProblemState, StrategyState, UserType
from server.structures import User, Rules, Problem, Submission, Tournament
from server.commonFunctions import readFile, printToFile
import os

os.remove('database.db')

from server.storage import storage
import server.useCasesAPI as useCasesAPI

StrategyCnt = 10

game = readFile("tic_tac_toe/game.py")
classes = readFile("tic_tac_toe/classes.py")
logsTemplate = readFile("tic_tac_toe/templates/logs.html.j2")
css = readFile("tic_tac_toe/static/style.css")

sources = [
    ['problems/0/game.py', game], 
    ['problems/0/classes.py', classes], 
    ['app/templates/problems/0/logs.html.j2', logsTemplate],
    ['app/static/problems/0/style.css', css]
]

downloads = [
    ['app/downloads/0/classes.py', classes]
]

sources2 = [
    ['problems/1/game.py', game], 
    ['problems/1/classes.py', classes], 
    ['app/templates/problems/1/logs.html.j2', logsTemplate],
    ['app/static/problems/1/style.css', css]
]

downloads2 = [
    ['app/downloads/1/classes.py', classes]
]

statement = readFile("Text/trashST")

rules = Rules("TicTacToe", sources, downloads, statement)
rules2 = Rules("TicTacToe (copy)", sources2, downloads2, statement)
subs = [i for i in range(10)]

TicTacToe = Problem(-1, rules, set(subs), [])
TicTacToe2 = Problem(-1, rules2, {}, [])

storage.saveProblem(TicTacToe)
storage.saveProblem(TicTacToe2)

for i in range(StrategyCnt):
    user = User(-1, "hlebushek" + str(i), "12345", UserType.Default, {0 : [i]})
    storage.saveUser(user)

for i in range(StrategyCnt):
    sub = Submission(-1, i, 0, readFile("tic_tac_toe/strategies/st" + str(i + 1) + ".py"), StrategyState.Main)
    storage.saveSubmission(sub)

root = User(-1, "test", "123", UserType.Admin, {})
storage.saveUser(root)
useCasesAPI.addSubmission(10, 0, readFile("tic_tac_toe/strategies/st1.py"))
useCasesAPI.addSubmission(10, 0, readFile("tic_tac_toe/strategies/st2.py"))
useCasesAPI.addSubmission(10, 0, readFile("tic_tac_toe/strategies/st3.py"))
useCasesAPI.addSubmission(0, 1, readFile("tic_tac_toe/strategies/st1.py"))
useCasesAPI.addSubmission(1, 1, readFile("tic_tac_toe/strategies/st2.py"))
useCasesAPI.addSubmission(2, 1, readFile("tic_tac_toe/strategies/st3.py"))
useCasesAPI.addSubmission(3, 1, readFile("tic_tac_toe/strategies/st4.py"))
useCasesAPI.addSubmission(4, 1, readFile("tic_tac_toe/strategies/st10.py"))
useCasesAPI.changeMainSubmission(0, 13)
useCasesAPI.changeMainSubmission(1, 14)
useCasesAPI.changeMainSubmission(2, 15)
useCasesAPI.changeMainSubmission(3, 16)
useCasesAPI.changeMainSubmission(4, 17)