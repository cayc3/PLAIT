# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'malimg.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        Dialog.resize(570, 530)
        Dialog.setMinimumSize(QtCore.QSize(570, 530))
        Dialog.setMaximumSize(QtCore.QSize(570, 530))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.LB_Malimg = QtWidgets.QLabel(self.groupBox)
        self.LB_Malimg.setMaximumSize(QtCore.QSize(253, 237))
        self.LB_Malimg.setText(_fromUtf8(""))
        self.LB_Malimg.setObjectName(_fromUtf8("LB_Malimg"))
        self.verticalLayout_2.addWidget(self.LB_Malimg)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_3.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_3.addWidget(self.label_3)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_4.setMaximumSize(QtCore.QSize(253, 480))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_4.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_4.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_4.addWidget(self.label_6)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.verticalLayout.setStretch(0, 3)
        self.horizontalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        #Dialog.setWindowTitle(_translate("Dialog", "二进制文件图像分类", None))
        Dialog.setWindowTitle(_translate("Dialog", "Binary Image Classification", None))
        #self.groupBox.setTitle(_translate("Dialog", "二进文件制图像", None))
        self.groupBox.setTitle(_translate("Dialog", "Binary Image", None))
        #self.groupBox_3.setTitle(_translate("Dialog", "机器学习分类结果", None))
        self.groupBox_3.setTitle(_translate("Dialog", "Classification Results of Machine Learning", None))
        self.label.setText(_translate("Dialog", "TextLabel", None))
        self.label_2.setText(_translate("Dialog", "TextLabel", None))
        self.label_3.setText(_translate("Dialog", "TextLabel", None))
        #self.groupBox_2.setTitle(_translate("Dialog", "相似图像对比", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Image Congruency", None))
        #self.groupBox_4.setTitle(_translate("Dialog", "相似的图像", None))
        self.groupBox_4.setTitle(_translate("Dialog", "Congruent Images", None))
        self.label_4.setText(_translate("Dialog", "TextLabel", None))
        self.label_5.setText(_translate("Dialog", "TextLabel", None))
        self.label_6.setText(_translate("Dialog", "TextLabel", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
