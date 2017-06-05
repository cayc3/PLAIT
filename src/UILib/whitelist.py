# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'whitelist.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(363, 458)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setReadOnly(False)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.PB_Apply = QtWidgets.QPushButton(Dialog)
        self.PB_Apply.setObjectName(_fromUtf8("PB_Apply"))
        self.horizontalLayout.addWidget(self.PB_Apply)
        self.PB_OK = QtWidgets.QPushButton(Dialog)
        self.PB_OK.setObjectName(_fromUtf8("PB_OK"))
        self.horizontalLayout.addWidget(self.PB_OK)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "白名单设置", None))
        Dialog.setWindowTitle(_translate("Dialog", "Whitelist Settings", None))
        self.PB_Apply.setText(_translate("Dialog", "应  用", None))
        self.PB_Apply.setText(_translate("Dialog", "Enable", None))
        self.PB_OK.setText(_translate("Dialog", "确  定", None))
        self.PB_OK.setText(_translate("Dialog", "OK", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
