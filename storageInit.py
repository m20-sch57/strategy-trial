from structures import *
from commonFunctions import readFile

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
