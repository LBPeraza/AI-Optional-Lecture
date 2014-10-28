# BoardGame.py

from Tkinter import *
from Animation import Animation
import connect4

def make2dList(rows, cols):
    return [[0]*cols for row in xrange(rows)]


class Connect4(Animation):
    def __init__(self, rows, cols, ai):
        self.cellSize = 100
        self.width, self.height = cols * self.cellSize, rows * self.cellSize
        self.rows, self.cols = rows, cols
        self.state = connect4.Connect4State.new(rows, cols)
        #self.state = connect4.Connect4State([[0, 0, 0, 0, 0, 0, 0],
        #           [0, 0, 0, 0, 0, 0, 0],
        #           [1, 0, 0, 2, 0, 0, 0],
        #           [2, 0, 2, 1, 0, 0, 0],
        #           [2, 0, 1, 1, 0, 0, 0],
        #           [2, 2, 1, 1, 0, 0, 0]])
        self.player = 1
        self.colors = [None, "blue", "red"]
        self.hoverColumn = None
        self.ai = ai
        self.gameOver = False
        self.winner = None

    def run(self):
        super(Connect4, self).run(width=self.width, height=self.height)

    def redrawAll(self):
        #self.canvas.create_rectangle(0, 0, self.width, self.height)
        self.drawBoard()
        if self.gameOver:
            self.canvas.create_text(self.width/2, self.height/2,
                text="Player %d wins!" % self.winner, font="Arial 30 bold")

    def drawBoard(self):
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                self.drawCell(row, col)
        if self.hoverColumn != None:
            self.canvas.create_rectangle(self.hoverColumn * self.cellSize, 0,
                                         (self.hoverColumn + 1) * self.cellSize, self.height,
                                         outline="green")

    def drawCell(self, row, col):
        left, top, right, bottom = self.getCellBounds(row, col)
        self.canvas.create_rectangle(left, top, right, bottom)
        color = self.colors[self.state.board[row][col]]
        if color != None:
            self.canvas.create_oval(left, top, right, bottom, fill=color)

    def getCellBounds(self, row, col):
        return (col * self.cellSize, row * self.cellSize,
                (col + 1) * self.cellSize, (row + 1) * self.cellSize)

    def mouseMoved(self, event):
        if self.player == 1:
            self.hoverColumn = self.getMouseCol(event.x)
        else:
            self.hoverColumn = None

    def mousePressed(self, event):
        if self.gameOver: return
        if self.player != 1: return
        col = self.getMouseCol(event.x)
        if col != None:
            self.state = self.state.makeMove(col, self.player)
            self.checkForWin()
            self.player = self.state.otherPlayer(self.player)

    def getMouseCol(self, x):
        if 0 <= x < self.width:
            col = x / self.cellSize
            if self.state.getRow(col) != None:
                return col
        return None

    def timerFired(self):
        if self.player == 2:
            col = self.ai(self.state, self.player)
            self.state = self.state.makeMove(col, self.player)
            self.checkForWin()
            self.player = self.state.otherPlayer(self.player)

    def checkForWin(self):
        if abs(self.state.getScore(1)) == connect4.WINVALUE:
            self.gameOver = True
            self.winner = 1 if self.state.getScore(1) > 0 else 2

c = Connect4(6, 7, connect4.minimax)
c.run()