from classes import *

def Strategy(game: GameState, b: int) -> Turn:
    for i in range(7):
        if game.field[i][-1] == '.':
            return Turn(i)

