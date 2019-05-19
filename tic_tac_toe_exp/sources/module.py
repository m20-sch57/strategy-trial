FieldSize = 3

def lineCheck(arr, x0, y0, dx, dy):
    res = arr[x0][y0]
    for i in range(FieldSize - 1):
        if (arr[x0 + dx][y0 + dy] != arr[x0][y0]):
            return '.'
        x0 += dx
        y0 += dy
    return res

def check(full):
    winner = '.'
    for i in range(3):
        winner = lineCheck(full.a, i, 0, 0, 1)
        if (winner != '.'):
            return winner

    for i in range(3):
        winner = lineCheck(full.a, 0, i, 1, 0)
        if (winner != '.'):
            return winner

    winner = lineCheck(full.a, 0, 0, 1, 1)
    if (winner != '.'):
        return winner

    winner = lineCheck(full.a, 0, 3 - 1, 1, -1)
    if (winner != '.'):
        return winner

    return '.'
