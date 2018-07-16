from tkinter import Tk, Toplevel, Menu
from config import Config
from tshirtlogo import MainCanvas
from settings import Settings
from files import FileIO

class MainWindow(Tk):
    def __init__(self, fileManager, lines):
        super().__init__()
        self.fileManager = fileManager
        self.lines = lines
        self.menubar = Menu(self)
        self.bind('<Control-s>', lambda x: fileManager.saveFile()) # bind mouse motion to
        self.bind('<Control-z>', self.undo) # bind mouse motion to
        self.addMenuCascade("File", {"Open...":fileManager.openFile, "Save":fileManager.saveFile, "Save As":fileManager.saveFileAs})
        self.addMenuCascade("Edit", {"Undo":self.undo})

    def addMenuCascade(self, label, commands):
        menu = Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label=label, menu=menu)
        for key, value in commands.items():
            menu.add_command(label=key, command=value)
        self.__refreshMenuBar()

    def setTitle(self, title):
        self.title(title)

    def setTitleToFileName(self):
        if fileManager.isDirty():
            self.setTitle("Computer Sciece Department Graphic - * " + self.fileManager.getFileName())
        else:
            self.setTitle("Computer Sciece Department Graphic - " + self.fileManager.getFileName())

    def __refreshMenuBar(self):
        self.config(menu=self.menubar)

    def loopCallbacks(self, milliseconds, callbacks):
        for callback in callbacks:
            callback()
        self.after(milliseconds, lambda: self.loopCallbacks(milliseconds, callbacks))  # reschedule event in 2 seconds

    def undo(self, event=None):     # Remove the previously drawn graphic
        if (self.lines):
            self.lines.pop()
            self.fileManager.callCallbacks()

if __name__ == '__main__':
    lines = []
    fileManager = FileIO(lines)
    mainWindow = MainWindow(fileManager, lines)
    mainWindow.loopCallbacks(500, [mainWindow.setTitleToFileName])
    settings = Config(bgColor="#005500", wireColor="#C5A953", hasStartNode=False, hasEndNode=False, hasStartModule=False, hasEndModule=False, isContinuous=False)
    canvas = MainCanvas(lines, settings=settings)
    fileManager.addCallbacks([mainWindow.setTitleToFileName, canvas.refreshCanvas])
    settingsWindowConfig = Toplevel(mainWindow)
    settingsWindowConfig.title("Settings")
    Settings(settings=settings, master=settingsWindowConfig)
    mainWindow.mainloop()
