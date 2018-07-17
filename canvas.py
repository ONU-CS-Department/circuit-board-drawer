"""
This module inherits the tkinter Canvas. It presents graphics to the user.
"""
from tkinter import Tk, Canvas, filedialog, TclError
import json
from line_graphic import LineGraphic
from settings import Settings

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

class MainCanvas(Canvas):
    def __init__(self, lines, settings=None):
        """Construct the object

        Keyword arguments:
        lines -- array of "LineGraphic" objects
        settings -- a Config instance (default None)
        """
        super().__init__()
        self.settings = settings
        self.settings.registerFunction("bgColor", self.refreshBackground)
        self.config(background=self.settings.get("bgColor"), width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.bind('<Motion>', self.__mouseMotion) # bind mouse motion to
        self.bind('<Button-1>', self.__click) # bind mouse motion to
        self.pack(fill="both", expand=True)
        self.curX = -1
        self.curY = -1
        self.lines = lines

    def __click(self, event):
        """Add a vertex with each click. If vertex is second one, draw a line. 

        Keyword arguments:
        event -- tkinter click event
        """
        x, y = event.x, event.y
        if self.__isFirstVertex():         # If this is the first click of the line.
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

    def __isFirstVertex(self):
        """Returns true if a given click was the first vertex in drawing a line"""
        return (self.curX == -1)

    def refreshBackground(self):
        """Refresh the background color"""
        try:
            self.config(background=self.settings.get("bgColor"), width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        except TclError: pass

    def __clearCanvas(self):  # Clear all graphics from the canvas
        """Clear all graphics from the canvas"""
        self.delete("all")

    def __mouseMotion(self, event):
        """If the first vertex is already drawn, connect a pseudo-transparent line to the mouse"""
        if not self.__isFirstVertex():
            self.refreshCanvas()
            line = LineGraphic(self.curX, self.curY, event.x, event.y, self.settings.get("wireColor"), self.settings.get("hasStartNode"), self.settings.get("hasEndNode"), self.settings.get("hasStartModule"), self.settings.get("hasEndModule"))
            line.drawLine(canvas=self, stipple="gray50")

    def __drawLines(self):
        """Draw all lines to the screen in FIFO order"""
        for line in self.lines:
            line.drawLine(canvas=self)

    def refreshCanvas(self): 
        """Clear the canvas and draw the lines"""
        self.__clearCanvas()
        self.__drawLines()
