from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import StringVar
from tkinter import ttk



class AdvSettingsWindow(Toplevel):
    def __init__(self, app):
        Toplevel.__init__(self)
        self.parentApp = app
        self.repstr = StringVar()
        self.xstr = StringVar()
        self.ystr = StringVar()
        self.opentype = StringVar()
        self.allowdupl = 0
        self.opentypes = ("list", "vectoroflists", "set",  "vectorofsets", "priorityqueue", "vectorofpriorityqueues")
        self.rep = 1
        self.x = 100
        self.y = 101
        self.mode = 0
        self.error = 0
        self.errormes = ""

        self.wm_title("Advanced settings")
        self.geometry("410x320")
        self.resizable(False, False)
        self.readyButton = Button(self, text="Done", command=self.callback)

        self.expframe = Frame(self, height=140)
        self.expLabel = Label(self.expframe, text="Experiment settings", font='Helvetica 14 bold')

        self.empmapframe = Frame(self, height=140)
        self.empLabel = Label(self.empmapframe, text="Empty map settings", font='Helvetica 14 bold')

        self.repLabel = Label(self.expframe, text="Numper of repetition", width=19, anchor = "w")
        self.repeatBox = Entry(self.expframe, width=5, textvariable=self.repstr)
        self.opTypeLabel = Label(self.expframe, text="Open container type", width=19, anchor = "w")
        self.openTypeMenu = ttk.Combobox(self.expframe, textvariable=self.opentype, values = self.opentypes, width=17, state="readonly")
        self.openTypeMenu.set(self.opentypes[0])

        self.duplFrame = Frame(self.expframe)
        self.rbutton1 = Radiobutton(self.duplFrame, text='Without duplicates', variable=self.allowdupl, value=0, anchor="w")
        self.rbutton2 = Radiobutton(self.duplFrame, text='With duplicates', variable=self.allowdupl, value=1, anchor="w")
        self.rbutton1.select()
        self.rbutton1.pack(anchor="w")
        self.rbutton2.pack(anchor="w")


        self.stSiLab = Label(self.empmapframe, text="Starting size of map", width=19, anchor = "w")
        self.startSize = Entry(self.empmapframe, textvariable=self.xstr, width=19)
        self.fnSiLab = Label(self.empmapframe, text="Ending size of map", width=19, anchor = "w")
        self.finSize = Entry(self.empmapframe, textvariable=self.ystr, width=19)

        self.expLabel.grid(row=0, column=0,padx = 10,pady= 10, sticky='new',columnspan=2)
        self.opTypeLabel.grid(row=1, column=0, padx=10, sticky='nw')
        self.openTypeMenu.grid(row=1, column=1, padx=10, sticky='nw')
        self.duplFrame.grid(row=2, column=1, padx = 10,pady = 10, sticky='nw')
        self.repLabel.grid(row=3, column=0,padx = 10, sticky='nw')
        self.repeatBox.grid(row=3, column=1, padx=10, sticky='nw')


        self.empLabel.grid(row=0, column=0,padx = 10,pady= 10, sticky='new', columnspan=2)
        self.stSiLab.grid(row=1, column=0,padx = 10, sticky='nw')
        self.startSize.grid(row=1, column=1, padx=10, sticky='nw')
        self.fnSiLab.grid(row=2, column=0, padx = 10, sticky='nw')
        self.finSize.grid(row=2, column=1, padx=10, sticky='nw')
        self.expframe.pack(anchor="nw")
        self.empmapframe.pack(anchor="nw")
        self.readyButton.pack(anchor="se", padx=20, pady=20)
        self.protocol("WM_DELETE_WINDOW", self.callback)

        self.repstr.trace("w", lambda name, index, mode, var=self.repstr: self.repeatEnrChange(var))

        self.xstr.trace("w", lambda name, useless, mode, vars = (1, self.xstr, self.ystr): self.sizeEnrChanged(vars))
        self.ystr.trace("w", lambda name, useless, mode, vars = (2, self.xstr, self.ystr): self.sizeEnrChanged(vars))
        self.opentype.trace("w", self.CheckDupl)

        self.repeatBox.insert(0, str(self.rep))
        self.startSize.insert(0, str(self.x))
        self.finSize.insert(0, str(self.y))

    def callback(self):
        if self.error == 0:
            self.parentApp.UpdateTestAdvSettings(self.x, self.y, self.rep, self.opentype.get(), self.allowdupl)
            self.withdraw()
        else:
            messagebox.showinfo('Enter correct information', self.errormes)

    def repeatEnrChange(self, sv):
        try:
            tmp = int(sv.get())
            if tmp <= 0:
                raise ValueError('value should be more then 0')
            self.rep = tmp
            self.error = 0
            self.repeatBox.config({"background": "White"})
        except ValueError as e:
                self.repeatBox.config({"background": "Red"})
                self.error = 1
                self.errormes = "Enter correct number of repetition"
        return True

    def sizeEnrChanged(self, vars):
        if vars[0] == 1:
            entr = self.startSize
        else:
            entr = self.finSize
        try:
            tmp = int(vars[vars[0]].get())
            if tmp <= 0:
                raise ValueError('Value should be more then 0')
            entr.config({"background": "White"})
            if vars[0] == 1:
                self.x = tmp
            else:
                self.y = tmp

            if self.x >= self.y:
                raise Warning('Start valuse should be less then final')
            else:
                self.startSize.config({"background": "White"})
                self.finSize.config({"background": "White"})
            self.error = 0
        except ValueError as e:
                entr.config({"background": "Red"})
                self.error = 1
                self.errormes = "Enter correct size"
        except Warning as e:
            self.startSize.config({"background": "Red"})
            self.finSize.config({"background": "Red"})
            self.error = 1
            self.errormes = str(e)

        return True

    def UpdateMode(self, mode):
        self.mode = mode
        if self.mode == 0:
            self.startSize.config(state="normal")
            self.finSize.config(state="normal")
        else:
            self.startSize.config(state="disable")
            self.finSize.config(state="disable")

    def CheckDupl(self, *args):
        if(self.opentypes.index(self.opentype.get()) > 3):
            self.rbutton1.config(state="disable")
            self.rbutton2.config(state="disable")
        else:
            self.rbutton1.config(state="normal")
            self.rbutton2.config(state="normal")