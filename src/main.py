# -*- coding: utf-8 -*-

'''
    S.M.A.R.T.
    Static Malware Analysis and Report Tool
    author: Zeng RuoXing
    ->
    PLAIT
    PyLance Artificial Intelligence Tool
    (as is, ya gone an' plai't yerself)
    editor:

'''

from PyQt5 import QtGui, QtCore, QtWidgets
import QTermWidget
from UILib.main import Ui_MainWindow
import time, sys, os, shutil
from datetime import datetime
from control import CheckFolder, ScanFile
from menuset.setting import Dialog as SetDialog
from menuset.validation import Dialog as mlvdDialog
from menuset.editwhitelist import Dialog as WtLDialog
from menuset.authorinfo import Dialog as AuthorInfo
from menuset.filedetail import Dialog as DetailDialog
from menuset.ngramopcode import Dialog as OpcodeDialog
from menuset.malimgclassify import Dialog as MalimgDialog
from menuset.uploadfile import Dialog as UploadDialog
from globalset import FlagSet, FilePath
import sqlite3

reload(sys)
sys.setdefaultencoding( "utf-8" )

class MainWindow(QtWidgets.QMainWindow):
    # scanemit = QtCore.pyqtSignal(str)
    # anailzemit = QtCore.pyqtSignal(str) # 开始分析文件信号/Start Parsing File Signals

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # checkBox对象/Object
        # 扫描规则部分/Scan Rule Section
        self.cbrall  = self.ui.CBRuleAll    # 规则全选/Selection All
        self.cbrpe   = self.ui.CBRulePE     # PE分析/PE Analysis
        self.cbrcryp = self.ui.CBRuleCrypto # 检查加密/Check Encryption
        self.cbrpack = self.ui.CBRulePack   # 文件查壳/File Case
        self.cbrself = self.ui.CBRuleSelf   # 自定义规则/Custom Rules
        self.cbrwl   = self.ui.CBRuleWL     # 白名单/Whitelist
        # 文件类型部分/File Type Section
        self.cbtall  = self.ui.CBTypeAll    # 类型全选/Select All
        self.cbtpe   = self.ui.CBTypePE     # PE类型/PE
        self.cbtofs  = self.ui.CBTypeOffice # office类型/Office
        self.cbtsh   = self.ui.CBTypeShell  # 脚本类型/Script
        self.cbtzip  = self.ui.CBTypeZip    # 压缩包/Archive
        self.cbtmda  = self.ui.CBTypeMedia  # 多媒体/Multimedia
        self.cbtasm  = self.ui.CBTypeAsm    # asm文件/Assembly

        # 扫描选项下拉菜单/Scan Options Dropdown Menu
        self.cbbox = self.ui.comboBox

        # 初始按键不可用/Initial Key Unavailable
        self.ui.PB_Start.setEnabled(False)
        self.ui.PB_End.setEnabled(False)
        self.ui.PB_SelectHistory.setEnabled(False)

        # tab2信息显示textEdit/tab2 - Information Display textEdit
        self.text = self.ui.textEdit
        self.ui.PB_ClearLog.clicked.connect(self.clearAnalysisLog)
        self.ui.PB_KeepLog.clicked.connect(self.saveAnalysisLog)

        # tab3日历widget/tab3 - Calendar Widget
        self.calender = self.ui.calendarWidget
        self.calender.clicked.connect(self.getCalenderDate)
        self.table2 = self.ui.tableWidget_2
        self.historydb = ''
        self.ui.PB_SelectHistory.clicked.connect(lambda: self.queryDBOperate(2))

        # tab4日历widget/tab4 - Debug Widget
        #self.debug = self.ui.debug

        # 设置tablewdiget属性/Setup Table Properties Widget
        # 自动适配header宽度，效果不好后期改适配最后一列/Auto Header Width, The Effect is Not Good Late Change Fitting Final Column
        # setStretchLastSection已在ui文件中设置/setStretchLastSection Set in UI File
        # 设置不可编辑 设置每次选中一行 设置可多选/Set Non-Editable Settings Each Selected - Setup Multiple Options
        # 设置id列不显示/Hide ID Column
        self.table = self.ui.tableWidget
        # self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        # self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.table.setColumnHidden(8, True)

        # tablewidget信号槽--排序/tablewidget Signal Slot--Sort
        self.table.horizontalHeader().sectionClicked.connect(self.tableHeaderEvent)

        # 右键菜单信号槽/Right Button Menu Signal Slot
        self.table.customContextMenuRequested.connect(self.generateMenu)

        # 菜单栏控件-索引字典/Menu Bar Controls-Indexed Dictionaries
        self.menubardict = {
            self.ui.AC_Check   : 0, # 检查配置/Check Configurations
            self.ui.AC_Setting : 1, # 软件设置/Software Settings
            self.ui.AC_CheckML : 2, # 机器学习/Machine Learning
            self.ui.AC_EditWL  : 3, # 名单设置/List Settings
            self.ui.AC_Info    : 4, # 版本信息/Version Information
            self.ui.AC_About   : 5, # 关于软件/About Software
            self.ui.AC_Author  : 6  # 联系作者/Contact Author
        }

        # 菜单栏信号槽/Menu Bar Signal Slot
        # for key, value in self.menubardict.items():
        #     print key, value
        #     key.triggered.connect(lambda: self.menuBarOperate(value))
        self.ui.AC_Check.triggered.connect(lambda: self.menuBarOperate(0))
        self.ui.AC_Setting.triggered.connect(lambda: self.menuBarOperate(1))
        self.ui.AC_CheckML.triggered.connect(lambda: self.menuBarOperate(2))
        self.ui.AC_EditWL.triggered.connect(lambda: self.menuBarOperate(3))
        self.ui.AC_Info.triggered.connect(lambda: self.menuBarOperate(4))
        self.ui.AC_About.triggered.connect(lambda: self.menuBarOperate(5))
        self.ui.AC_Author.triggered.connect(lambda: self.menuBarOperate(6))

        self.scanflag = 0  # 扫描策略flag/Scan Policy Flag
        self.folder   = '' # 选取文件夹路径/Select Folder Path
        self.files    = [] # 最终选取的文件名列表/List of Final Selected File Names
        self.depth    = -1
        self.dirsnum  = 0
        self.filenum  = 0
        self.table    = self.ui.tableWidget
        self.rowindex = 0
        self.rulelist = ['2', '3', '4', '5', '6']
        self.typelist = ['7', '8', '9', '10', '11', '12']
        self.rule     = [] # 发送至control的扫描规则/Send to Scanning Rules
        self.type     = [] # 发送至control的文件类型/Send to File Type
        self.flist    = [] # uploadfile判断更新滑动窗口uploadfile/Judging Update Sliding Window
        self.enter    = -1 # 回车更新数据库id//Return Update Database ID

        # 其他窗口对象实例/Other Window Object Instances
        self.setdialog    = SetDialog() # 设置/Set Up
        self.mlvddialog   = mlvdDialog()   # 机器学习验证/Machine Learning Validation
        self.wtldialog    = WtLDialog()    # 白名单/Whitelist
        self.authorinfo   = AuthorInfo() # 作者/Author
        self.detailDialog = DetailDialog() # 文件信息/File Information
        self.opcodeDialog = OpcodeDialog() # 操作码n元语法分类/N-Meta Syntax Classification of OpCode
        self.malimgDialog = MalimgDialog() # 二进制文件图像分类/Binary File Image Classification
        self.uploadDialog = UploadDialog() # 文件上传/File Upload

        # 按钮事件信号槽/Button Event Signal Slot
        #QtCore.QObject.connect(self.ui.PB_SelectFolder, QtCore.SIGNAL("clicked()"), self.selectFolder)
        self.ui.PB_SelectFolder.clicked.connect(self.selectFolder)
        #QtCore.QObject.connect(self.ui.PB_Start, QtCore.SIGNAL("clicked()"), self.startScan)
        self.ui.PB_Start.clicked.connect(self.startScan)
        #QtCore.QObject.connect(self.ui.PB_Clear, QtCore.SIGNAL("clicked()"), self.clearTableWidget)
        self.ui.PB_Clear.clicked.connect(self.clearTableWidget)
        self.ui.PB_End.clicked.connect(self.stopScan)
        self.ui.PB_Recover.clicked.connect(lambda: self.queryDBOperate(0))
        self.ui.PB_Select.clicked.connect(lambda: self.queryDBOperate(1))
        self.ui.PB_Store.clicked.connect(self.store2DataBaseByDate)

        self.fuzzy = self.ui.lineEditSelect # 模糊查询lineEdit/Fuzzy Query LineEdit

        # checkbox信号槽/CheckBox Signal Slot
        # 使用lambda表达式自定义参数/Customizing Parameters Using Lambda Expressions
        self.cbrall.clicked.connect(lambda: self.checkBoxEvent(0))
        self.cbtall.clicked.connect(lambda: self.checkBoxEvent(1))
        self.cbrpe.clicked.connect(lambda: self.checkBoxEvent(2))
        self.cbrcryp.clicked.connect(lambda: self.checkBoxEvent(3))
        self.cbrpack.clicked.connect(lambda: self.checkBoxEvent(4))
        self.cbrself.clicked.connect(lambda: self.checkBoxEvent(5))
        self.cbrwl.clicked.connect(lambda: self.checkBoxEvent(6))
        self.cbtpe.clicked.connect(lambda: self.checkBoxEvent(7))
        self.cbtofs.clicked.connect(lambda: self.checkBoxEvent(8))
        self.cbtsh.clicked.connect(lambda: self.checkBoxEvent(9))
        self.cbtzip.clicked.connect(lambda: self.checkBoxEvent(10))
        self.cbtmda.clicked.connect(lambda: self.checkBoxEvent(11))
        self.cbtasm.clicked.connect(lambda: self.checkBoxEvent(12))

        # 连接线程操作的信号槽/Signaling Slot for Connecting Thread Operations
        # self.scanemit.connect(self.recvInitSingal)
        # self.anailzemit.connect(self.updateScanInfo)

    '''
    #选择文件按钮事件响应函数
    Select File Button Event Response Function
    #设置扫描文件或扫描文件夹
    Set Up Scanning Files or Scanning Folders
    # 假设以扫描类型作为开始扫描动作测试/Suppose Scanning Type as a Start Scanning Action Test
    # 需要实现在功能函数线程中而非UI线程/Need to Implement in Functional Function Threads Instead of UI Threads
    '''
    def selectFolder(self):
        if 0 == self.cbbox.currentIndex():
            self.scanflag = 0
            #self.folder = QtWidgets.QFileDialog.getExistingDirectory(self, u"选择文件夹", "e:\\")#QtCore.QDir.currentPath())
            self.folder = QtWidgets.QFileDialog.getExistingDirectory(self, u"Select Folder", "e:\\")#QtCore.QDir.currentPath())
            if self.folder:
                #showmsg = u"选择：" + self.folder
                showmsg = u"Select：" + self.folder
                self.ui.statusbar.showMessage(showmsg)
                self.ui.lineEditScanStart.setText(self.folder)
            else:
                self.ui.lineEditScanStart.setText('')
                #self.ui.statusbar.showMessage(u"操作取消")
                self.ui.statusbar.showMessage(u"Operation Canceled")
        elif 1 == self.cbbox.currentIndex():
            self.scanflag = 1
            # 清空列表/Empty List
            self.files[:] = []
            #getlist = list(QtWidgets.QFileDialog.getOpenFileNames(self, u"选择文件", "e:\\"))
            getlist = list(QtWidgets.QFileDialog.getOpenFileNames(self, u"Select File", "e:\\"))
            if getlist:
                for i in getlist:
                    i = str(i).decode('utf-8')
                    self.files.append(i)
                #showmsg = u"已选择待扫描文件"
                showmsg = u"Select Files to be Scanned"
                self.ui.statusbar.showMessage(showmsg)
                self.ui.lineEditScanStart.setText(showmsg)
            else:
                self.ui.lineEditScanStart.setText('')
                #self.ui.statusbar.showMessage(u"操作取消")
                self.ui.statusbar.showMessage(u"Operation Canceled")
        else:
            pass
        # 选择完成后激活开始按键/Activate Start Button After Selecting Complete
        if self.ui.lineEditScanStart.text() == '':
                self.ui.PB_Start.setEnabled(False)
                return
        self.ui.PB_Start.setEnabled(True)

    '''
    #扫描器起始
    Scanner Starting
    #调度扫描文件夹与扫描文件
    Scheduling Scanned Folders and Scanned Files
    #扫描文件时不受filetype选择影响
    Scanning Files Without the Filetype Selection
    #需要添加类似的调度函数
    You Need to Add a Similar Dispatch Function
    '''
    def startScan(self):
        self.ui.PB_Start.setEnabled(False)
        self.ui.PB_Clear.setEnabled(False)
        self.ui.PB_End.setEnabled(True)
        self.ui.progressBar.reset()
        #self.ui.statusbar.showMessage(u"正在初始化...")
        self.ui.statusbar.showMessage(u"Initializing...")
        FlagSet.scanstopflag = 1 # 恢复停止标识/Restore Stop Identity
        FlagSet.scandoneflag = 0 # 恢复完成标识/Restore Completion Identity
        FlagSet.scansqlcount = self.table.rowCount()
        try:
            sqlconn = sqlite3.connect("../db/fileinfo.db")
        except sqlite3.Error, e:
            print "sqlite connect failed" , "\n", e.args[0]
        sqlcursor = sqlconn.cursor()
        sqlcursor.execute("delete from base_info where md5 is NULL")#> ?", str(self.table.rowCount()),) <-warring
        sqlconn.commit()
        sqlconn.close()
        print "delete no value data over"
        # 设置左右滑动效果/Set the Left and Right Sliding Effect
        # 进度条最大最小值都为0/The Maximum Progress Bar Minimum Value is 0
        self.ui.progressBar.setMaximum(0)
        self.ui.progressBar.setValue(0)
        # 应用扫描策略/Apply Scan Policy
        self.rule, self.type = self.prevScanPrepare()
        if 0 == self.scanflag: # 选择文件夹/Select Folder
            self.depth = self.ui.spinBox.value()
            print "start: " + str(self.folder).decode('utf-8')
            if self.folder != '':
                # send folder filetype, scanrule and folder depth to fliter
                self.folderThread = CheckFolder(self.folder, self.type, self.rule, self.depth)
                # two signals connect one slot
                self.folderThread.numberSignal.connect(self.recvInitSingal)
                self.folderThread.folderSignal.connect(self.showFileAnalyzLog)
                #执行run方法/Executing the Run Method
                self.folderThread.start()
        elif 1 == self.scanflag: # 选择文件
            if self.files:
                self.filenum = len(self.files)
                # 直接连接control中的scanfile线程/Scanfile Threads in Direct Connection Control
                self.filesThread = ScanFile(self.files, self.rule)
                self.filesThread.fileSignal.connect(self.updateScanInfo) # 连到更新函数中/Connect to Update Function
                self.filesThread.smsgSignal.connect(self.updateStatusBar)
                self.filesThread.flogSignal.connect(self.showFileAnalyzLog)
                self.filesThread.start()
        else:
            pass

    def stopScan(self):
        print "stopscan"
        self.ui.PB_Start.setEnabled(True)
        self.ui.PB_Clear.setEnabled(True)
        self.ui.PB_End.setEnabled(False)
        #self.ui.statusbar.showMessage(u"手动结束扫描，等待线程退出")
        self.ui.statusbar.showMessage(u"Manual End Scan，Waiting for Threads to Quit")
        FlagSet.scanstopflag = 0

    '''
    #扫描前准备函数
    Prepare Function Before Scanning
    #负责获取所有设置并统一设置调度
    Responsible for Obtaining All Settings and Setting Up Schedules
    #返回调度结果rule[]与type[]
    Return Dispatch Result Rule[] with Type[]
    '''
    def prevScanPrepare(self):
        policy = self.getScanPolicy()
        if not any(set(policy) & set(self.typelist)):
            #self.ui.statusbar.showMessage(u"请至少选择一种类型文件")
            self.ui.statusbar.showMessage(u"Please Select at Least One Type File")
        # if "set([])" == str(set(policy) & set(self.rulelist)):
        #     self.ui.statusbar.showMessage(u"不使用拓展规则")
        #     self.ui.statusbar.showMessage(u"Do Not Use Extension Rules")
        rulepolicy = list(set(policy) & set(self.rulelist))
        typepolicy = list(set(policy) & set(self.typelist))
        return rulepolicy, typepolicy

    '''
    #接收startScan连接的子进程checkFolder返回内容
    Receive StartScan Connection Child Process CheckFolder Return Content
    #@index:区分信息索引
    @index:Differentiating Information Index
    #1-子文件夹个数
    1-Number of Subfolders
    #2-文件个数
    2-Number of Files
    #3-文件名列表
    3-File Name List
    #@msg:具体内容
    @msg:Specific Content
    '''
    def recvInitSingal(self, index, msg):
        if 1 == index:
            self.dirsnum = msg
            print "folders number is: " + self.dirsnum
        if 2 == index:
            self.filenum = msg
            print "files number is: " + self.filenum
        if 3 == index:
            scanlist = msg
            if 0 == int(self.filenum):
                #self.ui.statusbar.showMessage(u"未检索到符合条件的文件，扫描结束")
                self.ui.statusbar.showMessage(u"No Eligible Files Retrieved，Scan Ended")
                self.ui.progressBar.setMaximum(1)
                self.ui.progressBar.setValue(1)
                FlagSet.scandoneflag = 1
                self.ui.PB_Start.setEnabled(True)
                self.ui.PB_Clear.setEnabled(True)
                self.ui.PB_End.setEnabled(False)
                return
            if 0 == FlagSet.scanstopflag:
                #self.ui.statusbar.showMessage(u"扫描初始化已停止")
                self.ui.statusbar.showMessage(u"Scan Initialization Stopped")
                self.ui.progressBar.setMaximum(1)
                self.ui.progressBar.setValue(1)
                return
            # 扫描线程准备工作 第一版 发列表/Scan Thread Preparation First Edition List
            # 下一版可以考虑不发文件名list/The Next Edition Can Consider Not Sending a Filename List
            # 3月2日更新配合多文件选择使用，暂不修改/March 2 Update with Multiple File Selection, Not Modified
            # 3月27日更改为读写数据库/March 27 Change to Read and Write Database
            self.scanThread = ScanFile(int(self.filenum), self.rule)
            self.scanThread.fileSignal.connect(self.updateScanInfo) # 连到更新函数中/Connect to Update Function
            self.scanThread.smsgSignal.connect(self.updateStatusBar)
            self.scanThread.flogSignal.connect(self.showFileAnalyzLog)
            self.scanThread.start()

    '''
    #可对应添加scanfile信号发射的参数
    Can Correspond to Add Scanfile Signal Emission Parameters
    #@msg:文件绝对路径，将分割为文件名+路径
    @msg: File Absolute Path, Divide into Filename + Path
    #@文件类型
    @File Type
    #@文件日期
    @File Date
    #@文件大小
    @File Size
    #@文件MD5
    @File MD5
    '''
    def updateScanInfo(self, num, msg):
        self.updateStatusBar(num, msg)
        # 更新tablewidget/Update tablewidget
        self.rowindex = FlagSet.scansqlcount
        i = self.rowindex
        # print i
        self.table.setRowCount(i)
        # 或者用insertRow/Or Use InsertRow
        sqlcursor = self.readFromDB(i)
        fid   = str(sqlcursor[0])
        fsize = str(sqlcursor[2])
        ftype = str(sqlcursor[3])
        ftime = self.convertTime(sqlcursor[4])
        fMD5  = str(sqlcursor[5])
        mark  = str(sqlcursor[7]).decode('utf-8')
        p, f  = os.path.split(str(sqlcursor[1]).decode('utf-8')) # 分割文件路径与文件名/Split File Path and Filename
        self.table.setItem(i - 1, 0, QtWidgets.QTableWidgetItem(f))
        self.table.setItem(i - 1, 1, QtWidgets.QTableWidgetItem(p))
        sizeitem = QtWidgets.QTableWidgetItem(fsize+"  ")
        # 设置单元内容对齐方式/Set Cell Content Alignment
        if int(fsize) > 100*1024*1024:
            sizeitem.setForeground(QtCore.Qt.red)
        sizeitem.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.table.setItem(i - 1, 2, sizeitem)
        self.table.setItem(i - 1, 3, QtWidgets.QTableWidgetItem(ftype))
        detection = self.convertSocre2Rank(sqlcursor[6])
        self.table.setItem(i - 1, 4, detection)
        self.table.setItem(i - 1, 5, QtWidgets.QTableWidgetItem(mark))
        self.table.setItem(i - 1, 6, ftime)
        self.table.setItem(i - 1, 7, QtWidgets.QTableWidgetItem(fMD5))
        self.table.setItem(i - 1, 8, QtWidgets.QTableWidgetItem(fid))

    '''
    #更新重新扫描返回事件
    Update Rescan Return Events
    '''
    def updateRescanInfo(self, num, msg):
        self.updateStatusBar(int(msg), msg)
        # 更改tablewidget内容/Change tablewidget Content
        infos = self.readFromDB(num + 1)
        print infos
        line = -1
        for i in range(self.table.rowCount()):
            if int(self.table.item(i, 8).text()) == num:
                line = i
        if -1 == line:
            print "sql id error"
            return
        detection = self.convertSocre2Rank(infos[6])
        dtime     = self.convertTime(infos[4])
        mark      = str(infos[7]).decode('utf-8')
        self.table.setItem(line, 4, detection)
        self.table.setItem(line, 5, QtWidgets.QTableWidgetItem(mark))
        self.table.setItem(line, 6, dtime)

    '''
    #读取数据库信息
    Reading Database Information
    #更新tablewidget显示
    Update tablewidget Display
    '''
    def readFromDB(self, index):
        i = index
        try:
            sqlconn = sqlite3.connect("../db/fileinfo.db")
        except sqlite3.Error, e:
            print "sqlite connect failed" , "\n", e.args[0]
        sqlcursor = sqlconn.cursor()
        sqlcursor.execute("select * from base_info where id =?", (int(i-1),))
        sqlconn.commit()
        sqlcursor = sqlcursor.fetchone()
        sqlconn.close()
        return sqlcursor

    '''
    #更新进度条函数
    Update Progress Bar Function
    '''
    def updateStatusBar(self, num, msg):
        if -1 == num: # 显示yara规则库的检查信息/Displaying Check Information for the Yara Rule Library
            self.ui.statusbar.showMessage(msg)
            self.ui.progressBar.setMaximum(0)
            self.ui.progressBar.setValue(0)
            return # 没有return进度条不会左右移动/No Return Progress Bar Will Not Move Around
        showmsg = 'recv result from file: ' + msg
        self.ui.statusbar.showMessage(showmsg)
        # 更新进度条 最大值和当前值放在一起/Update Progress Bar Maximum and Current Value
        self.ui.progressBar.setMaximum(int(self.filenum))
        self.ui.progressBar.setValue(num)
        if int(self.filenum) == num:
            #self.ui.statusbar.showMessage(u"扫描结束")
            self.ui.statusbar.showMessage(u"Scan Ended")
            FlagSet.scandoneflag = 1
            self.ui.PB_Start.setEnabled(True)
            self.ui.PB_Clear.setEnabled(True)
            self.ui.PB_End.setEnabled(False)

    def updateTableMsg(self):
        pass

    '''
    #数据库模糊查询
    Database Fuzzy Query
    #@flag:查询标记 1-执行查询 0-恢复内容 2-历史记录查询
    @flag: Query Mark 1-Execute Query 0-Resume Content 2-History Query
    '''
    def queryDBOperate(self, flag):
        print flag
        # 构造模糊查询条件
        # Constructed Fuzzy Query Conditions
        # 默认赋值tab1内容/Default Assignment tab1 Content
        sql = unicode("'%" + str(self.fuzzy.text()) + "%'")
        condition = unicode(self.ui.comboBox_2.currentText())
        dbname = "../db/fileinfo.db"
        if 2 == flag:
            sql = unicode("'%" + str(self.ui.LE_FuzzyHistory.text()) + "%'")
            condition = condition = unicode(self.ui.comboBox_3.currentText())
            dbname = self.historydb
        try:
            sqlconn = sqlite3.connect(dbname)
        except sqlite3.Error, e:
            print "sqlite connect failed" , "\n", e.args[0]
        sqlcursor = sqlconn.cursor()
        if 0 == flag:
            sqlcursor.execute("select * from base_info where md5 not NULL")
        elif 1 == flag or 2 == flag:
            sqlcursor.execute("select * from base_info where " + condition + " like " + sql)
        else:
            print "database query flag error"
            return
        sqlconn.commit()
        i = 0
        for raw in sqlcursor:
            i += 1
            if 2 == flag:
                self.updateFromHistoryDB(i, raw)
                continue
            self.updateFromDBInit(i, raw)
        sqlconn.close()

    '''
    #初始化时从数据库中读取内容并更新
    Reads and Updates Content from the Database when Initializing
    #msg:数据库查询返回元组
    msg:Database Query Returns Tuples
    '''
    def updateFromDBInit(self, index, msg):
        info  = msg
        # index = info[0] + 1 # index标记
        self.table.setRowCount(index)
        p, f  = os.path.split(str(info[1]).decode('utf-8'))
        fid   = str(info[0])
        size  = str(info[2])
        ftype = str(info[3])
        ftime = float(info[4])
        md5   = str(info[5])
        score = int(info[6])
        mark  = str(info[7]).decode('utf-8')
        index -= 1
        dtime = self.convertTime(ftime)
        # self.table.setItem(index - 1, 0, QtWidgets.QTableWidgetItem(f))
        self.table.setItem(index, 0, QtWidgets.QTableWidgetItem(f))
        self.table.setItem(index, 1, QtWidgets.QTableWidgetItem(p))
        sizeitem = QtWidgets.QTableWidgetItem(size+"  ")
        if int(size) > 100*1024*1024:
            sizeitem.setForeground(QtCore.Qt.red)
        detection = self.convertSocre2Rank(score)
        self.table.setItem(index, 4, detection)
        sizeitem.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.table.setItem(index, 5, QtWidgets.QTableWidgetItem(mark))
        self.table.setItem(index, 2, QtWidgets.QTableWidgetItem(sizeitem))
        self.table.setItem(index, 3, QtWidgets.QTableWidgetItem(ftype))
        self.table.setItem(index, 6, dtime)
        self.table.setItem(index, 7, QtWidgets.QTableWidgetItem(md5))
        self.table.setItem(index, 8, QtWidgets.QTableWidgetItem(fid))

    '''
    #转换score数值与评判结果
    Converting Score Numeric and Judging Results
    '''
    def convertSocre2Rank(self, score):
        if score >= 15:
            #detection = QtWidgets.QTableWidgetItem(u"危险 - " + str(score))
            detection = QtWidgets.QTableWidgetItem(str(score) + u" - Dangerous")
            detection.setForeground(QtCore.Qt.red)
        if score >= 10 and score < 15:
            #detection = QtWidgets.QTableWidgetItem(u"可疑 - " + str(score))
            detection = QtWidgets.QTableWidgetItem(str(score) + u" - Suspicious")
            detection.setForeground(QtCore.Qt.darkRed)
        if score >= 5 and score < 10:
            #detection = QtWidgets.QTableWidgetItem(u"常规 - " + str(score))
            detection = QtWidgets.QTableWidgetItem(str(score) + u" - Security")
            detection.setForeground(QtCore.Qt.darkYellow)
        if score < 5 and score >=0:
            #detection = QtWidgets.QTableWidgetItem(u"安全 - " + str(score))
            detection = QtWidgets.QTableWidgetItem(str(score) + u" - Info")
            detection.setForeground(QtCore.Qt.green)
        if score < 0:
            #detection = QtWidgets.QTableWidgetItem(u" 不支持类型 ")
            detection = QtWidgets.QTableWidgetItem(u" No Support, Yet")
            detection.setForeground(QtCore.Qt.blue)
        detection.setTextAlignment(QtCore.Qt.AlignCenter)
        return detection

    '''
    #转换时间函数
    Converting Time Functions
    '''
    def convertTime(self, intime):
        nowtime   = time.time()
        localtime = time.localtime(intime)
        midnight  = nowtime - nowtime % 86400 + time.timezone
        if intime < midnight:
            outtime = time.strftime(' %Y-%m-%d ', localtime)
        else:
            outtime = time.strftime('%H:%M:%S', localtime)
        outtime = QtWidgets.QTableWidgetItem(outtime)
        outtime.setTextAlignment(QtCore.Qt.AlignCenter)
        return outtime

    '''
    #checkbox事件
    CheckBox Events
    #@flag: 标记全选与其他
    @flag: Mark All Selected with others
    '''
    def checkBoxEvent(self, flag):
        ruleslist = [self.cbrpe, self.cbrcryp, self.cbrpack, self.cbrself, self.cbrwl]
        typeslist = [self.cbtpe, self.cbtofs, self.cbtsh, self.cbtzip, self.cbtmda, self.cbtasm]
        if flag == 0: # 对应rule全选操作/Corresponding Rule-Selection Operation
            if self.cbrall.isChecked():
                print "all rules selected"
                for i in ruleslist:
                    i.setCheckState(QtCore.Qt.Checked)
            else:
                for i in ruleslist:
                    i.setCheckState(QtCore.Qt.Unchecked)
        elif flag == 1: # 对应type全选操作/Corresponding Type Full Selection Operation
            if self.cbtall.isChecked():
                print "all type selected"
                for i in typeslist:
                    i.setCheckState(QtCore.Qt.Checked)
            else:
                for i in typeslist:
                    i.setCheckState(QtCore.Qt.Unchecked)
        else:
            if self.cbrall.isChecked() or self.cbtall.isChecked():
                if flag < 7:
                    self.cbrall.setCheckState(QtCore.Qt.Unchecked)
                else:
                    self.cbtall.setCheckState(QtCore.Qt.Unchecked)
        policy = self.getScanPolicy()
        if set(self.rulelist).issubset(set(policy)):
            self.cbrall.setCheckState(QtCore.Qt.Checked)
        if set(self.typelist).issubset(set(policy)):
            self.cbtall.setCheckState(QtCore.Qt.Checked)

    '''
    #获取数据库设置及扫描文件类型策略
    Obtaining Database Settings and Scanning File Type Policies
    #判断checkbox勾选情况
    Determine checkbox Check Case
    #默认使用内置规则检测pe文件
    Default Use of Built-In Rule Detection PE File
    #return policy列表
    Return policyList
    '''
    def getScanPolicy(self):
        policy = []
        if self.cbrall.isChecked():
            policy.append("0")
        if self.cbtall.isChecked():
            policy.append("1")
        if self.cbrpe.isChecked():
            policy.append("2")
        if self.cbrcryp.isChecked():
            policy.append("3")
        if self.cbrpack.isChecked():
            policy.append("4")
        if self.cbrself.isChecked():
            policy.append("5")
        if self.cbrwl.isChecked():
            policy.append("6")
        if self.cbtpe.isChecked():
            policy.append("7")
        if self.cbtofs.isChecked():
            policy.append("8")
        if self.cbtsh.isChecked():
            policy.append("9")
        if self.cbtzip.isChecked():
            policy.append("10")
        if self.cbtmda.isChecked():
            policy.append("11")
        if self.cbtasm.isChecked():
            policy.append("12")
        return policy

    '''
    #菜单栏点击事件响应函数
    Menu Bar Click event Response Function
    '''
    def menuBarOperate(self, index):
        print index
        if 1 == index:
            dialog = self.setdialog
            dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./UILib/icons/setting_icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            dialog.setWindowIcon(icon)
            dialog.show()
        if 2 == index:
            dialog = self.mlvddialog
            dialog.show()
        if 3 == index:
            dialog = self.wtldialog
            dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            # icon = QtGui.QIcon()
            # icon.addPixmap(QtGui.QPixmap(".\\UILib\\icons\\setting_icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            # dialog.setWindowIcon(icon)
            dialog.show()
        if 6 == index:
            dialog = self.authorinfo
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./UILib/icons/pk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            dialog.setWindowIcon(icon)
            dialog.show()

    '''
    #右键菜单生成函数
    Right-click Menu Generation Function
    #仍需完善策略
    Still Need to Refine the Strategy
    '''
    def generateMenu(self, pos):
        # 未选中元素时无法使用右键菜单/The Right-Click Menu Cannot be Used when an Element is Unchecked
        print pos # 原始坐标/Original Coordinates
        row_num = [] # 右键操作列索引列表/Right-Click the List of Column Indexes
        rid_num = [] # 右键id索引列表/Right-Key ID Index List
        for i in self.table.selectionModel().selection().indexes():
            row_num.append(i.row())
            rid_num.append(int(self.table.item(i.row(), 8).text()))
        row_num = list(set(row_num))
        rid_num = list(set(rid_num))
        # print row_num
        # print len(row_num)
        # 未选中任何一行/No Row Selected
        if len(row_num) < 1:
            return
        # 选中多行/Select Multiple Lines
        elif len(row_num) > 1:
            #print u"多选"
            print u"Multiple Selections"
            mumenu  = QtWidgets.QMenu()
            #muitem1 = mumenu.addAction(QtGui.QIcon("./UILib/icons/drescan_icon.png"), u"重新扫描")
            muitem1 = mumenu.addAction(QtGui.QIcon("./UILib/icons/drescan_icon.png"), u"ReScan")
            if 0 == FlagSet.scandoneflag:
                muitem1.setEnabled(False)
            maction = mumenu.exec_(self.table.mapToGlobal(pos))
            if maction == muitem1:
                print "get clicked"
                self.filenum = len(row_num)
                rescanfiles  = ("rescan", rid_num)
                print rescanfiles
                # 直接连接control中的scanfile线程
                # Scanfile Threads in Direct Connection Control
                self.rule, useless = self.prevScanPrepare()
                self.filesThread = ScanFile(rescanfiles, self.rule)
                self.filesThread.fileSignal.connect(self.updateRescanInfo) # 连到更行重新函数中/Connect to a More Row-Back Function
                self.filesThread.smsgSignal.connect(self.updateStatusBar)
                self.filesThread.flogSignal.connect(self.showFileAnalyzLog)
                self.filesThread.start()
        # 选中一行
        # Select One Line
        else:
            row_num = row_num[0]
            menu = QtWidgets.QMenu()
            #item1 = menu.addAction(QtGui.QIcon("./UILib/icons/detail_icon.png"), u"详细信息") # (u"详细信息")
            item1 = menu.addAction(QtGui.QIcon("./UILib/icons/detail_icon.png"), u"More Information") # (u"More Information")
            #item2 = menu.addAction(QtGui.QIcon("./UILib/icons/drescan_icon.png"), u"重新扫描")
            item2 = menu.addAction(QtGui.QIcon("./UILib/icons/drescan_icon.png"), u"ReScan")
            #advmenu = menu.addMenu(QtGui.QIcon("./UILib/icons/robot_icon.png"), u"机器学习")
            advmenu = menu.addMenu(QtGui.QIcon("./UILib/icons/robot_icon.png"), u"Machine Learning")
            #item3 = advmenu.addAction(QtGui.QIcon("./UILib/icons/img_icon.png"), u"二进制图像")
            item3 = advmenu.addAction(QtGui.QIcon("./UILib/icons/img_icon.png"), u"Binary Image")
            #item4 = advmenu.addAction(QtGui.QIcon("./UILib/icons/code_icon.png"), u"操作码分类")
            item4 = advmenu.addAction(QtGui.QIcon("./UILib/icons/code_icon.png"), u"OpCode Classification")
            #item5 = menu.addAction(QtGui.QIcon("./UILib/icons/mark_icon.png"), u"文件位置")
            item5 = menu.addAction(QtGui.QIcon("./UILib/icons/mark_icon.png"), u"Open Location")
            #item6 = menu.addAction(QtGui.QIcon("./UILib/icons/user_icon.png"), u"用户标记")
            item6 = menu.addAction(QtGui.QIcon("./UILib/icons/user_icon.png"), u"User Tags")
            #item7 = menu.addAction(QtGui.QIcon("./UILib/icons/upload_icon.png"), u"上传样本")
            item7 = menu.addAction(QtGui.QIcon("./UILib/icons/upload_icon.png"), u"Upload Sample")
            #item8 = menu.addAction(QtGui.QIcon("./UILib/icons/upload_icon.png"), u"上传样本")
            item8 = menu.addAction(QtGui.QIcon("./UILib/icons/dbg_icon.png"), u"Debug Sample")
            fname = self.table.item(row_num, 0).text()
            fpath = self.table.item(row_num, 1).text()
            ffull = os.path.join(str(fpath), str(fname)) # 文件绝对路径/File Absolute Path
            fmd5  = self.table.item(row_num, 7).text()
            if 0 == FlagSet.scandoneflag:
                item2.setEnabled(False)
                item6.setEnabled(False)
            # if 'PE32' not in self.table.item(row_num, 3).text() and 'executable' not in self.table.item(row_num, 3).text():
            # 更改为png图片及可执行文件都触发/Change to PNG Picture and Executable File Trigger
            ext = os.path.splitext(str(fname))[1]
            if 'executable' not in self.table.item(row_num, 3).text() and 'png' not in ext:
                item3.setEnabled(False)
            if not str(self.table.item(row_num, 0).text()).endswith('.asm'):
                item4.setEnabled(False)
            action = menu.exec_(self.table.mapToGlobal(pos))
            if action == item1:
                # print u'您选了选项一，当前行文字内容是：', self.table.item(row_num, 0).text()
                # print u'You Chose the Option 一，The current line text content is：', self.table.item(row_num, 0).text()
                print ffull
                filedetail = self.detailDialog
                filedetail.getFileName(ffull, fmd5)
                filedetail.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("./UILib/icons/detail_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                filedetail.setWindowIcon(icon)
                filedetail.show()
            elif action == item2:
                self.filenum = 1
                rescan = []
                reid = int(self.table.item(row_num, 8).text())
                rescan.append(reid)
                rescanfiles = ("rescan", rescan)
                print rescanfiles
                # 直接连接control中的scanfile线程/Scanfile Threads in Direct Connection Control
                self.rule, useless = self.prevScanPrepare()
                self.filesThread = ScanFile(rescanfiles, self.rule)
                self.filesThread.fileSignal.connect(self.updateRescanInfo) # 连到更行重新函数中/Connect to a More Row-Back Function
                self.filesThread.smsgSignal.connect(self.updateStatusBar)
                self.filesThread.flogSignal.connect(self.showFileAnalyzLog)
                self.filesThread.start()
            elif action == item3:
                print "going to create a pe image"
                malimgclass = self.malimgDialog
                malimgclass.getFileName(ffull)
                malimgclass.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("./UILib/icons/img_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                malimgclass.setWindowIcon(icon)
                malimgclass.show()
            elif action == item4:
                print "going to analysis asm file"
                opcodeclass = self.opcodeDialog
                opcodeclass.getFileName(ffull)
                opcodeclass.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("./UILib/icons/code_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                opcodeclass.setWindowIcon(icon)
                opcodeclass.show()
            elif action == item5:
                #print u"打开文件所在位置"
                print u"Open File Location"
                fname = self.table.item(row_num, 0).text()
                fpath = self.table.item(row_num, 1).text()
                #ffull = os.path.join(str(fpath), str(fname)) #.encode('cp936'), str(fname).encode('cp936'))
                # 仅打开文件夹/Open Folder Only
                # os.startfile(fpath)
                # 打开文件-慎重/Open File-Safely
                # os.startfile(ffull)
                # 打开文件夹并定位到文件/Open a Folder and Navigate to a File
                print str(ffull) #.encode('cp936')
		        estr = 'open /System/Library/CoreServices/Finder.app ' + str(fpath) #.encode('cp936')
                #estr = 'explorer /select,' + str(ffull) #.encode('cp936')
		        #estr = 'nautilus ' + str(fpath)
                os.system(estr)
            elif action == item6:
                # 设置item可编辑/Set Item to Edit
                self.table.editItem(self.table.item(row_num, 5))
                self.enter = row_num
                #self.ui.statusbar.showMessage(u"修改后按回车更新标记内容")
                self.ui.statusbar.showMessage(u"Update Tagged Content by Carriage Return after Modification")
            elif action == item7:
                # 在没有数据库的情况下
                # In Case of No Database
                # 如果前后两次打开同一个文件，那么不清空内容
                # If You Open the Same File Two Times Before and After, Not Emptying the Content
                # 否则执行clear方法
                # Otherwise Executing the Clear Method
                flist = self.flist # 文件名列表/List of File Names
                flist.append(fmd5)
                print flist
                dialog = self.uploadDialog
                dialog.getFilename(ffull)
                if len(flist) == 2:
                    if flist[0] != flist[1]:
                        dialog.clearFileData()
                    del flist[0]
                print flist
                dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("./UILib/icons/upload_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                dialog.setWindowIcon(icon)
                dialog.show()
            elif action == item8:
                #print u"打开文件所在位置"
                print u"Debug Sample"
                fname = self.table.item(row_num, 0).text()
                fpath = self.table.item(row_num, 1).text()
                ffull = os.path.join(str(fpath), str(fname)) #.encode('cp936'), str(fname).encode('cp936'))
                # 仅打开文件夹/Open Folder Only
                # os.startfile(fpath)
                # 打开文件-慎重/Open File-Safely
                # os.startfile(ffull)
                # 打开文件夹并定位到文件/Open a Folder and Navigate to a File
                print str(ffull) #.encode('cp936')
                # LLDB
                #self.ui.tab_4.sendText('lldb ' + str(ffull) + '\r')
                # GDB
                #self.ui.tab_4.sendText('gdb ' + str(ffull) + '\r')
                # Radare2
                self.ui.tab_4.sendText('r2 ' + str(ffull) + '\r')
                # Voltron
                #self.ui.tab_4.sendText('voltron ' + str(ffull) + '\r')
                #os.system(estr)
            else:
                return

    '''
    #表头点击事件
    Table Header Click Event
    #index:表头section索引值
    Table Header Section Index Value
    '''
    def tableHeaderEvent(self, index):
        if 0 == FlagSet.scansqlcount:
            return
        self.table.horizontalHeader().setSortIndicatorShown(True)
        if 0 == index:
            #print u"按文件名排序"
            print u"Sort by Filename"
            sortflag = self.table.horizontalHeader().sortIndicatorOrder()
            print sortflag
            self.table.sortByColumn(index, sortflag)
        elif 1 == index:
            #print u"按文件路径排序"
            print u"Sort by File Path"
            sortflag = self.table.horizontalHeader().sortIndicatorOrder()
            print sortflag
            self.table.sortByColumn(index, sortflag)
        elif 2 == index:
            #print u"按文件大小排序，单位Bytes"
            print u"Sort by File Size，Unit Bytes"
            sortflag = self.table.horizontalHeader().sortIndicatorOrder()
            print sortflag
            self.sortByFileSize(sortflag)
        elif 3 == index:
            #print u"按文件类型排序"
            print u"Sort by File Type"
            sortflag = self.table.horizontalHeader().sortIndicatorOrder()
            print sortflag
            self.table.sortByColumn(index, sortflag)
        elif 4 == index:
            #print u"按扫描结果排序"
            print u"Sort by Scan Results"
            sortflag = self.table.horizontalHeader().sortIndicatorOrder()
            print sortflag
            self.table.sortByColumn(index, sortflag)
        elif 5 == index:
            #print u"按标记排序"
            print u"Sort by Tag"
            sortflag = self.table.horizontalHeader().sortIndicatorOrder()
            print sortflag
            self.table.sortByColumn(index, sortflag)
        elif 6 == index:
            #print u"按分析日期排序"
            print u"Sort by Analysis Date"
            sortflag = self.table.horizontalHeader().sortIndicatorOrder()
            print sortflag
            self.table.sortByColumn(index, sortflag)
        elif 7 == index:
            #print u"按MD5值排序"
            print u"Sort by MD5 Value"
            sortflag = self.table.horizontalHeader().sortIndicatorOrder()
            print sortflag
            self.table.sortByColumn(index, sortflag)
        else:
            self.table.horizontalHeader().setSortIndicatorShown(False)
            pass

    '''
    #tablewidget表头点击事件
    tablewidget Table Header Click Event
    #文件大小排序数据库操作
    File Size Sorting Database Operations
    '''
    def sortByFileSize(self, flag):
        try:
            sqlconn = sqlite3.connect("../db/fileinfo.db")
        except sqlite3.Error, e:
            print "sqlite connect failed" , "\n", e.args[0]
        sqlcursor = sqlconn.cursor()
        if 0 == flag:
            sqlcursor.execute("select * from base_info where md5 not NULL order by size")
        elif 1 == flag:
            sqlcursor.execute("select * from base_info where md5 not NULL order by size desc")
        else:
            print "sort flag error, quit..."
            sqlconn.close()
            return
        sqlconn.commit()
        i = 0
        for raw in sqlcursor:
            i += 1
            self.updateFromDBInit(i, raw)
        sqlconn.close()

    '''
    #清空tablewidget内容
    Empty tablewidget Content
    '''
    def clearTableWidget(self):
        print self.table.rowCount()
        print "clear tablewidget"
        self.table.setRowCount(0)
        self.table.clearContents()
        self.rowindex = 0 # 让新元素从第一行开始/Let the New Element Start from the First Line
        self.ui.progressBar.setValue(0) # 进度条回0/Progress Bar Return 0
        #self.ui.statusbar.showMessage(u"已清空显示列表内容")
        self.ui.statusbar.showMessage(u"Empty Display list Contents")
        try:
            sqlconn = sqlite3.connect("../db/fileinfo.db")
        except sqlite3.Error, e:
            print "sqlite connect failed" , "\n", e.args[0]
        sqlcursor = sqlconn.cursor()
        sqlcursor.execute("delete from base_info where id >= 0")
        sqlconn.commit()
        sqlconn.close()
        FlagSet.scansqlcount = 0 # 将全局计数flag置0/Counting Global flag 置0
        self.table.horizontalHeader().setSortIndicatorShown(False)

    '''
    #保存tab页内容至历史数据库
    Save tab Page Content to History Database
    '''
    def store2DataBaseByDate(self):
        tday = datetime.today()
        y = str(tday.year)
        m = str(tday.month)
        d = str(tday.day)
        src = "../db/fileinfo.db"
        dst = "../db/history/" + y + m + d + ".db"
        print src, dst
        shutil.copy(src, dst)
        if os.path.isfile(dst):
            self.ui.statusbar.showMessage(u"本页内容已保存至" + dst)
            self.ui.statusbar.showMessage(u"The contents of this page have been saved to" + dst)

    #------------------------------tab2-----------------------------
    '''
    #文件分析日志显示
    File Analysis Log Display
    #@flag:标记-暂未使用
    @flag:Tags-Temporarily Unused
    #@msg:接收内容
    @msg:Receive Content
    '''
    def showFileAnalyzLog(self, flag, msg):
        nowtime = time.localtime(time.time())
        nowtime = time.strftime('%Y-%m-%d %H:%M:%S', nowtime)
        nowtime = "[" + nowtime + "]  "
        self.text.append(nowtime + msg)

    '''
    #清除历史分析
    Clear Historical Analysis
    '''
    def clearAnalysisLog(self):
        self.text.clear()
        self.showFileAnalyzLog(4, " clear all information")

    '''
    #保存分析结果
    Save Analysis Results
    #使用qtextstream流写入文件
    Use qtextstream Stream Writes File
    '''
    def saveAnalysisLog(self):
        tday = datetime.today()
        y = str(tday.year)
        m = str(tday.month)
        d = str(tday.day)
        H = str(tday.hour)
        M = str(tday.minute)
        S = str(tday.second)
        name = "../log/{}-{}-{}_{}-{}-{}.analy".format(y, m, d, H, M, S)
        try:
            ftmp = QtCore.QFile(name)
            ftmp.open(QtCore.QIODevice.WriteOnly)
            stream = QtCore.QTextStream(ftmp)
            slog = self.text.toPlainText()
            stream << slog
            #self.ui.statusbar.showMessage(u"扫描报告保存成功")
            self.ui.statusbar.showMessage(u"Scan Report Saved Successfully")
        except IOError, e:
            print e.args[0]

    #------------------------------tab3-----------------------------
    '''
    #显示分析历史信息
    Displaying Profiling History Information
    #获取日历控件响应
    Get the Calendar Control Response
    '''
    def getCalenderDate(self):
        qdate = self.calender.selectedDate()
        y = str(qdate.year())
        m = str(qdate.month())
        d = str(qdate.day())
        #flogs = "{}年{}月{}日文件分析记录".format(y, m, d)
        flogs = "{} Year{} Month{} File Analysis Record".format(y, m, d)
        fname = "../db/history/" + y + m + d + ".db"
        self.historydb = fname
        if not os.path.isfile(fname):
            #self.ui.statusbar.showMessage(u"无此日分析历史记录")
            self.ui.statusbar.showMessage(u"No History of this Day Analysis")
            self.ui.PB_SelectHistory.setEnabled(False)
            self.table2.setRowCount(0)
            self.table2.clearContents()
            return
        self.ui.PB_SelectHistory.setEnabled(True)
        try:
            sqlconn = sqlite3.connect(fname)
        except sqlite3.Error, e:
            print "sqlite connect failed" , "\n", e.args[0]
        self.ui.statusbar.showMessage(unicode(flogs))
        sqlcursor = sqlconn.cursor()
        sqlcursor.execute("select * from base_info where md5 not NULL")
        sqlconn.commit()
        i = 0
        for raw in sqlcursor:
            i += 1
            self.updateFromHistoryDB(i, raw)
        sqlconn.close()

    '''
    #显示历史分析数据库内容
    Displaying Historical Profiling Database Content
    #@index:table索引
    @index:tableIndex
    #@msg:查询记录
    @msg:Query Records
    '''
    def updateFromHistoryDB(self, index, msg):
        info  = msg
        # index = info[0] + 1 # index标记
        self.table2.setRowCount(index)
        p, f  = os.path.split(str(info[1]).decode('utf-8'))
        size  = str(info[2])
        ftype = str(info[3])
        ftime = float(info[4])
        md5   = str(info[5])
        score = int(info[6])
        mark  = str(info[7]).decode('utf-8')
        index -= 1
        dtime = self.convertTime(ftime)
        # self.table.setItem(index - 1, 0, QtWidgets.QTableWidgetItem(f))
        self.table2.setItem(index, 0, QtWidgets.QTableWidgetItem(f))
        self.table2.setItem(index, 1, QtWidgets.QTableWidgetItem(p))
        sizeitem = QtWidgets.QTableWidgetItem(size+"  ")
        if int(size) > 100*1024*1024:
            sizeitem.setForeground(QtCore.Qt.red)
        detection = self.convertSocre2Rank(score)
        self.table2.setItem(index, 4, detection)
        sizeitem.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.table2.setItem(index, 5, QtWidgets.QTableWidgetItem(mark))
        self.table2.setItem(index, 2, QtWidgets.QTableWidgetItem(sizeitem))
        self.table2.setItem(index, 3, QtWidgets.QTableWidgetItem(ftype))
        self.table2.setItem(index, 6, dtime)
        self.table2.setItem(index, 7, QtWidgets.QTableWidgetItem(md5))

    #------------------------------event-----------------------------
    '''
    #重写键盘响应事件
    Override Keyboard Response Events
    '''
    def keyPressEvent(self, event):
        if QtCore.Qt.Key_Enter and self.enter > -1:
            mark = unicode(self.table.item(self.enter, 5).text())
            tid  = int(self.table.item(self.enter, 8).text())
            # print mark, tid
            try:
                sqlconn = sqlite3.connect("../db/fileinfo.db")
            except sqlite3.Error, e:
                print "sqlite connect failed" , "\n", e.args[0]
            sqlcursor = sqlconn.cursor()
            sqlcursor.execute("update base_info set mark=? where id=?", (mark, tid))
            sqlconn.commit()
        self.enter = -1
        #self.ui.statusbar.showMessage(u"用户标记已更新")
        self.ui.statusbar.showMessage(u"User Tag Updated")

    '''
    #重写窗口关闭事件
    Override Window Shutdown Events
    '''
    def closeEvent(self, event):
        # 无数据时直接退出/Direct Exit when Countless
        if 0 == FlagSet.scansqlcount:
            return
        quitbtn = QtWidgets.QMessageBox()
        # quitbtn.setButtonText(quitbtn.Yes, u"llaalf")
        #recv = quitbtn.question(self, u"退出", u"是否保存当前信息", \
        recv = quitbtn.question(self, u"Exit", u"Save Current Information", \
                                                        quitbtn.Yes, \
                                                        quitbtn.No, \
                                                        quitbtn.Cancel )
        if recv == quitbtn.No:
            try:
                sqlconn = sqlite3.connect("../db/fileinfo.db")
            except sqlite3.Error, e:
                print "sqlite connect failed" , "\n", e.args[0]
            sqlcursor = sqlconn.cursor()
            sqlcursor.execute("delete from base_info where id >= 0")
            sqlconn.commit()
            sqlconn.close()
        elif recv == quitbtn.Yes:
            print "saved"
            pass
            # 下次开启窗口读取数据库count并传给sqlconunt/Next open Window Read Database Count and Pass to sqlconunt
        else:
            event.ignore()

    '''
    #窗口打开事件
    Window Open Event
    '''
    def showEvent(self, event):
        try:
            sqlconn = sqlite3.connect("../db/fileinfo.db")
        except sqlite3.Error, e:
            print "sqlite connect failed" , "\n", e.args[0]
        sqlcursor = sqlconn.cursor()
        sqlcursor.execute("select * from base_info where md5 not NULL")
        sqlconn.commit()
        i = 0
        for raw in sqlcursor:
            i += 1
            self.updateFromDBInit(i, raw)
        sqlconn.close()
        print self.table.rowCount()
        FlagSet.scansqlcount = self.table.rowCount() # 为打开窗口不清数据做准备/Preparing to Open the Window's Data
        # 加载白名单/Load Whitelist
        f = open(FilePath.whitelist, "r")
        f.readline()
        for line in f:
            FilePath.whitefile.append(str(line).split('\n')[0])

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWindow()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("./UILib/icons/main_icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    myapp.setWindowIcon(icon)
    myapp.show()

    sys.exit(app.exec_())
