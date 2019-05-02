from classes import *
from random import randint

def Strategy(a: GameState, b: int) -> Turn:
	return Turn(randint(0, 1))	
