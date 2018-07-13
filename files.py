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
        with open(self.fileName,'rb') as file:
            data = pickle.loads(file.read())
        self.data.clear()
        for lineObject in data:
            self.data.append(lineObject)
            self.savedData.append(lineObject)
        self.callCallbacks()
        
    def saveFile(self):
        print(self.fileName)
        if self.fileName:
            with open(self.fileName,'wb') as file:
                file.write(pickle.dumps(self.data))
            self.callCallbacks()
        else:
            self.saveFileAs()

    def isDirty(self):
        return False

    def saveFileAs(self):
        self.fileName = filedialog.asksaveasfilename(filetypes=self.filetypes, initialdir=self.initialdir)
        with open(self.fileName,'wb') as file:
            file.write(pickle.dumps(self.data))
        self.callCallbacks()

    def callCallbacks(self):
        for callback in self.callbacks:
            callback()

    def addCallbacks(self, callbacks):
        for callback in callbacks:
            self.callbacks.append(callback) 

    def getFileName(self):
        return self.fileName

