#coding=utf-8

import sys, os
from PyQt5 import QtCore
import sqlite3
sys.path.append("..")
from publicfunc.fileanalyze import FileAnalize, getFileInfo

class FileDetail(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(list)

    def __init__(self, filename, parent=None):
        super(FileDetail, self).__init__(parent)
        self.filename = str(filename)#.encode('cp936')

    def run(self):
        # 获取文件基本内容/Get the Basic Contents of a File
        useless, baseinfo = getFileInfo(self.filename)
        self.finishSignal.emit(baseinfo)

class PEFileInfo(QtCore.QThread):
    sectionSignal = QtCore.pyqtSignal(list)
    importSignal  = QtCore.pyqtSignal(dict)

    def __init__(self, filename, md5, parent=None):
        super(PEFileInfo, self).__init__(parent)
        self.filename = str(filename)#.encode('cp936')
        self.md5      = str(md5)

    # 处理PE节/Processing PE Section
    def getSetInfo(self):
        pefile  = FileAnalize(self.filename)
        setinfo = pefile.checkFileSections()
        return setinfo

    # 处理导入表/Processing Import Tables
    def getImpInfo(self):
        pefile  = FileAnalize(self.filename)
        impinfo = pefile.checkFileImports()
        return impinfo

    def run(self):
        print "pefile info from thread"
        try:
            sqlconn = sqlite3.connect("../db/fileinfo.db")
        except sqlite3.Error, e:
            print "sqlite connect failed", "\n", e.args[0]
        sqlcursor = sqlconn.cursor()
        try:
            sqlcursor.execute("select * from pe_info where md5=?", (self.md5,))
            sqlconn.commit()
            sqlcursor = sqlcursor.fetchone()
            if sqlcursor:
                impinfo = dict(eval(sqlcursor[3])) # 获取导入表信息/Get Import table Information
                setinfo = list(eval(sqlcursor[2])) # 获取PE节信息/Get PE Section Information
                self.importSignal.emit(impinfo)
                self.sectionSignal.emit(setinfo)
            else:
                self.importSignal.emit(self.getImpInfo())
                self.sectionSignal.emit(self.getSetInfo())
        except sqlite3.Error, e:
            print "sqlite exec err", "\n", e.args[0]
