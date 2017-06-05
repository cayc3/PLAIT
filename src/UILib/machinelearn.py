# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'machinelearn.ui'
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
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(621, 486)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.PB_ConfMatrix = QtWidgets.QPushButton(Dialog)
        self.PB_ConfMatrix.setObjectName(_fromUtf8("PB_ConfMatrix"))
        self.horizontalLayout.addWidget(self.PB_ConfMatrix)
        self.PB_CrossVad = QtWidgets.QPushButton(Dialog)
        self.PB_CrossVad.setObjectName(_fromUtf8("PB_CrossVad"))
        self.horizontalLayout.addWidget(self.PB_CrossVad)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.frame = QtWidgets.QFrame(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout.addWidget(self.frame)
        self.LB_VadRst = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LB_VadRst.sizePolicy().hasHeightForWidth())
        self.LB_VadRst.setSizePolicy(sizePolicy)
        self.LB_VadRst.setObjectName(_fromUtf8("LB_VadRst"))
        self.verticalLayout.addWidget(self.LB_VadRst)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        #Dialog.setWindowTitle(_translate("Dialog", "机器学习验证", None))
        Dialog.setWindowTitle(_translate("Dialog", "Machine Learning Validation", None))
        #self.label.setText(_translate("Dialog", "分类器：", None))
        self.label.setText(_translate("Dialog", "Classifier：", None))
        #self.comboBox.setItemText(0, _translate("Dialog", "随机森林", None))
        self.comboBox.setItemText(0, _translate("Dialog", "Stochastic Gradient Descent (SGD)", None))
        #self.comboBox.setItemText(1, _translate("Dialog", "K近邻", None))
        self.comboBox.setItemText(1, _translate("Dialog", "Nearest Neighbors (kNN)", None))
        #self.comboBox.setItemText(2, _translate("Dialog", "支持向量机", None))
        self.comboBox.setItemText(2, _translate("Dialog", "Support Vector Machines (SVM)", None))
        #self.comboBox.setItemText(3, _translate("Dialog", "朴素贝叶斯", None))
        self.comboBox.setItemText(3, _translate("Dialog", "Naive Bayes", None))
        #self.PB_ConfMatrix.setText(_translate("Dialog", "混淆矩阵", None))
        self.PB_ConfMatrix.setText(_translate("Dialog", "Confusion Matrix", None))
        #self.PB_CrossVad.setText(_translate("Dialog", "交叉验证", None))
        self.PB_CrossVad.setText(_translate("Dialog", "Cross-Validation", None))
        #self.LB_VadRst.setText(_translate("Dialog", "交叉验证结果：", None))
        self.LB_VadRst.setText(_translate("Dialog", "Result：", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
