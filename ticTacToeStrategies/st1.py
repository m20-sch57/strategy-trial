from problems.0.game import *
import random

def Strategy(a: GameState, b: int) -> Turn:
    while True:
        i, j = random.randint(0, 2), random.randint(0, 2);
        if (a.a[i][j] == '.'):
            return Turn(i, j);
