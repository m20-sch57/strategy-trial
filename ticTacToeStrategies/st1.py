import random

def Strategy(game, a, b):
    while True:
        i, j = random.randint(0, 2), random.randint(0, 2);
        if (a.a[i][j] == '.'):
            return game.Turn(i, j);
