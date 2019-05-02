class GameState:
     def __init__(self):
        self.field = [['.' for i in range(6)] for i in range(7)]

# Field is a list of columns, enumerarted from 0 to 6, from left to right
# each column is a list of cells, enumerated from 0 to 5, from DOWN to UP.
# each sell represents it's state, if it has '.' it's unused.
# In other cases it has 'X' or 'O' that represents it's owner.

class Turn:
    def __init__(self, column):
        self.column = column

