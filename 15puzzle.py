# 15puzzle.py
# Lukas Peraza (lbp)
# Aaron Perley (aperley)
#
# For AI Optional Lecture for 15-112 F14

import copy

def swapCells(a, row0, col0, row1, col1):
    a[row0][col0], a[row1][col1] = a[row1][col1], a[row0][col0]

class BoardState(object):
    def __init__(self, board):
        self.board = board
        self.rows, self.cols = len(board), len(board[0])

    # returns list of tuples of (child state, move)
    def getChildStates(self):
        holeRow, holeCol = self.findHole()
        moves = [
            ("L", (0, -1)),
            ("R", (0, +1)),
            ("U", (-1, 0)),
            ("D", (+1, 0))
            ]
        children = []
        for (move, (drow, dcol)) in moves:
            newRow, newCol = holeRow + drow, holeCol + dcol
            if ((0 <= newRow < self.rows) and
                (0 <= newCol < self.cols)):
                newBoard = copy.deepcopy(self.board)
                swapCells(newBoard, holeRow, holeCol, newRow, newCol)
                children.append((BoardState(newBoard), move))
        return children

    def findHole(self):
        for i in xrange(self.rows):
            for j in xrange(self.cols):
                if (self.board[i][j] == 0): return (i, j)
        raise Exception("FUCK YOU")

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

def dfs(state, targetState, moves=[], seen=None):
	if state == targetState:
		return moves

	if seen == None:
		seen = set()
	seen.add(state)

	for childState, move in state.getChildStates():
		if childState in seen: continue
		result = dfs(childState, targetState, moves + [move], seen)
		if result != None:
			return result
	
	return None
