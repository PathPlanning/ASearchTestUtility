import os
import xml.etree.ElementTree as xml
import xlwt
from xlwt import Utils
from xlwt import XFStyle


# mode 0 - empty file
# mode 1 - map file


class Test:

    def __init__(self):
        self.width = 10000
        self.height = 10000
        self.repeat = 1
        self.cellsize = 1
        self.startx = 0
        self.starty = 0
        self.finishx = self.width - 1
        self.finishy = self.height - 1
        self.execFilePath = ""
        self.mapFilePath = ""
        self.mode = 0
        self.metrictype = "diagonal"
        self.searchtype = "astar"
        self.hweight = 1
        self.breakingties = "g-max"
        self.allowdiagonal = 1
        self.allowsqueeze = 0
        self.cutcorners = 0
        self.loglevel = 0.5
        self.addstr = ""
        self.startSize = 100
        self.finSize = 101
        self.opentype = "vectoroflists"
        self.allowdupl = 0
        self.wb = xlwt.Workbook()
        self.res = self.wb.add_sheet('result')
        self.av = self.wb.add_sheet('average')
        self.resrow = 0
        self.avrow = 0
        self.sumtry = 0

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
            i = 0
            while i < self.repeat:
                os.system(self.execFilePath + " " + self.mapFilePath)
                self.WriteResults(i, self.width)
                i += 1
        self.CountAv()
        self.wb.save('Result.xls')

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
        width.text = str(self.width)
        height = xml.SubElement(map, "height")
        height.text = str(self.height)
        cellsize = xml.SubElement(map, "cellsize")
        cellsize.text = str(self.cellsize)
        startx = xml.SubElement(map, "startx")
        startx.text = str(self.startx)
        starty = xml.SubElement(map, "starty")
        starty.text = str(self.starty)
        finishx = xml.SubElement(map, "finishx")
        finishx.text = str(self.finishx)
        finishy = xml.SubElement(map, "finishy")
        finishy.text = str(self.finishy)

        metrictype = xml.SubElement(algorithm, "metrictype")
        metrictype.text = self.metrictype
        searchtype = xml.SubElement(algorithm, "searchtype")
        searchtype.text = self.searchtype
        hweight = xml.SubElement(algorithm, "hweight")
        hweight.text = str(self.hweight)
        breakingties = xml.SubElement(algorithm, "breakingties")
        breakingties.text = self.breakingties
        allowdiagonal = xml.SubElement(algorithm, "allowdiagonal")
        allowdiagonal.text = str(self.allowdiagonal)
        allowsqueeze = xml.SubElement(algorithm, "allowsqueeze")
        allowsqueeze.text = str(self.allowsqueeze)
        cutcorners = xml.SubElement(algorithm, "cutcorners")
        cutcorners.text = str(self.cutcorners)

        metrictype = xml.SubElement(opentype, "type")
        metrictype.text = self.opentype
        metrictype = xml.SubElement(opentype, "duplicate")
        metrictype.text = str(self.allowdupl)

        loglevel = xml.SubElement(options, "loglevel")
        loglevel.text = str(self.loglevel)
        loglevel = xml.SubElement(options, "logpath")
        loglevel = xml.SubElement(options, "logfilename")

        tree = xml.ElementTree(root)

        with open("tmp.xml", "wb") as fh:
            tree.write(fh, encoding="utf-8")
        self.mapFilePath = "tmp.xml"

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