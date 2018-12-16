def Strategy(a: GameState, b: int) -> Turn:
    while True:
        i, j = random.randint(0, 2), random.randint(0, 2);
        if (a[i][j] == '.'):
            return Turn(i, j);
