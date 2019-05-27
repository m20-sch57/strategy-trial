from problems.0.game import *

def Strategy(a: GameState, b: int) -> Turn:
    for i in range(3):
        for j in range(3):
            if (a.a[i][j] == '.'):
                return Turn(i, j);
