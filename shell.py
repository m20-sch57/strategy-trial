#print("s")

import sys

strategyPath, importPathesStr, GameStr, PlayerIdStr = input(), input(), input(), input()

importPathes = importPathesStr.split()
#print("ip")

for path in importPathes:
    sys.path.append(path)
#print("p")

classes = __import__("classes")
strategy = __import__(strategyPath)
#print("i")

game = classes.GameState()
game.fromString(GameStr)
#print("cg")

playerId = str(PlayerIdStr)
#print("ci")

turn = strategy.Strategy(game, playerId)
#if type(turn) != classes.Turn:
#    raise TypeError("Invalid Type")
#print("r")

print(turn.toString())
#print("e")

