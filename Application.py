from mainWindow import *
from Test import *

class Application:

    def __init__(self):
        self.root = MainWindow(title="PathTester", app=self)
        self.advWindow = AdvSettingsWindow(app=self)
        self.advWindow.withdraw()
        self.experiment = Test(self)
        self.task = Mission()
        self.experiment.task = self.task
        self.advWindow.task = self.task
        self.root.mainloop()


    def ChangeTestMode(self, mode):
        self.experiment.mode = mode

    def StartTesting(self):
        self.experiment.StartTesting()

    def ChangeTestPath(self, path, mapfile):
        self.experiment.execFilePath = path
        self.experiment.mapFilePath = mapfile

    def ChangeTestRep(self, num):
        self.experiment.repeat = num

    def ChangeTestMapSize(self, x, y):
        self.experiment.SetMapSize(x, y)

    def UpdateTestAdvSettings(self, x, y, rep):
        self.experiment.startSize = x
        self.experiment.finSize = y
        self.experiment.repeat = rep

    def UpdateAdvWindow(self, mode):
        self.advWindow.Update(mode)

    def ParseMapXML(self):
        self.experiment.ParseMapXML()

    def StartExperiment(self):
        self.experiment.StartTesting()

    def EndExperiment(self):
        self.root.ProgressEnd()



