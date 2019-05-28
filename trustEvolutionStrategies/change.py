def Strategy(game, a, b):
	if (len(a.turns[0]) == 0):
		return game.Turn(0)
	else:
		return game.Turn(a.turns[b ^ 1][-1] ^ 1)
