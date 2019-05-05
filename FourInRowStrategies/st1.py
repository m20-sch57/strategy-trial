import classes

def Strategy(game: gameState, b: int) -> Turn:
    for i in range(7):
        if game.field[i][-1] == '.':
            return Turn(i)

