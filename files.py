from tkinter import filedialog
import cPickle as pickle

class FileIO:
    def __init__(self, fileName=""):
        self.fileName = fileName
        self.filetypes = (("Pickle files","*.pkl"))
        
    def openFile(self):
        self.fileName = filedialog.askopenfilename(filetypes=self.filetypes)
        return pickle.load(open(self.fileName, "rb") )
        
    def saveFile(self, data):
        if not self.fileName:
            pickle.dump(data, open(data, "wb"))
        else:
            self.saveFileAs(data)

    def saveFileAs(self, data):
        self.fileName = filedialog.asksaveasfilename(filetypes=self.filetypes)
        self.saveFile(data)

    def getFileName(self):
        return self.fileName

