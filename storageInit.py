from structures import *
from commonFunctions import readFile
import os

os.system('rm database.db')

from storage import *
import demoAPI

def init():
	root = User(-1, "root", "secret", [])

	TicTacToeGame = readFile("tic_tac_toe/game.py")
	TicTacToeClasses = readFile("tic_tac_toe/classes.py")
	TicTacToeLogsTemplate = readFile("tic_tac_toe/templates/logs.html.j2")
	TicTacToeCss = readFile("tic_tac_toe/static/style.css")

	TicTacToeRules = Rules(0, [["game.py", TicTacToeGame], ["classes.py", TicTacToeClasses]], [["logs.html.j2", TicTacToeLogsTemplate]], [["style.css", TicTacToeCss]], "")
	TicTacToe = Problem(-1, "Tic Tac Toe", TicTacToeRules, ProblemState.Running, 0, 0, [], [])

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
	demoAPI.tournament()
