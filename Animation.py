# Animation.py

import random
from Tkinter import *

class Animation(object):
    # Override these methods when creating your own animation
    def mousePressed(self, event): pass
    def mouseMoved(self, event): pass
    def keyPressed(self, event): pass
    def timerFired(self): pass
    def init(self): pass
    def redrawAll(self): pass
    
    def run(self, width=300, height=300):
        # create the root and the canvas
        root = Tk()
        self.width = width
        self.height = height
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()
        def redrawAllWrapper():
            self.canvas.delete(ALL)
            self.redrawAll()
        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()
        def keyPressedWrapper(event):
            self.keyPressed(event)
            redrawAllWrapper()
        def mouseMovedWrapper(event):
            self.mouseMoved(event)
            redrawAllWrapper()
        root.bind("<Button-1>", mousePressedWrapper)
        root.bind("<Key>", keyPressedWrapper)
        root.bind("<Motion>", mouseMovedWrapper)
        self.timerFiredDelay = 250 # milliseconds
        def timerFiredWrapper():
            self.timerFired()
            redrawAllWrapper()
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper)
        self.init()
        timerFiredWrapper()
        root.mainloop()
