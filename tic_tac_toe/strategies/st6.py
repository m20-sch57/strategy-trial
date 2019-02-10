from classes import *

def Strategy(a: GameState, b: int) -> Turn:
    x = 56
    for i in range(1000000000):
        x = (x * 228) % 1337
    return Turn(0, 0)
