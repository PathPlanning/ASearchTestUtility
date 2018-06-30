from advSettingsWindow import *
from tkinter import *
from tkinter import filedialog
from Test import *
from Application import *

class MainWindow(Tk):
    def __init__(self, app, title='MainWindow'):
        Tk.__init__(self)
        self.bgcolor = '#%02x%02x%02x' % (236, 236, 236)
        self.config(background= self.bgcolor)
        self.var = IntVar()
        self.parentApp = app
        self.path = ""
        self.mapfilepath = ""
        self.geometry('600x400')
        self.wm_title(title)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(5, weight=1)
        self.pathLab = Label(self, text="ASearch executable file:", width=19, anchor="w",font='Helvetica 12 bold', background= self.bgcolor)
        self.pathBox = Entry(self,  highlightbackground= self.bgcolor)
        self.mappathLab = Label(self, text="XML map file:", width=19, anchor="w", background= self.bgcolor, font='Helvetica 12 bold')
        self.mapPathBox = Entry(self, highlightbackground= self.bgcolor, state = "disable")
        self.runButton = Button(self, text="Start", command=self.runButtonClicked, width=6, highlightbackground= self.bgcolor)
        self.mapfileButton = Button(self, text="Map file", command=self.mapfileButtonClicked, state = "disable", background= self.bgcolor, highlightbackground= self.bgcolor)
        self.advButton = Button(self, text="Advanced", command=self.advButtonClicked, background= self.bgcolor, highlightbackground= self.bgcolor)
        self.fileButton = Button(self, text="File", command=self.fileButtonClicked, width=6, background= self.bgcolor, highlightbackground= self.bgcolor)

        self.mapsetLab = Label(self, text="Type of the map", width=19, anchor="w",font='Helvetica 12 bold', background= self.bgcolor)
        self.mapsettingsframe = Frame(self, background= self.bgcolor);
        self.rbutton1 = Radiobutton(self.mapsettingsframe, text='Empty map', variable=self.var, value=0, command = self.defaultMapSelected, anchor="w", background= self.bgcolor)
        #self.rbutton2 = Radiobutton(self.mapsettingsframe, text='Спираль', variable=self.var, value=1, anchor="w",command =  self.defaultMapSelected)
        self.rbutton3 = Radiobutton(self.mapsettingsframe, text='Chose map file', variable=self.var, value=2, command = self.notDefaultMapSelected, anchor="w", background= self.bgcolor)
        self.rbutton1.grid(row=0,sticky='new')
        #self.rbutton2.grid(row=1,sticky='new')
        self.rbutton3.grid(row=2,sticky='new')

        self.pathLab.grid(row=0, column=0, padx=10, pady=5, sticky='new', columnspan=2)
        self.pathBox.grid(row=1, column=0, padx=10, pady=0, sticky='new', columnspan=2)
        self.fileButton.grid(row=1, column=2, padx=10, pady=0, sticky='ne', columnspan=1)
        self.mappathLab.grid(row=2, column=0, padx=10, pady=5, sticky='new', columnspan=2)
        self.mapPathBox.grid(row=3, column=0, padx=10, pady=0, sticky='new', columnspan=2)
        self.mapfileButton.grid(row=3, column=2, padx=10, pady=0, sticky='ne')
        self.mapsetLab.grid(row=4, column=0, padx=10, pady=5, sticky='new', columnspan=2)
        self.mapsettingsframe.grid(row=5, column=0, sticky='wn', padx=10, pady=5)
        self.advButton.grid(row=6, column=0, sticky='sw', padx=10, pady=5)
        self.runButton.grid(row=6, column=2, sticky='se', padx=10, pady=5)


    def runButtonClicked(self):
        self.ProgressStart()
        self.path = self.pathBox.get()
        self.parentApp.ChangeTestPath(self.path, self.mapfilepath)
        self.parentApp.StartExperiment()

    def mapfileButtonClicked(self):
        self.mapfilepath = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=( ("XML", "*.xml"),))
        self.mapPathBox.delete(0, END)
        self.mapPathBox.insert(0, self.mapfilepath)
        self.parentApp.ChangeTestPath(self.path, self.mapfilepath)
        self.parentApp.ParseMapXML()
        self.parentApp.UpdateAdvWindow(self.var.get())


    def advButtonClicked(self):
        self.parentApp.advWindow.deiconify()

    def fileButtonClicked(self):
        self.path = filedialog.askopenfilename(initialdir="/", title="Select file")
        self.pathBox.delete(0, END)
        self.pathBox.insert(0, self.path)

    def defaultMapSelected(self):
        self.mapfileButton.config(state="disable")
        self.mapPathBox.config(state="disable")
        self.parentApp.ChangeTestMode(self.var.get())
        self.parentApp.UpdateAdvWindow(self.var.get())

    def notDefaultMapSelected(self):
        self.mapfileButton.config(state="normal")
        self.mapPathBox.config(state="normal")
        self.parentApp.ChangeTestMode(self.var.get())
        self.parentApp.UpdateAdvWindow(self.var.get())

    def ProgressStart(self):
        self.runButton.config(state="disable")
        self.advButton.config(state="disable")
        self.mapfileButton.config(state="disable")
        self.mapPathBox.config(state="disable")
        self.fileButton.config(state="disable")
        self.pathBox.config(state="disable")
        self.rbutton1.config(state="disable")
        self.rbutton3.config(state="disable")
        self.wm_title("In progress...")
        self.update()

    def ProgressEnd(self):
        self.runButton.config(state="normal")
        self.advButton.config(state="normal")

        if self.var.get() == 2:
            self.mapfileButton.config(state="normal")
            self.mapPathBox.config(state="normal")

        self.fileButton.config(state="normal")
        self.pathBox.config(state="normal")
        self.rbutton1.config(state="normal")
        self.rbutton3.config(state="normal")
        self.wm_title("PathTester")
        self.update()