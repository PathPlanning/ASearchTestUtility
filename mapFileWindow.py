from tkinter import *
from tkinter import filedialog

class MapFileWindow(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry('300x200')
        self.pathBox = Entry(self)
        self.fileButton = Button(self, text="Выбрать", command=self.fileButtonClicked)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.pathBox.grid(row=1, column=0, padx=10, pady=10, sticky='w', columnspan=3)
        self.fileButton.grid(row=1, column=1, padx=10, pady=10, sticky='e', columnspan=1)

    def ChoseMapFile(self):
        self.deiconify()

    def fileButtonClicked(self):
        self.path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=( ("all files", "*.*"), ("win exec", "*.exe"),))
        self.pathBox.delete(0, END)
        self.pathBox.insert(0, self.path)