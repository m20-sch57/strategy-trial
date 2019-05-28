def check(a, i: int, j: int) -> bool:
    return a.a[i][j] == '.'

def Strategy(game, a, b):
   while True:
       i, j = random.randint(0, 2), random.randint(0, 2)
       if check(a, i, j):
           return game.Turn(i, j)
