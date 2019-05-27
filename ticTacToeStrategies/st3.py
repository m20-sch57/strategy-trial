from problems.0.game import *

def Strategy(a: GameState, b: int) -> Turn:
    for i in range(2, -1, -1):
        for j in range(2, -1, -1):
           if (a.a[i][j] == '.'):
                return Turn(i, j);
