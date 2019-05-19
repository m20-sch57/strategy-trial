strategyPath, importPathes, GameStr, PlayerIdStr = input().split("\n")

for path in importPathes:
    sys.path.append(path)

classes = __import__("classes")

stategy = __import__("")

game = classes.GameState()
game.fromString(GameStr)

playerId = str(PlayerIdStr)

