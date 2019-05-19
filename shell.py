classes = __import__("classes.py")

classesPath, strategyPath, GameStr, PlayerIdStr = input().split("\n")
game = classes.GameState()
game.fromString(GameStr)


