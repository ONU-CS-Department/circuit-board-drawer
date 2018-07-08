from tkinter import Tk, Canvas, filedialog, TclError
import json
from lineGraphic import LineGraphic
from settings import Settings

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

class MainCanvas(Canvas):
    def __init__(self, settings=None):
        super().__init__()
        self.settings = settings
        self.settings.registerFunction("bgColor", self.refreshBackground)
        self.config(background=self.settings.get("bgColor"), width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.bind('<Motion>', self.mouseMotion) # bind mouse motion to
        self.bind('<Button-1>', self.click) # bind mouse motion to
        self.pack(fill="both", expand=True)
        self.curX = -1
        self.curY = -1
        self.lines = []

    def click(self, event):
        x, y = event.x, event.y
        if self.isFirstVertex():         # If this is the first click of the line.
            self.curX = x
            self.curY = y
        else:
            self.lines.append(LineGraphic(self.curX, self.curY, x, y, self.settings.get("wireColor"), self.settings.get("hasStartNode"), self.settings.get("hasEndNode"), self.settings.get("hasStartModule"), self.settings.get("hasEndModule")))
            self.refreshCanvas()
            if (self.settings.get("isContinuous")):
                self.curX = x
                self.curY = y
            else:
                self.curX = -1
                self.curY = -1

    def isFirstVertex(self):
        return (self.curX == -1)

    def refreshBackground(self):
        try:
            self.config(background=self.settings.get("bgColor"), width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        except TclError: pass

    def clearCanvas(self):  # Clear all graphics from the canvas
        self.delete("all")

    def mouseMotion(self, event):   # Triggered every time the mouse moves across the canvas
        if not self.isFirstVertex():         # If the first vertex is already chosen, allow the other vertex to follow the mouse until a click event
            self.refreshCanvas()
            line = LineGraphic(self.curX, self.curY, event.x, event.y, self.settings.get("wireColor"), self.settings.get("hasStartNode"), self.settings.get("hasEndNode"), self.settings.get("hasStartModule"), self.settings.get("hasEndModule"))
            line.drawLine(canvas=self, stipple="gray50")

    def drawLines(self):            # Draw all graphics to the screen in FIFO order
        for line in self.lines:
            line.drawLine(canvas=self)

    def refreshCanvas(self):        # Clear the canvas and draw the lines
        self.clearCanvas()
        self.drawLines()

    def undo(self, event=None):     # Remove the previously drawn graphic
        if (self.lines):
            self.lines.pop()
            self.refreshCanvas()
