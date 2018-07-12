from tkinter import Button, Label, Entry, LEFT, StringVar, Frame, X, Checkbutton, HORIZONTAL, Menu, filedialog, colorchooser

class Settings(Frame):
    def __init__(self, settings=None, master=None):
        super().__init__(master)
        self.grid(row=0, columnspan=4)
        self.settings = settings
        
        self.addColorPicker(0, 'Background color:', "bgColor")
        self.addColorPicker(1, 'Draw color:', "wireColor")

        self.addCheckBox(2, "hasStartNode")
        self.addCheckBox(3, "hasEndNode")
        self.addCheckBox(4, "hasStartModule")
        self.addCheckBox(5, "hasEndModule")
        self.addCheckBox(6, "isContinuous")

    def addColorPicker(self, row, fieldLabel, settingValue):
        Label(self, text=fieldLabel).grid(row=row, column=1)
        colorField = StringVar(self, value=self.settings.get(settingValue))
        button = Button(self, text='     ', bg=self.settings.get(settingValue))
        button.configure(command=lambda: self.setButtonColor(row, settingValue, button, colorField))
        button.grid(row=row, column=4)
        entry = Entry(self, textvariable=colorField, width=15, validate='all')
        entry.bind("<KeyPress>", lambda event, settingValue=settingValue, button=button: self.onKeyPress(settingValue, event, button))
        entry.bind('<Control-v>', lambda e: 'break') #disable paste
        entry.grid(row=row, column=3)

    def onKeyPress(self, settingValue, event, button):
        potentialChar = ""
        if ((len(event.char) > 0) and (ord(event.char) < 128) and (ord(event.char) != 8)):
            potentialChar = event.char
        self.settings.set(settingValue, event.widget.get() + potentialChar)
        try:
            button.configure(bg=self.settings.get(settingValue))
        finally:
            return True

    def setButtonColor(self, row, settingValue, button, field):
        color = colorchooser.askcolor(self.settings.get(settingValue))[1]
        if color:
            field.set(color)
            self.settings.set(settingValue, color)
            button.configure(bg=self.settings.get(settingValue))

    def addCheckBox(self, row, value):
        Label(self, text = value.replace("_", " ").title() + ":").grid(row = row, column = 1)
        Checkbutton(self, command=lambda: self.toggleProperty(value)).grid(row=row, column=3)

    def toggleProperty(self, value):
        self.settings.set(value, not self.settings.get(value))
            
