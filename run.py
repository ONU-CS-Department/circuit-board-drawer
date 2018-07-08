from tkinter import Tk, Toplevel
from config import Config
from tshirtlogo import Application
from settings import Settings

if __name__ == '__main__':
    root = Tk()
    root.title("Computer Sciece Department Graphic")
    settings = Config(bgColor="#005500", wireColor="#C5A953", hasStartNode=False, hasEndNode=False, hasStartModule=False, hasEndModule=False, isContinuous=False)
    app = Application(settings=settings, master=root)
    settingsWindowConfig = Toplevel(root)
    settingsWindowConfig.title("Settings")
    Settings(settings=settings, master=settingsWindowConfig)
    root.mainloop()
