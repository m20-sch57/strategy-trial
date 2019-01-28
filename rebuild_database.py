from structures import ProblemState, StrategyState, UserType
from structures import User, Rules, Problem, Submission, Tournament
from commonFunctions import readFile
import os

os.remove('database.db')

from storage import storage

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

rules = Rules("TicTacToe", sources, [], "...")
subs = [i for i in range(10)]

TicTacToe = Problem(-1, rules, set(subs), [])

storage.saveProblem(TicTacToe)

for i in range(StrategyCnt):
    user = User(-1, "hlebushek" + str(i), "12345", UserType.Defalut, {0 : [i]})
    storage.saveUser(user)

for i in range(StrategyCnt):
    sub = Submission(-1, i, 0, readFile("tic_tac_toe/strategies/st" + str(i + 1) + ".py"), StrategyState.Main)
    storage.saveSubmission(sub)
