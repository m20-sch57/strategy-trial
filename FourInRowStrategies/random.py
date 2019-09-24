import random

def Strategy(game, a, b):
    while True:
        c = random.randint(0, 6)
        if a.field[c][-1] == '.':
            return game.Turn(c)
