# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MS_MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1000, 620)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setMargin(1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_4.setMargin(1)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSpacing(1)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(2)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.groupBox_4 = QtGui.QGroupBox(self.tab)
        self.groupBox_4.setMaximumSize(QtCore.QSize(16777215, 200))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setMargin(1)
        self.verticalLayout_6.setSpacing(3)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setMargin(1)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_4 = QtGui.QLabel(self.groupBox_4)
        self.label_4.setMaximumSize(QtCore.QSize(70, 15))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_7.addWidget(self.label_4)
        self.CBRuleAll = QtGui.QCheckBox(self.groupBox_4)
        self.CBRuleAll.setMaximumSize(QtCore.QSize(80, 15))
        self.CBRuleAll.setChecked(False)
        self.CBRuleAll.setObjectName(_fromUtf8("CBRuleAll"))
        self.horizontalLayout_7.addWidget(self.CBRuleAll)
        self.CBRuleYara = QtGui.QCheckBox(self.groupBox_4)
        self.CBRuleYara.setMaximumSize(QtCore.QSize(85, 15))
        self.CBRuleYara.setObjectName(_fromUtf8("CBRuleYara"))
        self.horizontalLayout_7.addWidget(self.CBRuleYara)
        self.CBRuleClamav = QtGui.QCheckBox(self.groupBox_4)
        self.CBRuleClamav.setMaximumSize(QtCore.QSize(90, 15))
        self.CBRuleClamav.setObjectName(_fromUtf8("CBRuleClamav"))
        self.horizontalLayout_7.addWidget(self.CBRuleClamav)
        self.CBRulePEiD = QtGui.QCheckBox(self.groupBox_4)
        self.CBRulePEiD.setMaximumSize(QtCore.QSize(80, 15))
        self.CBRulePEiD.setObjectName(_fromUtf8("CBRulePEiD"))
        self.horizontalLayout_7.addWidget(self.CBRulePEiD)
        self.CBRuleSelf = QtGui.QCheckBox(self.groupBox_4)
        self.CBRuleSelf.setMaximumSize(QtCore.QSize(140, 15))
        self.CBRuleSelf.setObjectName(_fromUtf8("CBRuleSelf"))
        self.horizontalLayout_7.addWidget(self.CBRuleSelf)
        self.CBRuleWL = QtGui.QCheckBox(self.groupBox_4)
        self.CBRuleWL.setMaximumSize(QtCore.QSize(120, 15))
        self.CBRuleWL.setObjectName(_fromUtf8("CBRuleWL"))
        self.horizontalLayout_7.addWidget(self.CBRuleWL)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(1, 1, 2, 1)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_3 = QtGui.QLabel(self.groupBox_4)
        self.label_3.setMaximumSize(QtCore.QSize(70, 15))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_6.addWidget(self.label_3)
        self.CBTypeAll = QtGui.QCheckBox(self.groupBox_4)
        self.CBTypeAll.setMaximumSize(QtCore.QSize(80, 15))
        self.CBTypeAll.setChecked(False)
        self.CBTypeAll.setObjectName(_fromUtf8("CBTypeAll"))
        self.horizontalLayout_6.addWidget(self.CBTypeAll)
        self.CBTypePE = QtGui.QCheckBox(self.groupBox_4)
        self.CBTypePE.setMaximumSize(QtCore.QSize(70, 15))
        self.CBTypePE.setChecked(True)
        self.CBTypePE.setObjectName(_fromUtf8("CBTypePE"))
        self.horizontalLayout_6.addWidget(self.CBTypePE)
        self.CBTypeOffice = QtGui.QCheckBox(self.groupBox_4)
        self.CBTypeOffice.setMaximumSize(QtCore.QSize(90, 15))
        self.CBTypeOffice.setObjectName(_fromUtf8("CBTypeOffice"))
        self.horizontalLayout_6.addWidget(self.CBTypeOffice)
        self.CBTypeShell = QtGui.QCheckBox(self.groupBox_4)
        self.CBTypeShell.setMaximumSize(QtCore.QSize(80, 15))
        self.CBTypeShell.setObjectName(_fromUtf8("CBTypeShell"))
        self.horizontalLayout_6.addWidget(self.CBTypeShell)
        self.CBTypeZip = QtGui.QCheckBox(self.groupBox_4)
        self.CBTypeZip.setMaximumSize(QtCore.QSize(90, 15))
        self.CBTypeZip.setObjectName(_fromUtf8("CBTypeZip"))
        self.horizontalLayout_6.addWidget(self.CBTypeZip)
        self.CBTypeMedia = QtGui.QCheckBox(self.groupBox_4)
        self.CBTypeMedia.setMaximumSize(QtCore.QSize(80, 15))
        self.CBTypeMedia.setObjectName(_fromUtf8("CBTypeMedia"))
        self.horizontalLayout_6.addWidget(self.CBTypeMedia)
        self.CBTypeAsm = QtGui.QCheckBox(self.groupBox_4)
        self.CBTypeAsm.setMaximumSize(QtCore.QSize(110, 15))
        self.CBTypeAsm.setObjectName(_fromUtf8("CBTypeAsm"))
        self.horizontalLayout_6.addWidget(self.CBTypeAsm)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(1, 1, 6, 1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_5 = QtGui.QLabel(self.groupBox_4)
        self.label_5.setMaximumSize(QtCore.QSize(70, 15))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout.addWidget(self.label_5)
        self.lineEditAdvSet = QtGui.QLineEdit(self.groupBox_4)
        self.lineEditAdvSet.setObjectName(_fromUtf8("lineEditAdvSet"))
        self.horizontalLayout.addWidget(self.lineEditAdvSet)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.horizontalLayout_9.addWidget(self.groupBox_4)
        self.groupBox_3 = QtGui.QGroupBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(300, 100))
        self.groupBox_3.setMaximumSize(QtCore.QSize(700, 200))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setContentsMargins(3, 1, 3, 1)
        self.verticalLayout_5.setSpacing(3)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(self.groupBox_3)
        self.label.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.lineEditScanStart = QtGui.QLineEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditScanStart.sizePolicy().hasHeightForWidth())
        self.lineEditScanStart.setSizePolicy(sizePolicy)
        self.lineEditScanStart.setObjectName(_fromUtf8("lineEditScanStart"))
        self.horizontalLayout_3.addWidget(self.lineEditScanStart)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_2 = QtGui.QLabel(self.groupBox_3)
        self.label_2.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_4.addWidget(self.label_2)
        self.comboBox = QtGui.QComboBox(self.groupBox_3)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_4.addWidget(self.comboBox)
        spacerItem = QtGui.QSpacerItem(5, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.PB_SelectFolder = QtGui.QPushButton(self.groupBox_3)
        self.PB_SelectFolder.setMaximumSize(QtCore.QSize(100, 22))
        self.PB_SelectFolder.setObjectName(_fromUtf8("PB_SelectFolder"))
        self.horizontalLayout_4.addWidget(self.PB_SelectFolder)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.PB_Start = QtGui.QPushButton(self.groupBox_3)
        self.PB_Start.setObjectName(_fromUtf8("PB_Start"))
        self.horizontalLayout_5.addWidget(self.PB_Start)
        self.PB_Pause = QtGui.QPushButton(self.groupBox_3)
        self.PB_Pause.setObjectName(_fromUtf8("PB_Pause"))
        self.horizontalLayout_5.addWidget(self.PB_Pause)
        self.PB_End = QtGui.QPushButton(self.groupBox_3)
        self.PB_End.setObjectName(_fromUtf8("PB_End"))
        self.horizontalLayout_5.addWidget(self.PB_End)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_9.addWidget(self.groupBox_3)
        self.groupBox = QtGui.QGroupBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.PB_Clear = QtGui.QPushButton(self.groupBox)
        self.PB_Clear.setObjectName(_fromUtf8("PB_Clear"))
        self.verticalLayout_7.addWidget(self.PB_Clear)
        self.horizontalLayout_9.addWidget(self.groupBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.tableWidget = QtGui.QTableWidget(self.tab)
        self.tableWidget.setMinimumSize(QtCore.QSize(450, 280))
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.verticalLayout_3.addWidget(self.tableWidget)
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_4 = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton_5 = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButton_6 = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        self.menu_3 = QtGui.QMenu(self.menubar)
        self.menu_3.setObjectName(_fromUtf8("menu_3"))
        self.menu_4 = QtGui.QMenu(self.menubar)
        self.menu_4.setObjectName(_fromUtf8("menu_4"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName(_fromUtf8("action"))
        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setObjectName(_fromUtf8("action_2"))
        self.action_3 = QtGui.QAction(MainWindow)
        self.action_3.setObjectName(_fromUtf8("action_3"))
        self.action_4 = QtGui.QAction(MainWindow)
        self.action_4.setObjectName(_fromUtf8("action_4"))
        self.action_5 = QtGui.QAction(MainWindow)
        self.action_5.setObjectName(_fromUtf8("action_5"))
        self.action_6 = QtGui.QAction(MainWindow)
        self.action_6.setObjectName(_fromUtf8("action_6"))
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu_2.addAction(self.action_3)
        self.menu_4.addAction(self.action_4)
        self.menu_4.addAction(self.action_5)
        self.menu_4.addAction(self.action_6)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Static Malware Analysis & Report Tool", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "参数设置", None))
        self.label_4.setText(_translate("MainWindow", "扫描规则：", None))
        self.CBRuleAll.setText(_translate("MainWindow", "全选", None))
        self.CBRuleYara.setText(_translate("MainWindow", "YARA", None))
        self.CBRuleClamav.setText(_translate("MainWindow", "Clamav", None))
        self.CBRulePEiD.setText(_translate("MainWindow", "PEiD", None))
        self.CBRuleSelf.setText(_translate("MainWindow", "自定义规则", None))
        self.CBRuleWL.setText(_translate("MainWindow", "启用白名单", None))
        self.label_3.setText(_translate("MainWindow", "文件类型：", None))
        self.CBTypeAll.setText(_translate("MainWindow", "全选", None))
        self.CBTypePE.setText(_translate("MainWindow", "PE", None))
        self.CBTypeOffice.setText(_translate("MainWindow", "Office", None))
        self.CBTypeShell.setText(_translate("MainWindow", "脚本", None))
        self.CBTypeZip.setText(_translate("MainWindow", "压缩包", None))
        self.CBTypeMedia.setText(_translate("MainWindow", "多媒体", None))
        self.CBTypeAsm.setText(_translate("MainWindow", "asm文件", None))
        self.label_5.setText(_translate("MainWindow", "高级设置：", None))
        self.lineEditAdvSet.setText(_translate("MainWindow", "当前未设置", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "操作区域", None))
        self.label.setText(_translate("MainWindow", "扫描起始：", None))
        self.label_2.setText(_translate("MainWindow", "扫描策略：", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "文件夹扫描", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "多文件扫描", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "自定义扫描", None))
        self.PB_SelectFolder.setText(_translate("MainWindow", "选择目标", None))
        self.PB_Start.setText(_translate("MainWindow", "开  始", None))
        self.PB_Pause.setText(_translate("MainWindow", "暂  停", None))
        self.PB_End.setText(_translate("MainWindow", "结  束", None))
        self.groupBox.setTitle(_translate("MainWindow", "显示策略", None))
        self.PB_Clear.setText(_translate("MainWindow", "清  空", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Path", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Size", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Type", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Detection", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Mark", None))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "AnalysisDate", None))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "MD5", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "GroupBox", None))
        self.pushButton_4.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_6.setText(_translate("MainWindow", "PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))
        self.menu.setTitle(_translate("MainWindow", "管理", None))
        self.menu_2.setTitle(_translate("MainWindow", "文件", None))
        self.menu_3.setTitle(_translate("MainWindow", "高级设置", None))
        self.menu_4.setTitle(_translate("MainWindow", "帮助", None))
        self.action.setText(_translate("MainWindow", "自动启动", None))
        self.action_2.setText(_translate("MainWindow", "啦啦啦", None))
        self.action_3.setText(_translate("MainWindow", "读取配置", None))
        self.action_4.setText(_translate("MainWindow", "版本信息", None))
        self.action_5.setText(_translate("MainWindow", "关于软件", None))
        self.action_6.setText(_translate("MainWindow", "联系作者", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

