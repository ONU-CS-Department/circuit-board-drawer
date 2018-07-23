"""
This module provides an interface for reading and writing to files.
"""
from tkinter import filedialog
import _pickle as pickle
import getpass

class FileIO():
    def __init__(self, data, callbacks=[], fileName=""):
        """Construct the object

        Keyword arguments:
        data -- an array of objects
        callbacks -- methods invoked when saving or opening a file
        fileName -- name of file to write to (default "")
        """
        self.fileName = fileName
        self.filetypes = (("Pickle files","*.pkl"),("all files","*.*"))
        self.data = data
        self.savedData = self.data.copy()
        self.callbacks = callbacks
        
    def openFile(self):
        """Open a file for writing"""
        self.fileName = filedialog.askopenfilename(filetypes=self.filetypes)
        data = None
        try:
            with open(self.fileName,'rb') as file:
                data = pickle.loads(file.read())
            # To ensure that the same "data" address reference is kept, clear and append new objects onto the data array
            # rather than setting self.data to a new array
            self.data.clear()
            for lineObject in data:
                self.data.append(lineObject)
            self.setSavePoint()
            self.callCallbacks()
        except FileNotFoundError:
            print("No file was chosen.")
        except:
            print("An unknown error has occured.")
        
    def saveFile(self):
        """Write to file"""
        if self.fileName:
            try:
                with open(self.fileName,'wb') as file:
                    file.write(pickle.dumps(self.data))
                self.setSavePoint()
                self.callCallbacks()
            except FileNotFoundError:
                print("No file was chosen")
            except:
                print("An unknown error has occured.")
        else:
            self.saveFileAs()

    def saveFileAs(self):
        """Choose a filename, then write to file"""
        self.fileName = filedialog.asksaveasfilename(filetypes=self.filetypes)
        self.fileName += ".pkl"
        try:
            with open(self.fileName,'wb') as file:
                file.write(pickle.dumps(self.data))
            self.setSavePoint()
            self.callCallbacks()
        except FileNotFoundError:
            print("No file was chosen")
        except:
            print("An unknown error has occured.")

    def setSavePoint(self):
        """When saving/opening a file. Set a marker for when data was last saved."""
        self.savedData = self.data.copy()

    def isDirty(self):
        """Return True if data needs to be saved"""
        return not (self.data == self.savedData)

    def callCallbacks(self):
        """Invoke callback functions"""
        for callback in self.callbacks:
            callback()

    def addCallbacks(self, callbacks):
        """Add callback functions

        Keyword arguments:
        callbacks -- an array of objects
        """
        for callback in callbacks:
            self.callbacks.append(callback) 

    def getFileName(self):
        """Get the fileName property"""
        return self.fileName

