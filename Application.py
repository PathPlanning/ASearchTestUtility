from mainWindow import *
from Test import Test

class Application:

    def __init__(self):
        self.root = MainWindow(title="PathTester", app=self)
        self.advWindow = AdvSettingsWindow(app=self)
        self.advWindow.withdraw()
        self.experiment = Test()
        self.root.mainloop()

    def ChangeTestMode(self, mode):
        self.experiment.mode = mode

    def StartTesting(self):
        self.experiment.StartTesting()

    def ChangeTestExePath(self, path):
        self.experiment.execFilePath = path

    def ChangeTestRep(self, num):
        self.experiment.repeat = num

    def ChangeTestMapSize(self, x, y):
        self.experiment.SetMapSize(x, y)

    def UpdateTestAdvSettings(self, x, y, rep, optype, allowdupl):
        self.experiment.startSize = x
        self.experiment.finSize = y
        self.experiment.repeat = rep
        self.experiment.opentype = optype
        self.experiment.allowdupl = allowdupl