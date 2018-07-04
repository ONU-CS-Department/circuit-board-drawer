import tkinter as tk
from tkinter import Button, Label, Entry, LEFT, StringVar, N, S, E, W, Frame, X, Scale, HORIZONTAL
from tkinter.colorchooser import *
from math import atan, degrees

config = {"background_color": "#005500", "wire_color": "#C5A953", "has_start_node": False, "has_end_node": False, "has_start_module": False, "has_end_module": False}
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
class Application(tk.Canvas):
    def __init__(self, master=None):
        super().__init__(master)
        self.config(background=config["background_color"], width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.bind('<Motion>', self.mouseMotion) # bind mouse motion to
        self.curX = -1
        self.curY = -1
        self.bind('<Button-1>', self.click) # bind mouse motion to
        root.bind('<Control-z>', self.undo)      # forward-slash
        self.pack(fill="both", expand=True)
        self.lines = []

    def click(self, event):
        x, y = event.x, event.y
        if self.curX == -1:
            self.curX = x
            self.curY = y
        else:
            # color, hasStartNode=False, hasEndNode=False, hasStartModule=False, hasEndModule=False
            self.lines.append(LineGraphic(self, self.curX, self.curY, x, y, config["wire_color"], config["has_start_node"], config["has_end_node"], config["has_start_module"], config["has_end_module"]))
            self.refreshCanvas()
            self.curX = -1
            self.curY = -1

    def clearCanvas(self):
        self.delete("all")

    def mouseMotion(self, event):
        if self.curX != -1:
            print("asdf")
            self.refreshCanvas()
            line = LineGraphic(self, self.curX, self.curY, event.x, event.y, config["wire_color"], config["has_start_node"], config["has_end_node"], config["has_start_module"], config["has_end_module"], stipple="gray50")
            line.drawLine()
            self.config(background=config["background_color"], width=WINDOW_WIDTH, height=WINDOW_HEIGHT) # Fixes bug where color trail is left on the canvas
            #self.clearCanvas()
            # draw the line queue
            #self.drawLine(self.curX, self.curY, event.x, event.y)

    def drawLines(self):
        for line in self.lines:
            line.drawLine()

    def refreshCanvas(self):
        self.clearCanvas()
        self.drawLines()

    def undo(self, event):
        if (len(self.lines) > 0):
            self.lines.pop()
            self.refreshCanvas()
        

class Settings(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, columnspan=4)
        Label(self, text = 'Background color:').grid(row = 0, column = 1)
        self.backgroundColorField = StringVar(self, value=config["background_color"])
        self.updateBackgroundColor = self.register(self.backgroundEntryChanged)
        self.backgroundEntry = Entry(self, textvariable=self.backgroundColorField, width=15, validate='all', validatecommand=(self.updateBackgroundColor, '%d', '%S'))
        self.backgroundEntry.grid(row = 0, column = 3)
        self.backgroundColorButton = Button(self, text='     ', command=self.setBackgroundColor, bg=config["background_color"])
        self.backgroundColorButton.grid(row = 0, column = 4)

        Label(self, text = 'Draw color:').grid(row = 1, column = 1)
        self.wireColorField = StringVar(self, value=config["wire_color"])
        self.updateWireColor = self.register(self.wireEntryChanged)
        self.wireEntry = Entry(self, textvariable=self.wireColorField, width=15, validate='all', validatecommand=(self.updateWireColor, '%d', '%S'))
        self.wireEntry.grid(row = 1, column = 3)
        self.wireColorButton = Button(self, text='     ', command=self.setWireColor, bg=config["wire_color"])
        self.wireColorButton.grid(row = 1, column = 4)

        self.addToggleSlider(2, "has_start_node")
        self.addToggleSlider(3, "has_end_node")
        self.addToggleSlider(4, "has_start_module")
        self.addToggleSlider(5, "has_end_module")

    def addToggleSlider(self, row, value):
        Label(self, text = value.replace("_", " ").title()).grid(row = row, column = 1)
        self.scale = Scale(self, from_=0, to=1, orient=HORIZONTAL, showvalue=0, command=lambda label: self.sliderMoved(value)).grid(row=row, column=3)
        self.pack()

    def sliderMoved(self, value):
        config[value] = not config[value]

    def backgroundEntryChanged(self, isInsertion, text):
        if isInsertion == "1":
            config["background_color"] += text
        elif isInsertion == "0":
            config["background_color"] = config["background_color"][:(-1 * len(text))]
        try:
            app.config(background=config["background_color"], width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
            self.backgroundColorButton = Button(self, text='     ', command=self.setBackgroundColor, bg=config["background_color"]).grid(row = 0, column = 4)
        finally:
            return True

    def wireEntryChanged(self, isInsertion, text):
        if isInsertion == "1":
            config["wire_color"] += text
        elif isInsertion == "0":
            config["wire_color"] = config["wire_color"][:(-1 * len(text))]
        try:
            self.wireColorButton = Button(self, text='     ', command=self.setWireColor, bg=config["wire_color"]).grid(row = 1, column = 4)
        finally:
            return True

    def setBackgroundColor(self):
        color = askcolor(config["background_color"])[1]
        if color:
            self.backgroundColorField.set(color)
            config["background_color"] = color
            app.config(background=config["background_color"], width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
            self.backgroundColorButton = Button(self, text='     ', command=self.setBackgroundColor, bg=config["background_color"]).grid(row = 0, column = 4)

    def setWireColor(self):
        color = askcolor(config["wire_color"])[1]
        if color:
            self.wireColorField.set(color)
            config["wire_color"] = color
            self.wireColorButton = Button(self, text='     ', command=self.setWireColor, bg=config["wire_color"]).grid(row = 1, column = 4)

class LineGraphic():
    def __init__(self, master, x0, y0, x1, y1, color, hasStartNode=False, hasEndNode=False, hasStartModule=False, hasEndModule=False, stipple=""):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.color = color
        self.stipple = stipple
        self.hasStartNode = hasStartNode
        self.hasEndNode = hasEndNode
        self.hasStartModule = hasStartModule
        self.hasEndModule = hasEndModule
        self.canvas = master

    def drawLine(self):
        self.canvas.create_line(self.x0, self.y0, self.x1, self.y1, fill=self.color, width=6, stipple=self.stipple)
        lineDirection = self.getLineDirection()
        
        if self.hasStartNode:
            self.drawVertexShape(self.x0, self.y0, 16, 16, self.getOppositeDirection(lineDirection), "node")
        if self.hasEndNode:
            self.drawVertexShape(self.x1, self.y1, 16, 16, lineDirection, "node")
        if self.hasStartModule:
            self.drawVertexShape(self.x0, self.y0, 32, 16, self.getOppositeDirection(lineDirection), "module")
        if self.hasEndModule:
            self.drawVertexShape(self.x1, self.y1, 32, 16, lineDirection, "module")

    def drawVertexShape(self, x, y, width, height, direction, shape):
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
        if (shape == "node"):
            self.canvas.create_oval(x + x0Diff, y + y0Diff, x + x1Diff, y + y1Diff, width=6, outline=self.color) 
        if (shape == "module"):
            self.canvas.create_rectangle(x + x0Diff, y + y0Diff, x + x1Diff, y + y1Diff, outline=self.color, stipple=self.stipple, fill=self.color)
        
    def getOppositeDirection(self, lineDirection):
        #print(lineDirection)
        if (lineDirection == 0):
            return 2
        elif (lineDirection == 1):
            return 3
        elif (lineDirection == 2):
            return 0
        elif (lineDirection == 3):
            return 1

    # Lines angle is determined by the angle between two vertexes in line
    # Graph quadrant (in direction of circle) ranges: I: 0 to -90 exclusive, II: 90 exclusive to 0, III: 0 to -90 exclusive, IV: 90 exclusive to 0
    def getLineAngle(self):
        if (self.x0 == self.x1):
            if (self.y0 == self.y1):
                return -1
            if (self.y0 > self.y1):
                return 90.0
            return 270.0
        if (self.y0 == self.y1):
            if (self.x0 > self.x1):
                return 180.0
            return 0.0
        atanDegrees = degrees(atan((self.y1-self.y0)/(self.x1-self.x0)))

        if (self.y1 < self.y0):
            if (atanDegrees < 0.0):
                return abs(atanDegrees)
            return 90.0 + (90.0 - atanDegrees)
        else:
            if (atanDegrees < 0.0):
                return 180.0 + abs(atanDegrees)
            return 270.0 + (90.0 - atanDegrees)
    
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

root = tk.Tk()
root.title("Computer Sciece Department Graphic")
Application(master=root)
settingsWindowConfig = tk.Toplevel(root)
settingsWindowConfig.title("Settings")
Settings(settingsWindowConfig)

root.mainloop()
