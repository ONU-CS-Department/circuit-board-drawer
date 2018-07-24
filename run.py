"""
This module holds the main window and program entry point.
"""
from tkinter import Toplevel, Tk
from circuitBD.configuration.config import Config
from circuitBD.gui.canvas import MainCanvas
from circuitBD.gui.settings import Settings

if __name__ == '__main__':
    lines = []
    mainWindow = Tk()
    mainWindow.title("Circuit Board Drawer")
    # Set window title to refresh every 0.5 seconds
    settings = Config(bgColor="#005500", wireColor="#C5A953", hasStartNode=False, hasEndNode=False, hasStartModule=False, hasEndModule=False, isContinuous=False, useStraightLines=False)
    canvas = MainCanvas(lines, settings=settings)
    settingsWindowConfig = Toplevel(mainWindow)
    settingsWindowConfig.title("Settings")
    Settings(settings=settings, master=settingsWindowConfig)
    # Run tkinter mainloop
    mainWindow.mainloop()
