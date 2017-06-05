#coding=utf-8

from PyQt5 import QtGui, QtCore, QtWidgets
import sys, os, time
sys.path.append("..")
from UILib.detail import Ui_Dialog
from advanceoperate.detailthread import FileDetail, PEFileInfo
from globalset import ImpAlert

reload(sys)
sys.setdefaultencoding("utf-8")

class Dialog(QtWidgets.QDialog):
    # detailSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.widget   = self.ui.listWidget
        self.tree     = self.ui.treeWidget
        self.table    = self.ui.tableWidget
        self.filename = ""
        self.md5      = ""
        self.filetype = ""

    def getFileName(self, filename, md5):
        self.filename = filename
        self.md5      = md5
        self.detail   = FileDetail(self.filename) # 基本信息/Basic Information
        self.peinfo   = PEFileInfo(self.filename, self.md5) # PE信息/PE Information
        self.detail.finishSignal.connect(self.showBaseInfo)
        self.detail.start()

    def showBaseInfo(self, msg):
        self.widget.clear() # 清空list内容/Empty List Content
        self.table.clearContents() # 清空table内容保留列名/Empty Table Content Retention Column Name
        self.tree.clear()
        for n in msg:
            if "PE32" in n or "executable" in n:
                self.peinfo.importSignal.connect(self.showImpImfo) # 连接显示导入表widget/Connection Display Import Table Widget
                self.peinfo.sectionSignal.connect(self.showSetInfo) # 连接显示节信息widget/Connection Display Section Information Widget
                self.peinfo.start()
            n = unicode(n)
            self.widget.addItem(n)

    def showAdvInfo(self, msg):
        print "aadfasf"

    '''
    #显示PE import信息
    Show PE Import Information
    #未处理dll名None情况
    Unhandled DLL Name None Condition
    #已处理API名None情况
    Processed API Name None Condition
    '''
    def showImpImfo(self, msg):
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels([u"Name", u"Description"])
        alt = ImpAlert().alerts # 取glob内容
        att = [] # 需要注意的API列表->转集合/Note API List-> Turn Collection
        rootindex = len(msg.keys())
        for i in range(rootindex):
            dll = QtWidgets.QTreeWidgetItem(self.tree)
            keyname = msg.keys()[i]
            dll.setText(0, keyname)
            childindex = len(msg[keyname])
            for j in range(childindex):
                if None == msg[keyname][j]:
                    continue
                child = QtWidgets.QTreeWidgetItem(dll)
                child.setText(0, msg[keyname][j])
                if any(map(msg[keyname][j].startswith, alt.keys())):
                    att.append(msg[keyname][j])
                    child.setForeground(0, QtCore.Qt.red)
                    for a in alt:
                        if msg[keyname][j].startswith(a):
                            child.setText(1, alt.get(a))
        alert = QtWidgets.QTreeWidgetItem(self.tree)
        alert.setText(0, "Suspicious API")
        alert.setForeground(0, QtCore.Qt.red)
        att = list(set(att))
        for i in range(len(att)):
            child = QtWidgets.QTreeWidgetItem(alert)
            child.setText(0, att[i])
            child.setForeground(0, QtCore.Qt.red)

    '''
    #在tablewidget中显示PE节信息
    Display PE Section Information in tablewidget
    '''
    def showSetInfo(self, msg):
        # 认可的节名称/Approved Section Name
        goodsection = ['.data', '.text', '.code', '.reloc', '.idata', '.edata', '.rdata', '.bss', '.rsrc']
        self.table.setRowCount(msg[0])
        for i in range(msg[0]):
            for j in range(5):
                item = str(msg[i * 5 + j + 1])
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(item))
        self.table.horizontalHeader().setSectionResizeMode(1) #自适应宽度/Adaptive Width
        for i in range(msg[0]):
            secname = self.table.item(i, 0)
            if secname.text() not in goodsection:
                secname.setForeground(QtCore.Qt.red)
            entrpoy = self.table.item(i, 4)
            if float(entrpoy.text()) < 1 or float(entrpoy.text()) > 7:
                entrpoy.setForeground(QtCore.Qt.red)
            rawsize = self.table.item(i, 3)
            if 0 == int(rawsize.text()):
                rawsize.setForeground(QtCore.Qt.red)
        print "updated tablewidget"


if __name__ == "__main__":

    window = QtWidgets.QApplication(sys.argv)
    thiswindow = Dialog()
    thiswindow.show()

    sys.exit(window.exec_())
