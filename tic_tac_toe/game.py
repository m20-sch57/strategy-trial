from classes import *
from gameStuff import *
from app import app
from flask import render_template

FieldSize = 3
MaxScore = 100
TimeLimit = 1
TurnLimit = 100

class FullGameState:
	def __init__(self):
		self.a = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]

class Logs:
	def __init__(self):
		self.fieldLog = []

	def processResults(self, results):
		pass

	def update(self, a):
		b = a.copy()
		self.fieldLog.append(b)

	def show(self):
		for i in self.fieldLog:
			print(hex(id(i)))
		with app.app_context():
			data = render_template("tmp/logs.html.j2", fieldLog = self.fieldLog)
		return data

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

	winner = lineCheck(full.a, 0, FieldSize - 1, 1, -1)
	if (winner != '.'):
		return winner

	return '.';

def makeTurn(gameState: FullGameState, playerId: int, turn: Turn, logs = None) -> list:
	charList = ['X', 'O']
	if (turn.r < 0 or turn.r >= FieldSize or turn.c < 0 or turn.c >= FieldSize or gameState.a[turn.r][turn.c] != '.'):
		return [TurnState.Incorrect, gameState, nextPlayer(playerId)]
	if (len(logs.fieldLog)):
		print("---------------------------????????????")
		print(logs.fieldLog[0])
		print(gameState.a)
		print(hex(id(logs.fieldLog[0])))
		print(hex(id(gameState.a)))
		gameState.a[turn.r][turn.c] = charList[playerId]
		print(logs.fieldLog[0])
		print(gameState.a)
	if (logs is not None):
		logs.update(gameState.a)
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
