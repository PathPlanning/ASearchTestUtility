from advSettingsWindow import *
from tkinter import *
from tkinter import filedialog
from Test import *
from Application import *

class MainWindow(Tk):
    def __init__(self, app, title='MainWindow'):
        Tk.__init__(self)
        self.var = IntVar()
        self.parentApp = app
        self.path = ""
        self.mapfilepath = ""
        self.geometry('600x400')
        self.wm_title(title)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.pathBox = Entry(self)
        self.mapPathBox = Entry(self)
        self.runButton = Button(self, text="Start", command=self.runButtonClicked, width=6)
        self.mapfileButton = Button(self, text="Map file", command=self.mapfileButtonClicked, state = "disable")
        self.advButton = Button(self, text="Advanced", command=self.advButtonClicked)
        self.fileButton = Button(self, text="File", command=self.fileButtonClicked, width=6)

        self.mapsettingsframe = Frame(self);
        self.rbutton1 = Radiobutton(self.mapsettingsframe, text='Empty map', variable=self.var, value=0, command = self.defaultMapSelected, anchor="w")
        #self.rbutton2 = Radiobutton(self.mapsettingsframe, text='Спираль', variable=self.var, value=1, anchor="w",command =  self.defaultMapSelected)
        self.rbutton3 = Radiobutton(self.mapsettingsframe, text='Chose map file', variable=self.var, value=2, command = self.notDefaultMapSelected, anchor="w")

        self.rbutton1.grid(row=0,sticky='new')
        #self.rbutton2.grid(row=1,sticky='new')
        self.rbutton3.grid(row=2,sticky='new')

        self.pathBox.grid(row=0, column=0, padx=10, pady=10, sticky='new', columnspan=2)
        self.mapPathBox.grid(row=2, column=0, padx=10, pady=10, sticky='new', columnspan=2)
        self.mapfileButton.grid(row=3, column=0, padx=10, pady=10, sticky='ws')
        self.advButton.grid(row=3, column=1, sticky='s', padx=10, pady=10)
        self.runButton.grid(row=3, column=2, sticky='se', padx=10, pady=10)
        self.fileButton.grid(row=0, column=2, padx=10, pady=10, sticky='ne', columnspan=1)

        self.mapsettingsframe.grid(row=1, column=0, sticky='wn', padx=10, pady=10)


    def runButtonClicked(self):
        self.path = self.pathBox.get()
        self.parentApp.ChangeTestExePath(self.path)
        self.parentApp.StartTesting()

    def mapfileButtonClicked(self):
        self.mapfilepath = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=( ("XML", "*.xml"),))
        self.mapPathBox.delete(0, END)
        self.mapPathBox.insert(0, self.mapfilepath)

    def advButtonClicked(self):
        self.parentApp.advWindow.deiconify()

    def fileButtonClicked(self):
        self.path = filedialog.askopenfilename(initialdir="/", title="Select file")
        self.pathBox.delete(0, END)
        self.pathBox.insert(0, self.path)

    def defaultMapSelected(self):
        self.mapfileButton.config(state="disable")
        self.parentApp.ChangeTestMode(self.var)

    def notDefaultMapSelected(self):
        self.mapfileButton.config(state="normal")
        self.parentApp.ChangeTestMode(self.var)
