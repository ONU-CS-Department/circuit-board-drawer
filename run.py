from tkinter import Tk, Toplevel, Menu
from config import Config
from tshirtlogo import MainCanvas
from settings import Settings
from files import FileIO

class MainWindow(Tk):
    def __init__(self, fileManager):
        super().__init__()
        self.title("Computer Sciece Department Graphic - Untitled")
        self.fileManager = fileManager
        self.menubar = Menu(self)
        self.addMenuCascade("File", {"Open...":fileManager.openFile, "Save":fileManager.saveFile, "Save As":fileManager.saveFileAs})

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

if __name__ == '__main__':
    data = []
    dataCache = []
    fileManager = FileIO(data)
    mainWindow = MainWindow(fileManager)
    mainWindow.loopCallbacks(800, [mainWindow.setTitleToFileName])
    settings = Config(bgColor="#005500", wireColor="#C5A953", hasStartNode=False, hasEndNode=False, hasStartModule=False, hasEndModule=False, isContinuous=False)
    canvas = MainCanvas(data, settings=settings)
    fileManager.addCallbacks([mainWindow.setTitleToFileName, canvas.refreshCanvas])
    settingsWindowConfig = Toplevel(mainWindow)
    settingsWindowConfig.title("Settings")
    Settings(settings=settings, master=settingsWindowConfig)
    mainWindow.mainloop()
