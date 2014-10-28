# 15puzzle.py
# Lukas Peraza (lbp)
# Aaron Perley (aperley)
#
# For AI Optional Lecture for 15-112 F14

WINVALUE = 10000

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

# returns column of move which minimizes maximum loss
def minimax(board, player, depth=5):
    state, column, score = minimaxAlgo(board, player, depth)
    return column

# returns (Connect4State, column, score) of best move
def minimaxAlgo(board, player, depth=5, maximizing=True):
    if (depth < 1): raise Exception("minimax error")
    elif (depth == 1):
        return board
    else:
        choice = None
        choiceCol = None
        choiceScore = None
        for childState, column in board.getChildStates():
            childScore = childState.getScore(player)
            if abs(childScore) == WINVALUE:
                return childState, column, childScore
            childScore = minimaxAlgo(board, player, depth-1, not maximizing)
            if (choice == None or
                (maximizing and childScore > choiceScore) or
                (not maximizing and childScore < choiceScore)):
                choice = childState
                choiceCol = column
                choiceScore = childScore
        return choice, choiceCol, choiceScore