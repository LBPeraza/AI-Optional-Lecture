# 15puzzle.py
# Lukas Peraza (lbp)
# Aaron Perley (aperley)
#
# For AI Optional Lecture for 15-112 F14

import copy, random

def swapCells(a, row0, col0, row1, col1):
    a[row0][col0], a[row1][col1] = a[row1][col1], a[row0][col0]

class BoardState(object):
    @staticmethod
    def solvedBoard(size):
        board = [[0] * size for _ in xrange(size)]
        for row in xrange(size):
            for col in xrange(size):
                val = (row * size + col) + 1
                board[row][col] = val
        board[size-1][size-1] = 0
        return BoardState(board)

    @staticmethod
    def randomBoard(size, iters=20):
        board = BoardState.solvedBoard(size)
        moves = 0
        dirs = ["L", "R", "U", "D"]
        while moves < iters:
            move = random.choice(dirs)
            if board.doMove(move):
                moves += 1
        return board

    def __init__(self, board):
        self.board = board
        self.rows, self.cols = len(board), len(board[0])
        self.holeRow, self.holeCol = self.findHole()

    # returns list of tuples of (child state, move)
    def getChildStates(self):
        moves = ["L", "R", "U", "D"]
        children = []
        for move in moves:
            newBoardState = BoardState(copy.deepcopy(self.board))
            if (newBoardState.doMove(move)):
                children.append((newBoardState, move))
        return children

    def doMove(self, move):
        holeRow, holeCol = self.findHole()
        drow, dcol = 0, 0
        if "L" in move: dcol -= 1
        elif "R" in move: dcol += 1
        if "U" in move: drow -= 1
        elif "D" in move: drow += 1
        newRow, newCol = holeRow + drow, holeCol + dcol
        if ((0 <= newRow < self.rows) and
            (0 <= newCol < self.cols)):
            swapCells(self.board, holeRow, holeCol, newRow, newCol)
            return True
        return False, None

    def findHole(self):
        for i in xrange(self.rows):
            for j in xrange(self.cols):
                if (self.board[i][j] == 0): return (i, j)
        raise Exception("No hole on board")

    def __eq__(self, other):
        if isinstance(other, BoardState):
            return self.board == other.board
        return False

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

    def __hash__(self):
        return hash(str(self))

    def manhatten(self, other):
        otherPositions = { }
        for row in xrange(other.rows):
            for col in xrange(other.cols):
                otherPositions[other.board[row][col]] = (row, col)

        total = 0
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                value = self.board[row][col]
                otherRow, otherCol = otherPositions[value]
                total += abs(row - otherRow)
                total += abs(col - otherCol)
        return total

import Queue
def bfs(initialState, targetState):
    queue = Queue.Queue()
    queue.put((initialState, []))

    while not queue.empty():
        state, moves = queue.get()
        if state == targetState:
            return moves
        for childState, move in state.getChildStates():
            queue.put((childState, moves + [move]))

    return None

def dfs(state, targetState, maxDepth=5, moves=[], seen=None):
    if maxDepth == 0: return None
    if state == targetState:
        return moves

    if seen == None:
        seen = set()
    seen.add(state)

    for childState, move in state.getChildStates():
        if childState in seen: continue
        result = dfs(childState, targetState, maxDepth-1,
                     moves + [move], seen)
        if result != None:
            return result
    
    return None

def astar(initialState, targetState):
    queue = Queue.PriorityQueue()
    queue.put((initialState.manhatten(targetState),
               initialState, []))
    seen = set()
    while not queue.empty():
        score, state, moves = queue.get()
        if state == targetState:
            return moves
        for childState, move in state.getChildStates():
            if childState not in seen:
                seen.add(childState)
                queue.put((childState.manhatten(targetState),
                           childState, moves + [move]))
    return None
