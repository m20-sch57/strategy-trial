from structures import *
from gameStuff import *
from commonFunctions import readFile
import os
from storage import *
import demoAPI

def init():
    code = open("tic_tac_toe/strategies/st1.py", 'r').read()
    subm1 = Submission(0, 0, 0, code, StrategyState.Main, Result())
    root = User(0, "root", "secret", [0])

    TicTacToeGame = readFile("tic_tac_toe/game.py")
    TicTacToeClasses = readFile("tic_tac_toe/classes.py")
    TicTacToeLogsTemplate = readFile("tic_tac_toe/templates/logs.html.j2")
    TicTacToeCss = readFile("tic_tac_toe/static/style.css")

    TicTacToeRules = Rules(0, [["game.py", TicTacToeGame], ["classes.py", TicTacToeClasses]], [["logs.html.j2", TicTacToeLogsTemplate]], [["style.css", TicTacToeCss]], "")
    TicTacToe = Problem(0, "Tic Tac Toe", TicTacToeRules, ProblemState.Running, 0, 0, [], [])

    storage.saveSubmission(subm1)
    storage.saveUser(root)
    storage.saveProblem(TicTacToe)

    demoAPI.addMainStrategyByPath("tic_tac_toe/strategies/st1.py")
    demoAPI.addMainStrategyByPath("tic_tac_toe/strategies/st2.py")
    demoAPI.addMainStrategyByPath("tic_tac_toe/strategies/st3.py")
    demoAPI.addMainStrategyByPath("tic_tac_toe/strategies/st4.py")
    demoAPI.addMainStrategyByPath("tic_tac_toe/strategies/st5.py")
    demoAPI.addMainStrategyByPath("tic_tac_toe/strategies/st6.py")
    demoAPI.addMainStrategyByPath("tic_tac_toe/strategies/st7.py")
    demoAPI.addMainStrategyByPath("tic_tac_toe/strategies/st8.py")
    demoAPI.addMainStrategyByPath("tic_tac_toe/strategies/st9.py")
    demoAPI.addMainStrategyByPath("tic_tac_toe/strategies/st10.py")

if (__name__ == '__main__'):
    init()

    user = storage.getUserByName("root")
    print(user.password)

    demoAPI.tournament()

