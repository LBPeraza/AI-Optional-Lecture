# connect4.py
# Lukas Peraza (lbp)
# Aaron Perley (aperley)
#
# For AI Optional Lecture for 15-112 F14

import copy

WINVALUE = 10000

class Connect4State(object):
    def __init__(self, board):
        self.board = board
        self.rows, self.cols = len(self.board), len(self.board[0])

    @classmethod
    def new(cls, rows=6, cols=7):
        return cls([[0]*cols for row in xrange(rows)])

    # 0 = empty, 1 = player 1, 2 = player 2
    # returns [(childState, column)]
    def getChildStates(self, currentPlayer):
        states = []
        for col in xrange(self.cols):
            newState = self.makeMove(col, currentPlayer)
            if newState != None:
                states.append((newState, col))
        return states

    def makeMove(self, col, player):
        row = self.getRow(col)
        if row == None: return None
        newBoard = copy.deepcopy(self.board)
        newBoard[row][col] = player
        return Connect4State(newBoard)


    def getRow(self, col):
        for row in xrange(self.rows-1, -1, -1):
            if self.board[row][col] == 0: return row
        return None

    def otherPlayer(self, player):
        return 2 if player == 1 else 1


    # high score is better
    def getScore(self, currentPlayer):
        myLines = self.countLines(currentPlayer)
        otherLines = self.countLines(self.otherPlayer(currentPlayer))
        if max(myLines) >= 4:
            return WINVALUE
        elif max(otherLines) >= 4:
            return -WINVALUE
        else:
            return sum(myLines) - sum(otherLines) / 2.0

    def countLines(self, player):
        values = []
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                self.countLinesFromCell(row, col, player, values)
        return values


    def countLinesFromCell(self, row, col, player, values):
        dirs = [(-1, -1), (-1, 0), (-1, 1),
                ( 0, -1),          ( 0, 1),
                ( 1, -1), ( 1, 0), ( 1, 1)]
        for drow, dcol in dirs:
            values.append(self.countLineInDirection(row, col, drow, dcol, player))

    def countLineInDirection(self, row, col, drow, dcol, player):
        length = 0
        while ((0 <= row < self.rows) and
               (0 <= col < self.cols) and
               self.board[row][col] == player):
            length += 1
            row += drow
            col += dcol
        return length


    def __str__(self):
        maxWidth = 0
        for row in self.board:
            for val in row:
                maxWidth = max(maxWidth, len(str(val)))
        result = ""
        format = "%%%dd" % (maxWidth+1)
        for row in self.board:
            result += "["
            for i in xrange(self.cols):
                result += format % row[i]
                if (i < self.cols - 1): result += ","
            result += "]\n"
        return result.strip()


# returns column of move which minimizes maximum loss
def minimax(board, player, depth=5):
    maximizing = player == 1
    state, column, score = minimaxAlgo(board, player, depth, maximizing)
    return column

# returns (Connect4State, column, score) of best move
def minimaxAlgo(state, player, depth, maximizing):
    if (depth < 1): raise Exception("minimax error")
    elif (depth == 1):
        return (state, None, state.getScore(1))
    elif (abs(state.getScore(1)) == WINVALUE):
        return (state, None, state.getScore(1))
    else:
        choice = None
        choiceCol = None
        choiceScore = None
        for childState, column in state.getChildStates(player):
            bestState, bestCol, score = minimaxAlgo(childState, childState.otherPlayer(player),
                                            depth-1, not maximizing)
            if (choice == None or
                (maximizing and score > choiceScore) or
                (not maximizing and score < choiceScore)):
                choice = childState
                choiceCol = column
                choiceScore = score
        return choice, choiceCol, choiceScore

"""
s = Connect4State([[0 for col in xrange(7)] for row in xrange(6)])
player = 1

while True:
    if s.getScore(1) == WINVALUE:
        print "You win!"
        break
    elif s.getScore(2) == WINVALUE:
        print "You lost!"
        break
    print s
    print
    if player == 1:
        move = int(raw_input("Enter column: "))
        s = s.makeMove(move, 1)
    else:
        print "Thinking..."
        move = minimax(s, 2)
        s = s.makeMove(move, 2)
    player = s.otherPlayer(player)
"""