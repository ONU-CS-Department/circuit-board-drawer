from tkinter import Tk, Menu
class MainWindow(Tk): 
    def __init__(self, fileManager, lines): 
        """Construct the object 
 
        Keyword arguments: 
        fileManager -- an instance of the "FileIO" class 
        lines -- array of "LineGraphic" objects 
        """ 
        super().__init__() 
        self.fileManager = fileManager 
        self.lines = lines 
        self.menubar = Menu(self) 
        self.bind('<Control-s>', lambda x: fileManager.saveFile()) # bind mouse motion to 
        self.bind('<Control-z>', self.undo) # bind mouse motion to 
        self.addMenuCascade("File", {"Open...":fileManager.openFile, "Save":fileManager.saveFile, "Save As":fileManager.saveFileAs}) 
        self.addMenuCascade("Edit", {"Undo":self.undo}) 
 
    def addMenuCascade(self, label, commands): 
        """Add a dropdown menu under the title bar of the window 
 
        Keyword arguments: 
        label -- label of dropdown button 
        commands -- dictionary of key/value pairs. Key is the button label; Value is the evoked function. 
        """ 
        menu = Menu(self.menubar, tearoff=False) 
        self.menubar.add_cascade(label=label, menu=menu) 
        for key, value in commands.items(): 
            menu.add_command(label=key, command=value) 
        self.__refreshMenuBar() 
 
    def setTitle(self, title): 
        """Set the title of the window""" 
        self.title(title) 
 
    def setTitleToFileName(self): 
        """Set the title of the window with file path appended""" 
        # If the file has unsaved changes, add an "*" before the filename 
        if self.fileManager.isDirty(): 
            self.setTitle("Computer Sciece Department Graphic - * " + self.fileManager.getFileName()) 
        else: 
            self.setTitle("Computer Sciece Department Graphic - " + self.fileManager.getFileName()) 
 
    def __refreshMenuBar(self): 
        """Refresh the dropdown menus""" 
        self.config(menu=self.menubar) 
 
    def loopCallbacks(self, milliseconds, callbacks): 
        """Calls functios "callbacks" every "milliseconds" milliseconds  
 
        Keyword arguments: 
        milliseconds -- number of milliseconds 
        callbacks -- functions to call 
        """ 
        for callback in callbacks: 
            callback() 
        self.after(milliseconds, lambda: self.loopCallbacks(milliseconds, callbacks))  # reschedule event in 2 seconds 
 
    def undo(self, event=None): 
        """Remove the most recently "LineGraphic" object in the lines array 
 
        Keyword arguments: 
        event -- a keyboard or click event 
        """ 
        if (self.lines): 
            self.lines.pop() 
            self.fileManager.callCallbacks() 
