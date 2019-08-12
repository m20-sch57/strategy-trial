#print("s")
import sys
import importlib

sys.stderr.write("spam\n")

strategyPath, gameModule, GameStr, PlayerIdStr = input(), input(), input(), input()
sys.stderr.write('\n'.join((sys.path))+'\n')

#print("p")

game = importlib.import_module(gameModule)
strategy = importlib.import_module(strategyPath)
#print("i")

gameState = game.GameState()
gameState.fromString(GameStr)
#print("cg")

playerId = str(PlayerIdStr)
#print("ci")

turn = strategy.Strategy(game, gameState, int(playerId))
#if type(turn) != classes.Turn:
#    raise TypeError("Invalid Type")
#print("r")

print(turn.toString())
#print("e")

sys.stderr.write("finished\n")
