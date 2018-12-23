from structures import *
from commonFunctions import readFile
import os

os.system('rm database.db')

from storage import *
import demoAPI

def init():
	root = User(-1, "root", "secret", [], {})

	TicTacToeGame = readFile("tic_tac_toe/game.py")
	TicTacToeClasses = readFile("tic_tac_toe/classes.py")
	TicTacToeLogsTemplate = readFile("tic_tac_toe/templates/logs.html.j2")
	TicTacToeCss = readFile("tic_tac_toe/templates/style.css")

	TicTacToeRules = Rules(0, [["game.py", TicTacToeGame], ["classes.py", TicTacToeClasses]], [["logs.html.j2", TicTacToeLogsTemplate], ["style.css", TicTacToeCss]], "")
	TicTacToe = Problem(-1, "Tic Tac Toe", TicTacToeRules, ProblemState.Running, 0, 0, [], [])

	storage.saveUser(root)
	storage.saveProblem(TicTacToe)

	demoAPI.addStrategyByPath("tic_tac_toe/strategies/st1.py")
	demoAPI.addStrategyByPath("tic_tac_toe/strategies/st2.py")

if (__name__ == '__main__'):
	import tester
	import sys

	init()
	lst = sys.stdin.readlines()
	for line in lst:
		query = line.split()
		if (query[0] == 'add'):
			path = query[1]
			demoAPI.addStrategyByPath(path)
		if (query[0] == 'get'):
			id = int(query[1])
			print(demoAPI.getStrategyCode(id))
		if (query[0] == 'test'):
			id1 = int(query[1])
			id2 = int(query[2])
			invocationResult = demoAPI.judge(id1, id2)
			print(invocationResult.results[0])
			print(invocationResult.results[1])
			print(invocationResult.logs.show())
