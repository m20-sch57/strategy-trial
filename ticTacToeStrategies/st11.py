from problems.0.game import *

def check(a: GameState, i: int, j: int) -> bool:
    return a.a[i][j] == '.'

def Strategy(a: GameState, b: int) -> Turn:
   while True:
       i, j = random.randint(0, 2), random.randint(0, 2)
       if check(a, i, j):
           return Turn(i, j)
