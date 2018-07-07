import tkinter as tk
from tkinter import Button, Label, Entry, Frame, Checkbutton, Menu, filedialog, TclError
from math import atan2, degrees
import json
from settings import Settings
from config import Config

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
workingFileName = ""

class Application(tk.Canvas):
    def __init__(self, settings=None, master=None):
        super().__init__(master)
        self.settings = settings
        self.config(background=self.settings.get("bgColor"), width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.settings.registerFunction("bgColor", self.refreshBackground)
        self.bind('<Motion>', self.mouseMotion) # bind mouse motion to
        self.curX = -1
        self.curY = -1
        self.bind('<Button-1>', self.click) # bind mouse motion to
        root.bind('<Control-z>', self.undo)      # forward-slash
        menubar = Menu(root)
        menubar.add_command(label="Undo", command=self.undo)
        root.config(menu=menubar)
        self.pack(fill="both", expand=True)
        self.lines = []

    def click(self, event):
        x, y = event.x, event.y
        if self.curX == -1:         # If this is the first click of the line.
            self.curX = x
            self.curY = y
        else:
            self.lines.append(LineGraphic(self, self.curX, self.curY, x, y, self.settings.get("wireColor"), self.settings.get("hasStartNode"), self.settings.get("hasEndNode"), self.settings.get("hasStartModule"), self.settings.get("hasEndModule")))
            self.refreshCanvas()
            if (self.settings.get("isContinuous")):
                self.curX = x
                self.curY = y
            else:
                self.curX = -1
                self.curY = -1

    def refreshBackground(self):
        try:
            self.config(background=self.settings.get("bgColor"), width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        except TclError: pass

    def clearCanvas(self):  # Clear all graphics from the canvas
        self.delete("all")

    def mouseMotion(self, event):   # Triggered every time the mouse moves across the canvas
        if self.curX != -1:         # If the first vertex is already chosen, allow the other vertex to follow the mouse until a click event
            self.refreshCanvas()
            line = LineGraphic(self, self.curX, self.curY, event.x, event.y, self.settings.get("wireColor"), self.settings.get("hasStartNode"), self.settings.get("hasEndNode"), self.settings.get("hasStartModule"), self.settings.get("hasEndModule"))
            line.drawLine(stipple="gray50")

    def openFile(self):
        fileName = filedialog.askopenfilename()
        print(fileName)

    def saveFile(self):
        fileName = filedialog.askopenfilename()
        
        print(fileName)

    def saveFileAs(self):
        fileName = filedialog.asksaveasfilename(filetypes = (("Data File","*.dat"),("all files","*.*")))
        workingFileName = fileName
        self.writeArrayToFile(self.lines, workingFileName)

    def writeArrayToFile(self, array, fileName):
        with open(fileName, 'w+') as outfile:
            json.dump(array, outfile)

    def drawLines(self):            # Draw all graphics to the screen in FIFO order
        for line in self.lines:
            line.drawLine()

    def refreshCanvas(self):        # Clear the canvas and draw the lines
        self.clearCanvas()
        self.drawLines()

    def undo(self, event=None):     # Remove the previously drawn graphic
        #self.saveFileAs()
        if (self.lines):
            self.lines.pop()
            self.refreshCanvas()

class LineGraphic():
    def __init__(self, master, x0, y0, x1, y1, color, hasStartNode=False, hasEndNode=False, hasStartModule=False, hasEndModule=False, stipple=""):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.color = color
        self.hasStartNode = hasStartNode
        self.hasEndNode = hasEndNode
        self.hasStartModule = hasStartModule
        self.hasEndModule = hasEndModule
        self.canvas = master

    def drawLine(self, stipple=""):
        self.canvas.create_line(self.x0, self.y0, self.x1, self.y1, fill=self.color, width=6, stipple=stipple)
        lineDirection = self.getLineDirection()

        nodeSize = 16
        if (stipple != ""): # when node is not transparent
            nodeSize = 19
        
        if self.hasStartNode:
            self.drawVertexShape(self.x0, self.y0, nodeSize, nodeSize, self.getOppositeDirection(lineDirection), "node", stipple)
        if self.hasEndNode:
            self.drawVertexShape(self.x1, self.y1, nodeSize, nodeSize, lineDirection, "node", stipple)
        if self.hasStartModule:
            self.drawVertexShape(self.x0, self.y0, 16, 32, self.getOppositeDirection(lineDirection), "module", stipple)
        if self.hasEndModule:
            self.drawVertexShape(self.x1, self.y1, 16, 32, lineDirection, "module", stipple)

    def drawVertexShape(self, x, y, width, height, direction, shape, stipple=""):
        negator = 1
        if ((direction == 3) | (direction == 0)):
            negator *= -1

        if ((direction == 1) | (direction == 3)):
            x0Diff = 0 * negator
            y0Diff = -1 * width/2 * negator
            x1Diff = height * negator
            y1Diff = width/2 * negator
        else:
            x0Diff = width/2 * negator
            y0Diff = 0 * negator
            x1Diff = -1 * width/2  * negator
            y1Diff = height * negator
        if (shape == "node"): # Returing not for values, but to conserve space on this t-shirt :)
            if (stipple != ""): # create_oval doesn't allow transparency, so we must use "create_polygon" to make 
                self.canvas.create_polygon(x + x0Diff, y + y0Diff,x + x0Diff, y + y1Diff, x + x1Diff, y + y1Diff, x + x1Diff, y + y0Diff, outline=self.color, smooth=1, stipple=stipple, fill=self.color)
            else:
                self.canvas.create_oval(x + x0Diff, y + y0Diff, x + x1Diff, y + y1Diff, width=6, stipple=stipple, outline=self.color)
        else:
            self.canvas.create_rectangle(x + x0Diff, y + y0Diff, x + x1Diff, y + y1Diff, outline=self.color, stipple=stipple, fill=self.color)
        
    def getOppositeDirection(self, lineDirection):
        if (lineDirection == 0):
            return 2
        elif (lineDirection == 1):
            return 3
        elif (lineDirection == 2):
            return 0
        return 1

    # Lines angle is determined by the angle between two vertexes in line
    # Graph quadrant (in direction of circle) ranges: I: 0 to -90 exclusive, II: 90 exclusive to 0, III: 0 to -90 exclusive, IV: 90 exclusive to 0
    def getLineAngle(self):
        atanDegrees = degrees(atan2((self.y1-self.y0),(self.x1-self.x0)))
        if (atanDegrees < 0):
            return abs(atanDegrees)
        return 180 + (180 - atanDegrees)
    
    # 0, 1, 2, 3 for up, right, down, left
    def getLineDirection(self):
        angle = self.getLineAngle()
        if ((angle > 45.0) & (angle < 135.0)):
            return 0
        if ((angle >= 315.0) or ((angle > 0.0) & (angle <= 45.0))):
            return 1
        if ((angle >= 135.0) & (angle <= 225.0)):
            return 3
        return 2

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Computer Sciece Department Graphic")
    settings = Config(bgColor="#005500", wireColor="#C5A953", hasStartNode=False, hasEndNode=False, hasStartModule=False, hasEndModule=False, isContinuous=False)
    app = Application(settings=settings, master=root)
    settingsWindowConfig = tk.Toplevel(root)
    settingsWindowConfig.title("Settings")
    Settings(settings=settings, master=settingsWindowConfig)
    root.mainloop()
