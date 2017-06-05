#coding=utf-8

from PyQt5 import QtGui, QtCore, QtWidgets
import sys, os, time
sys.path.append("..")
from UILib.setting import Ui_Dialog
from publicfunc.updatedata import UpdateData
from globalset import FlagSet

reload(sys)
sys.setdefaultencoding("utf-8")

class Dialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.updatesystem)
        self.ui.pushButton_2.clicked.connect(self.updateyara)
        self.ui.pushButton_3.clicked.connect(self.updateclam)

    def updatesystem(self):
        update = QtWidgets.QMessageBox()
        #recv = update.question(self, u"更新", u"更新规则库时会停止扫描，是否更新", update.Yes, update.No)
        recv = update.question(self, u"Update", u"Scanning is Stopped while Updating. \n \n Update Now?", update.Yes, update.No)
        if recv == update.Yes:
            FlagSet.scanstopflag = 0
            U = UpdateData()
            U.pullApp()

    def updateyara(self):
        update = QtWidgets.QMessageBox()
        #recv = update.question(self, u"更新", u"更新规则库时会停止扫描，是否更新", update.Yes, update.No)
        recv = update.question(self, u"Update", u"Scanning is Stopped while Updating. \n \n Update Now?", update.Yes, update.No)
        if recv == update.Yes:
            FlagSet.scanstopflag = 0
            U = UpdateData()
            U.cloneYaraData()
            #U.updateYaraData()

    def updateclam(self):
        update = QtWidgets.QMessageBox()
        #recv = update.question(self, u"更新", u"更新规则库时会停止扫描，是否更新", update.Yes, update.No)
        recv = update.question(self, u"Update", u"Scanning is Stopped while Updating.\n \n Update Now?", update.Yes, update.No)
        if recv == update.Yes:
            FlagSet.scanstopflag = 0
            U = UpdateData()
            U.cloneClamData()
            #U.updateClamData()


if __name__ == "__main__":

    window = QtWidgets.QApplication(sys.argv)
    thiswindow = Dialog()
    thiswindow.show()

    sys.exit(window.exec_())
