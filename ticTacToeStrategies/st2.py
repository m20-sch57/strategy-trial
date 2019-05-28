def Strategy(game, a, b):
    for i in range(3):
        for j in range(3):
            if (a.a[i][j] == '.'):
                return game.Turn(i, j);
