from problems.0.game import *

def Strategy(a: GameState, b: int) -> Turn:
    x = 56
    for i in range(10):
        x = (x * 228) % 1337
    return Turn(0, 0)
