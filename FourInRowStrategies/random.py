from classes import *
import random

def Strategy(a: GameState, b: int) -> Turn:
    return Turn(random.randint(0, 7))

