def Strategy(game, a, b):
    for i in range(7):
        if a.field[i][-1] == '.':
            return game.Turn(i)

