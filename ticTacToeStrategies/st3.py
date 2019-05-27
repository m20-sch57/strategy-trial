def Strategy(game, a, b):
    for i in range(2, -1, -1):
        for j in range(2, -1, -1):
           if (a.a[i][j] == '.'):
                return game.Turn(i, j);
