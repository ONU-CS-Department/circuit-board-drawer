"""
This module is a Settings tkinter frame that holds checkboxes
and color pickers to edit value of config variables.
"""
from tkinter import Button, Label, Entry, LEFT, StringVar, Frame, X, Checkbutton, HORIZONTAL, Menu, filedialog, colorchooser

class Settings(Frame):
    def __init__(self, settings=None, master=None):
        """Construct the object

        Keyword arguments:
        settings -- a Config instance (default None)
        master -- class to inherit from (default None)
        """
        super().__init__(master)
        self.grid(row=0, columnspan=4)
        self.settings = settings
        
        self.addColorPicker(0, 'Background color:', "bgColor")
        self.addColorPicker(1, 'Draw color:', "wireColor")

        self.addCheckBox(2, "hasStartNode", "Has Start Node")
        self.addCheckBox(3, "hasEndNode", "Has End Node")
        self.addCheckBox(4, "hasStartModule", "Has Start Module")
        self.addCheckBox(5, "hasEndModule", "Has End Module")
        self.addCheckBox(6, "isContinuous", "Is Continuous")

    def addColorPicker(self, row, fieldLabel, settingKey):
        """Add a color picker to the frame

        Keyword arguments:
        row -- row to insert color picker into
        fieldLabel -- label to display to the user
        settingKey -- configuration variable to bind to color picker
        """
        Label(self, text=fieldLabel).grid(row=row, column=1)
        colorField = StringVar(self, value=self.settings.get(settingKey))
        button = Button(self, text='     ', bg=self.settings.get(settingKey))
        button.configure(command=lambda: self.chooseColor(settingKey, button, colorField))
        button.grid(row=row, column=4)
        entry = Entry(self, textvariable=colorField, width=15, validate='all')
        entry.bind("<KeyPress>", lambda event, settingKey=settingKey, button=button: self.onKeyPress(settingKey, event, button))
        entry.bind('<Control-v>', lambda e: 'break') #disable paste
        entry.grid(row=row, column=3)

    def onKeyPress(self, settingKey, event, button):
        """Add a color picker to the frame

        Keyword arguments:
        settingKey -- config variable to update when entering characters in field
        event -- keypress event
        button -- button to change the background color of
        """
        potentialChar = ""
        if ((len(event.char) > 0) and (ord(event.char) < 128) and (ord(event.char) != 8)):
            potentialChar = event.char
        self.settings.set(settingKey, event.widget.get() + potentialChar)
        try:
            button.configure(bg=self.settings.get(settingKey))
        finally:
            return True

    def chooseColor(self, settingKey, button, field):
        """Choose a color. The bg color of color button will change and the config variable will update

        Keyword arguments:
        settingKey -- configuration variable to update
        button -- button to update the color of
        field -- field to update with new color hex code
        """
        color = colorchooser.askcolor(self.settings.get(settingKey))[1]
        if color:
            field.set(color)
            self.settings.set(settingKey, color)
            button.configure(bg=self.settings.get(settingKey))

    def addCheckBox(self, row, key, fieldLabel):
        """Add a checkbox. When toggled, configuration variable is toggled

        Keyword arguments:
        row -- row to insert checkbox into
        key -- configuration variable to toggle
        fieldLabel -- label to display to the user
        """
        Label(self, text = fieldLabel + ":").grid(row = row, column = 1)
        Checkbutton(self, command=lambda: self.toggleProperty(key)).grid(row=row, column=3)

    def toggleProperty(self, key):
        """Toggle a configuration variable

        Keyword arguments:
        key -- configuration variable to toggle
        """
        self.settings.set(key, not self.settings.get(key))
            
