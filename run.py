"""
This module holds the main window and program entry point.
"""
from tkinter import Toplevel
from circuitBD.configuration.config import Config
from circuitBD.gui.canvas import MainCanvas
from circuitBD.gui.settings import Settings
from circuitBD.file_io.files import FileIO
from circuitBD.gui.main_window import MainWindow

if __name__ == '__main__':
    lines = []
    fileManager = FileIO(lines)
    mainWindow = MainWindow(fileManager, lines)
    # Set window title to refresh every 0.5 seconds
    mainWindow.loopCallbacks(500, [mainWindow.setTitleToFileName])
    settings = Config(bgColor="#005500", wireColor="#C5A953", hasStartNode=False, hasEndNode=False, hasStartModule=False, hasEndModule=False, isContinuous=False, useStraightLines=False, size=8)
    canvas = MainCanvas(lines, settings=settings)
    fileManager.addCallbacks([mainWindow.setTitleToFileName, canvas.refreshCanvas])
    settingsWindowConfig = Toplevel(mainWindow)
    settingsWindowConfig.title("Settings")
    Settings(settings=settings, master=settingsWindowConfig)
    # Run tkinter mainloop
    mainWindow.mainloop()
