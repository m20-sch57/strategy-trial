#print("s")

import sys
import importlib

strategyPath, gameModule, GameStr, PlayerIdStr = input(), input(), input(), input()

#print("p")

game = importlib.import_module(gameModule)
strategy = importlib.import_module(strategyPath)
#print("i")

gameState = game.GameState()
gameState.fromString(GameStr)
#print("cg")

playerId = str(PlayerIdStr)
#print("ci")

turn = strategy.Strategy(gameState, playerId)
#if type(turn) != classes.Turn:
#    raise TypeError("Invalid Type")
#print("r")

print(turn.toString())
#print("e")

