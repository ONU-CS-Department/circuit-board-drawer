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
        # Button-1
        #self.bind('<Motion>', self.motion) # bind mouse motion to
        self.curX = -1
        self.curY = -1
        self.bind('<Button-1>', self.click) # bind mouse motion to
        self.pack(fill="both", expand=True)

    def drawLine(self, x0, y0, x1, y1, lineIsVertical=False):
        self.create_line(x0, y0, x1, y1, fill=config["wire_color"], width=6)
        if lineIsVertical:
            vOffset = 8; hOffset = 0
        else:
            vOffset = 0; hOffset = 8
        #print(self.getLineAngle(x0, y0, x1, y1))
        lineAngle = self.getLineAngle(x0, y0, x1, y1)
        print(self.getLineDirection(x0, y0, x1, y1, lineAngle))
        if config["has_start_node"]:
            self.create_oval(x0-vOffset, y0-hOffset, x0+8-(hOffset*3), y0-16+(hOffset*3), width=6, outline=config["wire_color"])
        if config["has_end_node"]:
            self.create_oval(x1-vOffset, y1-hOffset, x1+8+hOffset, y1+16-hOffset, width=6, outline=config["wire_color"])
        if config["has_start_module"]:
            self.create_rectangle(x0-(2*vOffset), y0-(2*hOffset), x0+14-(3.75*hOffset), y0-16+(3.75*hOffset), outline=config["wire_color"], fill=config["wire_color"])
        if config["has_end_module"]:
            self.create_rectangle(x1-(vOffset*1.75), y1-(hOffset*1.75), x1+14+(hOffset/4), y1+16-(hOffset/4), outline=config["wire_color"], fill=config["wire_color"])

    def click(self, event):
        x, y = event.x, event.y
        if self.curX == -1:
            self.curX = x
            self.curY = y
        else:
            self.drawLine(self.curX, self.curY, x, y)
            self.curX = -1
            self.curY = -1

    def getLineAngle(self, x0, y0, x1, y1):
        if (x0 == x1):
            return 180.0
        return degrees(atan((y1-y0)/(x1-x0)))
    # 0, 1, 2, 3 for up, right, down, left
    def getLineDirection(self, x0, y0, x1, y1, angle):
        if ((y0 > y1) & (angle >= 0) & (angle <= 45.0)):
            return 3
        if ((y0 < y1) & (angle < 0) & (angle >= -45.0)):
            return 3
        return 0
        

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

root = tk.Tk()
root.title("Computer Sciece Department Graphic")
app = Application(master=root)
second_win = tk.Toplevel(root)
second_win.title("Settings")
app2 = Settings(second_win)

root.mainloop()
