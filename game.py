from classes import *
from gameStuff import *

FieldSize = 3
MaxScore = 100
TimeLimit = 1
TurnLimit = 100

class FullGameState:
	a = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]

def gameStateRep(full: FullGameState, playerId: int) -> GameState:
	result = GameState()
	result.a = full.a
	return result

def lineCheck(arr, x0, y0, dx, dy):
	res = arr[x0][y0]
	for i in range(FieldSize - 1):
		if (arr[x0 + dx][y0 + dy] != arr[x0][y0]):
			return '.'
		x0 += dx
		y0 += dy
	return res

def check(full: FullGameState):
	winner = '.'
	for i in range(FieldSize):
		winner = lineCheck(full.a, i, 0, 0, 1)
		if (winner != '.'):
			return winner

	for i in range(FieldSize):
		winner = lineCheck(full.a, 0, i, 1, 0)
		if (winner != '.'):
			return winner

	winner = lineCheck(full.a, 0, 0, 1, 1)
	if (winner != '.'):
		return winner

	winner = lineCheck(full.a, FieldSize - 1, FieldSize - 1, -1, -1)
	if (winner != '.'):
		return winner

	return '.';

def makeTurn(gameState: FullGameState, playerId: int, turn: Turn) -> list:
	charList = ['X', 'O']
	if (gameState.a[turn.r][turn.c] != '.'):
		return [TurnState.Incorrect, gameState, nextPlayer(playerId)]
	gameState.a[turn.r][turn.c] = charList[playerId]
	winner = check(gameState)
	if (winner == '.'):
		dot = 0
		for i in gameState.a:
			for j in i:
				if (j == '.'):
					dot = 1
		if (dot == 1):
			return [TurnState.Correct, gameState, nextPlayer(playerId)]
		else:
			return [TurnState.Last, [Result(MaxScore // 2, StrategyVerdict.Ok), Result(MaxScore // 2, StrategyVerdict.Ok)]]
	else:
		if (winner == 'X'):
			return [TurnState.Last, [Result(MaxScore, StrategyVerdict.Ok), Result(0, StrategyVerdict.Ok)]]
		else:
			return [TurnState.Last, [Result(0, StrategyVerdict.Ok), Result(MaxScore, StrategyVerdict.Ok)]]
