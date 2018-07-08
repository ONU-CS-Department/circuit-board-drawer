from tkinter import Tk, Toplevel, Menu
from config import Config
from tshirtlogo import MainCanvas
from settings import Settings

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Computer Sciece Department Graphic")
        self.menubar = Menu(self)

    def addMenuCascade(self, label, commands):
        menu = Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label=label, menu=menu)
        for key, value in commands.items():
            print(key)
            menu.add_command(label=key, command=value)
        self.__refreshMenuBar()

    def setTitle(title):
        self.title(title)

    def __refreshMenuBar(self):
        self.config(menu=self.menubar)

if __name__ == '__main__':
    mainWindow = MainWindow()
    settings = Config(bgColor="#005500", wireColor="#C5A953", hasStartNode=False, hasEndNode=False, hasStartModule=False, hasEndModule=False, isContinuous=False)
    canvas = MainCanvas(settings=settings)
    settingsWindowConfig = Toplevel(mainWindow)
    settingsWindowConfig.title("Settings")
    Settings(settings=settings, master=settingsWindowConfig)
    mainWindow.mainloop()
