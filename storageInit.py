from structures import *
from commonFunctions import readFile
from storage import *

def init():
	root = User(-1, "root", "secret", [], {})

	TicTacToeGame = readFile("tic_tac_toe/game.py")
	TicTacToeClasses = readFile("tic_tac_toe/classes.py")

	TicTacToeRules = Rules(0, [["game.py", TicTacToeGame], ["classes.py", TicTacToeClasses]], "")
	TicTacToe = Problem(-1, "Tic Tac Toe", TicTacToeRules, ProblemState.Running, 0, 0, [], [])

	storage = Storage("")
	storage.saveUser(root)
	storage.saveProblem(TicTacToe)
	return storage

if (__name__ == '__main__'):
	import tester
	import demoApi

	storage = init()
	while (True):
		query = input().split()
		if (query[0] == 'add'):
			path = query[1]
			addStrategyByPath(storage, path)
		if (query[0] == 'get'):
			id = int(query[1])
			print(getStrategyCode(storage, id))
		if (query[0] == 'test'):
			id1 = int(query[1])
			id2 = int(query[2])
			result = tester.testStrategies(storage, id1, id2)
			print(result[0])
			print(result[1])
