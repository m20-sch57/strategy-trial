from classes import *

def Strategy(a: GameState, b: int) -> Turn:
	if (len(a.turns[0]) == 0):
		return Turn(0)
	else:
		return Turn(a.turns[b ^ 1][-1] ^ 1)
