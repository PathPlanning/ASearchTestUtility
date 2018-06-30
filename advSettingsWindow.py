from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import StringVar
from tkinter import ttk
from Test import Mission



class AdvSettingsWindow(Toplevel):
    def __init__(self, app):
        # Инициализация и списки значений
        Toplevel.__init__(self)
        self.parentApp = app
        self.opentypes = ("list", "vectoroflists", "set", "vectorofsets", "priorityqueue", "vectorofpriorityqueues")
        self.metrictypes = ("euclidean", "diagonal", "manhattan", "chebyshev")
        self.searchtypes = ("astar", "dijkstra")
        self.breakingties = ("g-min", "g-max")

        # Переменные-параметры теста
        self.task = Mission()
        self.repstr = StringVar()
        self.xstr = StringVar()
        self.ystr = StringVar()
        self.opentype = StringVar()
        self.allowdupl = 0
        self.rep = 1
        self.x = 10000
        self.y = 11000
        self.mode = 0
        self.mtype = StringVar()
        self.stype = StringVar()
        self.hwstr = StringVar()
        self.hw = 1
        self.brt = StringVar()
        self.allowdiagonal = IntVar()
        self.allowsqueeze = IntVar()
        self.cutcorners = IntVar()
        self.allowdiagonal.set(1)
        self.allowsqueeze.set(1)
        self.cutcorners.set(1)

        # Переменные отвечающие за обработку ошибочных данных
        self.error = 0
        self.errormes = ""

        # Описание окна
        self.wm_title("Advanced settings")
        self.bgcolor = '#%02x%02x%02x' % (236, 236, 236)
        self.redcolor = '#%02x%02x%02x' % (222, 110, 94)
        self.geometry("412x570")
        self.configure(background= self.bgcolor)
        self.resizable(False, False)
        self.readyButton = Button(self, text="Done", command=self.callback, width = 8, height=5, highlightbackground= self.bgcolor)
        self.protocol("WM_DELETE_WINDOW", self.callback)

        # Описание фрейма отвечающего за настройку эксперимента
        self.expframe = Frame(self, height=140)
        self.expframe.configure(background= self.bgcolor)
        self.expLabel = Label(self.expframe, text="Experiment settings", font='Helvetica 14 bold', background= self.bgcolor)
        self.repLabel = Label(self.expframe, text="Number of repetition", width=19, anchor="w", background= self.bgcolor)
        self.repeatBox = Entry(self.expframe, width=5, textvariable=self.repstr, background = self.bgcolor, highlightbackground= self.bgcolor)
        self.opTypeLabel = Label(self.expframe, text="Open container type", width=19, anchor="w", background= self.bgcolor)
        self.openTypeMenu = ttk.Combobox(self.expframe, textvariable=self.opentype, values=self.opentypes, width=18, state="readonly", background= self.bgcolor)
        self.openTypeMenu.set(self.opentypes[0])
        self.duplFrame = Frame(self.expframe, background= self.bgcolor)
        self.rbutton1 = Radiobutton(self.duplFrame, text='Without duplicates', variable=self.allowdupl, value=0, anchor="w", background= self.bgcolor)
        self.rbutton2 = Radiobutton(self.duplFrame, text='With duplicates', variable=self.allowdupl, value=1, anchor="w", background= self.bgcolor)
        self.rbutton1.select()
        self.rbutton1.pack(anchor="w")
        self.rbutton2.pack(anchor="w")
        self.expLabel.grid(row=0, column=0, padx=10, pady=10, sticky='new', columnspan=2)
        self.opTypeLabel.grid(row=1, column=0, padx=10, sticky='nw')
        self.openTypeMenu.grid(row=1, column=1, padx=10, sticky='nw')
        self.duplFrame.grid(row=2, column=1, padx=10, pady=10, sticky='nw')
        self.repLabel.grid(row=3, column=0, padx=10, sticky='nw')
        self.repeatBox.grid(row=3, column=1, padx=10, sticky='nw')
        self.repstr.trace("w", lambda name, index, mode, var=self.repstr: self.repeatEnrChange(var))
        self.opentype.trace("w", self.CheckDupl)
        self.repeatBox.insert(0, str(self.rep))

        # Описание фрейма отвечающего за настройку пустой карты
        self.empmapframe = Frame(self, height=140, background= self.bgcolor)
        self.empLabel = Label(self.empmapframe, text="Empty map settings", font='Helvetica 14 bold',background= self.bgcolor)
        self.stSiLab = Label(self.empmapframe, text="Starting size of map", width=19, anchor="w",background= self.bgcolor)
        self.startSize = Entry(self.empmapframe, textvariable=self.xstr, width=19, background= self.bgcolor, highlightbackground= self.bgcolor)
        self.fnSiLab = Label(self.empmapframe, text="Ending size of map", width=19, anchor="w", background= self.bgcolor)
        self.finSize = Entry(self.empmapframe, textvariable=self.ystr, width=19, background= self.bgcolor, highlightbackground= self.bgcolor)
        self.empLabel.grid(row=0, column=0, padx=10, pady=5, sticky='new', columnspan=2)
        self.stSiLab.grid(row=1, column=0, padx=10, pady=5, sticky='nw')
        self.startSize.grid(row=1, column=1, padx=10, pady=5,  sticky='nw')
        self.fnSiLab.grid(row=2, column=0, padx=10, pady=5, sticky='nw')
        self.finSize.grid(row=2, column=1, padx=10, pady=5, sticky='nw')
        self.xstr.trace("w", lambda name, useless, mode, vars=(1, self.xstr, self.ystr): self.sizeEnrChanged(vars))
        self.ystr.trace("w", lambda name, useless, mode, vars=(2, self.xstr, self.ystr): self.sizeEnrChanged(vars))
        self.startSize.insert(0, str(self.x))
        self.finSize.insert(0, str(self.y))

        # Описание фрейма отвечающего за настройку алгоритма
        self.algframe = Frame(self, height=140, background= self.bgcolor)
        self.algLabel = Label(self.algframe, text="Algorithm settings", font='Helvetica 14 bold', background= self.bgcolor)
        self.sTypeLabel = Label(self.algframe, text="Search type", width=19, anchor="w", background= self.bgcolor)
        self.sTypeMenu = ttk.Combobox(self.algframe, textvariable=self.stype, values=self.searchtypes, width=18, state="readonly", background= self.bgcolor)
        self.sTypeMenu.set(self.searchtypes[0])
        self.sTypeMenu.bind("<<ComboboxSelected>>", self.CheckSType)
        self.mTypeLabel = Label(self.algframe, text="AStar Metric type", width=19, anchor="w", background= self.bgcolor)
        self.mTypeMenu = ttk.Combobox(self.algframe, textvariable=self.mtype, values=self.metrictypes, width=18, state="readonly", background= self.bgcolor)
        self.mTypeMenu.set(self.metrictypes[0])

        self.hwLabel = Label(self.algframe, text="Heuristic function weight", width=19, anchor="w", background= self.bgcolor)
        self.hwEntry = Entry(self.algframe, textvariable=self.hwstr, width=19, background= self.bgcolor, highlightbackground= self.bgcolor)
        self.hwstr.trace("w", self.HweightChanged)
        self.hwEntry.insert(0, str(self.hw))

        self.brLabel = Label(self.algframe, text="Breakingties", width=19, anchor="w", background= self.bgcolor)
        self.brTypeMenu = ttk.Combobox(self.algframe, textvariable=self.brt, values=self.breakingties, width=18, state="readonly", background= self.bgcolor)
        self.brTypeMenu.set(self.breakingties[0])

        self.alldiagLabel = Label(self.algframe, text="Allow diagonal moves", width=19, anchor="w", background= self.bgcolor)
        self.alldiagCheck = Checkbutton(self.algframe, text="", variable=self.allowdiagonal,  anchor="w", background= self.bgcolor, command= self.CheckAllDiag)

        self.allsquLabel = Label(self.algframe, text="Allow squeeze", width=19, anchor="w", background= self.bgcolor)
        self.allsquCheck = Checkbutton(self.algframe, text="", variable=self.allowsqueeze,  anchor="w", background= self.bgcolor)

        self.cutcornLabel = Label(self.algframe, text="Allow cutting corners", width=19, anchor="w",background= self.bgcolor)
        self.cutcornCheck = Checkbutton(self.algframe, text="", variable=self.cutcorners,  anchor="w", background= self.bgcolor, command=self.CheckCutCorn)

        self.algLabel.grid(row=0, column=0, padx=10, pady=10, sticky='new', columnspan=2)

        self.sTypeLabel.grid(row=1, column=0, padx=10,pady=5, sticky='nw')
        self.sTypeMenu.grid(row=1, column=1, padx=10,pady=5, sticky='nw')
        self.mTypeLabel.grid(row=2, column=0, padx=10,pady=5, sticky='nw')
        self.mTypeMenu.grid(row=2, column=1, padx=10,pady=5, sticky='nw')
        self.brLabel.grid(row=3, column=0, padx=10, pady=5,sticky='nw')
        self.brTypeMenu.grid(row=3, column=1, padx=10, pady=5,sticky='nw')
        self.hwLabel.grid(row=4, column=0, padx=10, pady=5,sticky='nw')
        self.hwEntry.grid(row=4, column=1, padx=10,pady=5,sticky='nw')
        self.alldiagLabel.grid(row=5, column=0, padx=10, sticky='nw')
        self.alldiagCheck.grid(row=5, column=1, padx=10, sticky='nw')
        self.allsquLabel.grid(row=6, column=0, padx=10, sticky='nw')
        self.allsquCheck.grid(row=6, column=1, padx=10, sticky='nw')
        self.cutcornLabel.grid(row=7, column=0, padx=10, sticky='nw')
        self.cutcornCheck.grid(row=7, column=1, padx=10, sticky='nw')

        # Окончательное размещение объектов в окне
        self.expframe.pack(anchor="nw")
        self.empmapframe.pack(anchor="nw")
        self.algframe.pack(anchor="nw")
        self.readyButton.pack(anchor="se", padx=10, pady=5)

    # Проверка правильности всех введенных данных перед скрытием окна
    def callback(self):
        if self.error == 0:
            self.task.searchtype = self.stype.get()
            self.task.metrictype = self.mtype.get()
            self.task.breakingties = self.brt.get()
            self.task.hweight = self.hw
            self.task.allowdiagonal = self.allowdiagonal.get()
            self.task.allowsqueeze = self.allowsqueeze.get()
            self.task.cutcorners = self.cutcorners.get()
            self.task.opentype = self.opentype.get()
            self.task.allowdupl = self.allowdupl

            self.parentApp.UpdateTestAdvSettings(self.x, self.y, self.rep)
            self.withdraw()
        else:
            messagebox.showinfo('Enter correct information', self.errormes)

    # Изменение параметра повтора эксперимента
    def repeatEnrChange(self, sv):
        try:
            tmp = int(sv.get())
            if tmp <= 0:
                raise ValueError('value should be more then 0')
            self.rep = tmp
            self.error = 0
            self.repeatBox.config({"background": "White"})
        except ValueError as e:
            self.repeatBox.config({"background": self.redcolor})
            self.error = 1
            self.errormes = "Enter correct number of repetition"
        return True

    # Изменение параметров отвечающих за размер карты
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
            entr.config({"background": self.redcolor})
            self.error = 1
            self.errormes = "Enter correct size"
        except Warning as e:
            self.startSize.config({"background": self.redcolor})
            self.finSize.config({"background": self.redcolor})
            self.error = 1
            self.errormes = str(e)

        return True

    # Проверка режима тестирования
    def Update(self, mode, ):
        self.mode = mode
        if self.mode == 0:
            self.startSize.config(state="normal")
            self.finSize.config(state="normal")
        elif self.mode == 2:
            self.startSize.config(state="disable")
            self.finSize.config(state="disable")

            self.stype.set(self.task.searchtype)
            self.mtype.set(self.task.metrictype)
            self.brt.set(self.task.breakingties)
            self.hw = self.task.hweight
            self.hwstr.set(str(self.hw))
            self.allowdiagonal.set(self.task.allowdiagonal)
            self.allowsqueeze.set(self.task.allowsqueeze)
            self.cutcorners.set(self.task.cutcorners)
            self.opentype.set(self.task.opentype)
            self.allowdupl = self.task.allowdupl



    # Проверка возможности дубликатов для выбранного типа контейнера
    def CheckDupl(self, *args):
        if (self.opentypes.index(self.opentype.get()) > 3):
            self.rbutton1.select()
            self.rbutton1.config(state="disable")
            self.rbutton2.config(state="disable")
        else:
            self.rbutton1.config(state="normal")
            self.rbutton2.config(state="normal")

    # Проверка на тип алгоритма
    def CheckSType(self, event):
        if self.stype.get() == "dijkstra":
            self.mTypeMenu.config(state="disable")
            self.hwEntry.config(state="disable")
        else:
            self.mTypeMenu.config(state="normal")
            self.hwEntry.config(state="normal")

    # Проверка параметра веса h(v)
    def HweightChanged(self, *args):
        try:
            tmp = float(self.hwstr.get())
            if tmp <= 0 or tmp > 2:
                raise ValueError('hweight should be more then 0 and less then 2')
            self.hw = tmp
            self.error = 0
            self.hwEntry.config({"background": "White"})
        except ValueError as e:
            self.hwEntry.config({"background": self.redcolor})
            self.error = 1
            self.errormes = "Enter correct hweight value"
        return True

    def CheckAllDiag(self):
        if self.allowdiagonal.get() == 0:
            self.allsquCheck.config(state="disable")
            self.cutcornCheck.config(state="disable")
            self.allowsqueeze.set(0)
            self.cutcorners.set(0)
        else:
            self.allsquCheck.config(state="normal")
            self.cutcornCheck.config(state="normal")

    def CheckCutCorn(self):
        if self.cutcorners.get() == 0:
            self.allsquCheck.config(state="disable")
            self.allowsqueeze.set(0)
        else:
            self.allsquCheck.config(state="normal")
