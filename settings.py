import tkinter as tk
from tkinter import Button, Label, Entry, LEFT, StringVar, Frame, X, Checkbutton, HORIZONTAL, Menu, filedialog
from tkinter.colorchooser import *

class Settings(tk.Frame):
    def __init__(self, settings=None, master=None):
        super().__init__(master)
        self.grid(row=0, columnspan=4)
        Label(self, text = 'Background color:').grid(row = 0, column = 1)
        self.settings = settings
        self.bgColorField = StringVar(self, value=self.settings.get("bgColor"))
        self.updatebgColor = self.register(self.backgroundEntryChanged)
        self.backgroundEntry = Entry(self, textvariable=self.bgColorField, width=15, validate='all', validatecommand=(self.updatebgColor, '%d', '%S'))
        self.backgroundEntry.grid(row = 0, column = 3)
        self.bgColorButton = Button(self, text='     ', command=self.setBGColor, bg=self.settings.get("bgColor"))
        self.bgColorButton.grid(row = 0, column = 4)

        Label(self, text = 'Draw color:').grid(row = 1, column = 1)
        self.wireColorField = StringVar(self, value=self.settings.get("wireColor"))
        self.updateWireColor = self.register(self.wireEntryChanged)
        self.wireEntry = Entry(self, textvariable=self.wireColorField, width=15, validate='all', validatecommand=(self.updateWireColor, '%d', '%S'))
        self.wireEntry.grid(row = 1, column = 3)
        self.wireColorButton = Button(self, text='     ', command=self.setWireColor, bg=self.settings.get("wireColor"))
        self.wireColorButton.grid(row = 1, column = 4)

        self.addCheckBox(2, "hasStartNode")
        self.addCheckBox(3, "hasEndNode")
        self.addCheckBox(4, "hasStartModule")
        self.addCheckBox(5, "hasEndModule")
        self.addCheckBox(6, "isContinuous")
        
    def addCheckBox(self, row, value):
        Label(self, text = value.replace("_", " ").title() + ":").grid(row = row, column = 1)
        Checkbutton(self, command=lambda: self.toggleProperty(value)).grid(row=row, column=3)

    def toggleProperty(self, value):
        self.settings.set(value, not self.settings.get(value))

    def backgroundEntryChanged(self, isInsertion, text):
        if isInsertion == "1":
            self.settings.set("bgColor", self.settings.get("bgColor") + text)
        elif isInsertion == "0":
            self.settings.set("bgColor", self.settings.get("bgColor")[:(-1 * len(text))])
        try:
            self.bgColorButton = Button(self, text='     ', command=self.setBGColor, bg=self.settings.get("bgColor")).grid(row = 0, column = 4)
        finally:
            return True

    def wireEntryChanged(self, isInsertion, text):
        if isInsertion == "1":
            self.settings.set("wireColor", self.settings.get("wireColor") + text)
        elif isInsertion == "0":
            self.settings.set("wireColor", self.settings.get("wireColor")[:(-1 * len(text))])
        try:
            self.wireColorButton = Button(self, text='     ', command=self.setWireColor, bg=self.settings.get("wireColor")).grid(row = 1, column = 4)
        finally:
            return True

    def setBGColor(self):
        color = askcolor(self.settings.get("bgColor"))[1]
        if color:
            self.bgColorField.set(color)
            self.settings.set("bgColor", color)
            self.bgColorButton = Button(self, text='     ', command=self.setBGColor, bg=self.settings.get("bgColor")).grid(row = 0, column = 4)

    def setWireColor(self):
        color = askcolor(self.settings.get("wireColor"))[1]
        if color:
            self.wireColorField.set(color)
            self.settings.set("wireColor", color)
            self.wireColorButton = Button(self, text='     ', command=self.setWireColor, bg=self.settings.get("wireColor")).grid(row = 1, column = 4)
