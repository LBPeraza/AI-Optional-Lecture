# 15PuzzleGraphics.py

from Tkinter import *
from Animation import Animation
import puzzle15, random

class Visual15Puzzle(Animation):
    @staticmethod
    def generateShuffle(iters=50):
        i = 0
        shuffles = []
        choices = "LRDU"
        opps = "RLUD"
        while i < iters:
            index = random.randint(0, 3)
            if i == 0 or opps[index] != shuffles[-1]:
                shuffles.append(choices[index])
                i += 1
        return shuffles

    def run(self):
        winSize = self.cellSize * self.size + 2 * self.margin
        self.winSize = winSize
        super(Visual15Puzzle, self).run(winSize, winSize, 80)

    def __init__(self, ai, size=4):
        self.cellSize = 100
        self.margin = 20
        self.state = puzzle15.BoardState.solvedBoard(size)
        self.size = size
        self.ai = ai

    def init(self):
        self.moving = False
        self.moves = []
        self.solved = False

    def timerFired(self):
        if self.moving:
            if self.moves != []:
                move = self.moves.pop(0)
                if not self.state.doMove(move):
                    self.moves.append(random.choice("LRDU"))
            else: self.moving = ""

    def keyPressed(self, event):
        c = event.keysym.lower()
        if self.moving != "solving":
            if c == "r":
                self.moving = "shuffle"
                self.moves += Visual15Puzzle.generateShuffle(10)
            elif c == "s":
                self.moving = "solving"
                self.moves = self.ai(self.state,
                                     puzzle15.BoardState.solvedBoard(self.size))
                if self.moves == None:
                    self.moving = False
                    print("No solution found :(")
            elif c == "right":
                self.state.doMove("L")
            elif c == "left":
                self.state.doMove("R")
            elif c == "up":
                self.state.doMove("D")
            elif c == "down":
                self.state.doMove("U")

    def mousePressed(self, event):
        if not self.moving:
            row, col = self.getCell(event.x, event.y)
            if row == None: return
            hrow, hcol = self.state.findHole()
            drow = hrow - row
            dcol = hcol - col
            if (abs(drow) + abs(dcol) == 1):
                if drow == 1: self.state.doMove("U")
                elif drow == -1: self.state.doMove("D")
                if dcol == 1: self.state.doMove("L")
                elif dcol == -1: self.state.doMove("R")

    def getCell(self, x, y):
        col = (x - self.margin) / self.cellSize
        row = (y - self.margin) / self.cellSize
        if 0 <= row < self.size and 0 <= col < self.size: return row, col
        return None, None

    def drawCell(self, row, col):
        x0, y0 = col*self.cellSize + self.margin, row*self.cellSize + self.margin
        x1, y1 = x0 + self.cellSize, y0+self.cellSize
        color = "white" if self.state.board[row][col] > 0 else "gray"
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        if self.state.board[row][col] != 0:
            cx, cy = (x0+x1)/2, (y0+y1)/2
            self.canvas.create_text(cx, cy, font="Arial 28 bold",
                                    text=self.state.board[row][col])

    def redrawAll(self):
        for row in xrange(self.size):
            for col in xrange(self.size):
                self.drawCell(row, col)

Visual15Puzzle(puzzle15.astar).run()
