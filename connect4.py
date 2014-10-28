# 15puzzle.py
# Lukas Peraza (lbp)
# Aaron Perley (aperley)
#
# For AI Optional Lecture for 15-112 F14

class Connect4State(object):
    def __init__(self, rows, cols):
        pass

    # 0 = empty, 1 = player 1, 2 = player 2
    # returns [(childState, column)]
    def getChildStates(self, currentPlayer):
        pass

    # high score is better
    def getScore(self, currentPlayer):
        pass

# returns (Connect4State, column) of best move
def minimax(board, player, depth=5, maximizing=True):
    if (depth < 1): raise Exception("minimax error")
    elif (depth == 1):
        return board
    else:
        choice = None
        choiceScore = None
        for childState, column in board.getChildStates():
            