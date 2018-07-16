from tkinter import filedialog
import _pickle as pickle
import getpass

class FileIO():
    def __init__(self, data, callbacks=[], fileName=""):
        self.fileName = fileName
        self.filetypes = (("Pickle files","*.pkl"),("all files","*.*"))
        user = getpass.getuser()
        self.initialdir = "Designs"
        self.data = data
        self.savedData = self.data.copy()
        self.callbacks = callbacks
        
    def openFile(self):
        self.fileName = filedialog.askopenfilename(filetypes=self.filetypes, initialdir=self.initialdir)
        data = None
        try:
            with open(self.fileName,'rb') as file:
                data = pickle.loads(file.read())
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
        self.fileName = filedialog.asksaveasfilename(filetypes=self.filetypes, initialdir=self.initialdir)
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

    def callCallbacks(self):
        for callback in self.callbacks:
            callback()

    def addCallbacks(self, callbacks):
        for callback in callbacks:
            self.callbacks.append(callback) 

    def getFileName(self):
        return self.fileName

