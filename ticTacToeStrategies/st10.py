from problems.0.game import *
import random

FieldSize = 3

def lineCheck(arr, x0, y0, dx, dy):
    res = arr[x0][y0]
    for i in range(FieldSize - 1):
        if (arr[x0 + dx][y0 + dy] != arr[x0][y0]):
            return '.'
        x0 += dx
        y0 += dy
    return res

def check(full: GameState):
    winner = '.'
    for i in range(FieldSize):
        winner = lineCheck(full.a, i, 0, 0, 1)
        if (winner != '.'):
            return winner

    for i in range(FieldSize):
        winner = lineCheck(full.a, 0, i, 1, 0)
        if (winner != '.'):
            return winner

    winner = lineCheck(full.a, 0, 0, 1, 1)
    if (winner != '.'):
        return winner

    winner = lineCheck(full.a, 0, FieldSize - 1, 1, -1)
    if (winner != '.'):
        return winner

    return '.'

def Strategy(a: GameState, b: int) -> Turn:
    charList = ['X', 'O']
    for x in range(50):
        i, j = random.randint(0, 2), random.randint(0, 2)
        if (a.a[i][j] == '.'):
            a.a[i][j] = charList[b]
            if (check(a) == charList[b]):
                return Turn(i, j)
            a.a[i][j] = '.'
    for x in range(50):
        i, j = random.randint(0, 2), random.randint(0, 2)
        if (a.a[i][j] == '.'):
            a.a[i][j] = charList[1 - b]
            if (check(a) == charList[1 - b]):
                return Turn(i, j)
            a.a[i][j] = '.'
    if (a.a[1][1] == '.'):
        return Turn(1, 1)
    while True:
        i, j = random.randint(0, 2), random.randint(0, 2)
        if (a.a[i][j] == '.'):
            return Turn(i, j);
