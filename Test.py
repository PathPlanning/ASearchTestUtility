import os
import xml.etree.ElementTree as xml
import xlwt
from xlwt import Utils
from xlwt import XFStyle

# mode 0 - empty file
# mode 2 - map file
class Mission:
    def __init__(self):
        self.width = 10000
        self.height = 10000
        self.cellsize = 1
        self.startx = 0
        self.starty = 0
        self.finishx = self.width - 1
        self.finishy = self.height - 1
        self.metrictype = "diagonal"
        self.searchtype = "astar"
        self.hweight = 1
        self.breakingties = "g-max"
        self.allowdiagonal = 1
        self.allowsqueeze = 0
        self.cutcorners = 0
        self.opentype = "vectoroflists"
        self.allowdupl = 0


class Test:

    def __init__(self, app):
        self.parentApp = app
        self.repeat = 1
        self.execFilePath = ""
        self.mapFilePath = ""
        self.mode = 0
        self.loglevel = 0.5
        self.addstr = ""
        self.startSize = 100
        self.finSize = 101
        self.wb = xlwt.Workbook()
        self.res = self.wb.add_sheet('result')
        self.av = self.wb.add_sheet('average')
        self.resrow = 0
        self.avrow = 0
        self.sumtry = 0
        self.task = Mission()
        self.resnum = 0

    def StartTesting(self):
        if self.mode == 0:
            i = 0
            while i < self.repeat:
                j = self.startSize
                while j <= self.finSize:
                    self.width = j
                    self.height = j
                    self.finishx = self.width - 1
                    self.finishy = self.height - 1
                    self.GenerateEmptyXML()
                    os.system(self.execFilePath + " " + self.mapFilePath + " fakemap")
                    self.WriteResults( i, j)
                    j += 100
                i += 1
                self.resrow = 0
        elif self.mode == 2:
            self.ChangeMapXML()
            i = 0
            while i < self.repeat:
                os.system(self.execFilePath + " " + self.mapFilePath)
                self.WriteResults(i, self.width)
                i += 1
        self.CountAv()
        self.wb.save("Result_" + str(self.resnum) + ".xls")
        self.Reset()

    def GenerateEmptyXML(self):
        root = xml.Element("root")
        map = xml.Element("map")
        algorithm = xml.Element("algorithm")
        opentype = xml.Element("openstructure")
        options = xml.Element("options")
        root.append(map)
        root.append(algorithm)
        root.append(opentype)
        root.append(options)

        width = xml.SubElement(map, "width")
        width.text = str(self.task.width)
        height = xml.SubElement(map, "height")
        height.text = str(self.task.height)
        cellsize = xml.SubElement(map, "cellsize")
        cellsize.text = str(self.task.cellsize)
        startx = xml.SubElement(map, "startx")
        startx.text = str(self.task.startx)
        starty = xml.SubElement(map, "starty")
        starty.text = str(self.task.starty)
        finishx = xml.SubElement(map, "finishx")
        finishx.text = str(self.task.finishx)
        finishy = xml.SubElement(map, "finishy")
        finishy.text = str(self.task.finishy)

        metrictype = xml.SubElement(algorithm, "metrictype")
        metrictype.text = self.task.metrictype
        searchtype = xml.SubElement(algorithm, "searchtype")
        searchtype.text = self.task.searchtype
        hweight = xml.SubElement(algorithm, "hweight")
        hweight.text = str(self.task.hweight)
        breakingties = xml.SubElement(algorithm, "breakingties")
        breakingties.text = self.task.breakingties
        allowdiagonal = xml.SubElement(algorithm, "allowdiagonal")
        allowdiagonal.text = str(self.task.allowdiagonal)
        allowsqueeze = xml.SubElement(algorithm, "allowsqueeze")
        allowsqueeze.text = str(self.task.allowsqueeze)
        cutcorners = xml.SubElement(algorithm, "cutcorners")
        cutcorners.text = str(self.task.cutcorners)

        optype = xml.SubElement(opentype, "type")
        optype.text = self.task.opentype
        opdupl = xml.SubElement(opentype, "duplicate")
        opdupl.text = str(self.task.allowdupl)

        loglevel = xml.SubElement(options, "loglevel")
        loglevel.text = str(self.loglevel)
        logpath = xml.SubElement(options, "logpath")
        logfilename = xml.SubElement(options, "logfilename")

        tree = xml.ElementTree(root)

        with open("tmp.xml", "wb") as fh:
            tree.write(fh, encoding="utf-8")
        self.mapFilePath = "tmp.xml"

    def ChangeMapXML(self):
        tree = xml.parse(self.mapFilePath)
        tree.find('./algorithm/searchtype').text = self.task.searchtype
        tree.find('./algorithm/metrictype').text = self.task.metrictype
        tree.find('./algorithm/breakingties').text = self.task.breakingties
        tree.find('./algorithm/hweight').text = str(self.task.hweight)
        tree.find('./algorithm/allowdiagonal').text = str(self.task.allowdiagonal)
        tree.find('./algorithm/allowsqueeze').text = str(self.task.allowsqueeze)
        tree.find('./algorithm/cutcorners').text = str(self.task.cutcorners)
        try:
            tree.find('./openstructure/type').text = self.task.opentype
            tree.find('./openstructure/duplicate').text = str(self.task.allowdupl)
        except Exception:
            root = tree.getroot()
            opentype = xml.Element("openstructure")
            root.append(opentype)
            optype = xml.SubElement(opentype, "type")
            optype.text = self.task.opentype
            opdupl = xml.SubElement(opentype, "duplicate")
            opdupl.text = str(self.task.allowdupl)
        tree.write(self.mapFilePath[0:-4] + "_tmp.xml")

    def WriteResults(self, ntry, size):
        tree = xml.ElementTree(file=self.mapFilePath[0:-4] + "_log.xml")
        root = tree.getroot()
        log = root.find("log")
        summary = log.find("summary")
        sumitems = summary.items()
        modename = ""
        if self.mode == 0:
            modename = "emptymap"
        elif self.mode == 2:
            modename = "Not default map"
        if ntry == 0:
            self.res.write(self.resrow, 0, modename)
            self.res.write(self.resrow, 1, size)

        self.res.write(self.resrow, ntry + 2, sumitems[4][1])
        self.resrow += 1 * (1 if self.mode == 0 else 0)

    def CountAv(self):
        numstyle = XFStyle()
        numstyle.num_format_str = "0.0000"
        if self.mode == 0:
            i = 0
            while i <= (self.finSize - self.startSize)/100:
                formula = 'AVERAGE(C1:%s)' % (Utils.rowcol_to_cell( i, self.repeat + 1))
                self.res.write(i, 2 + self.repeat , xlwt.Formula(formula), numstyle)
                i += 1
        elif self.mode == 2:
            formula = 'AVERAGE(C1:%s)' % (Utils.rowcol_to_cell(0, self.repeat + 1))
            self.res.write(0, 2 + self.repeat, xlwt.Formula(formula), numstyle)

    def ParseMapXML(self):
        tree = xml.parse(self.mapFilePath)
        self.task.width = int(tree.find('./map/width').text)
        self.task.height = int(tree.find('./map/height').text)
        self.task.cellsize = int(tree.find('./map/cellsize').text)
        self.task.startx = int(tree.find('./map/startx').text)
        self.task.starty = int(tree.find('./map/starty').text)
        self.task.finishx = int(tree.find('./map/finishx').text)
        self.task.finishy = int(tree.find('./map/finishy').text)

        self.task.searchtype = tree.find('./algorithm/searchtype').text
        self.task.metrictype = tree.find('./algorithm/metrictype').text
        self.task.breakingties = tree.find('./algorithm/breakingties').text
        self.task.hweight = float(tree.find('./algorithm/hweight').text)
        self.task.allowdiagonal = int(tree.find('./algorithm/allowdiagonal').text)
        self.task.allowsqueeze = int(tree.find('./algorithm/allowsqueeze').text)
        self.task.cutcorners = int(tree.find('./algorithm/cutcorners').text)
        try:
            self.task.opentype = tree.find('./openstructure/type').text
            self.task.allowdupl = int(tree.find('./openstructure/duplicate').text)
        except Exception:
            self.task.opentype = "vectoroflists"
            self.task.allowdupl = 0

    def Reset(self):
        self.wb = xlwt.Workbook()
        self.res = self.wb.add_sheet('result')
        self.av = self.wb.add_sheet('average')
        self.resrow = 0
        self.avrow = 0
        self.sumtry = 0
        self.task = Mission()
        self.resnum = 0
        while os.path.exists("Result_" + str(self.resnum) + ".xls"):
            self.resnum += 1
