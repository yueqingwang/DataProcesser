# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DataProcessUi.ui'
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
        MainWindow.resize(800, 600)
        MainWindow.setAccessibleName(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget_left = QtGui.QWidget(self.centralwidget)
        self.widget_left.setObjectName(_fromUtf8("widget_left"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget_left)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableFlow = QtGui.QTableWidget(self.widget_left)
        self.tableFlow.setObjectName(_fromUtf8("tableFlow"))
        self.tableFlow.setColumnCount(0)
        self.tableFlow.setRowCount(0)
        self.verticalLayout.addWidget(self.tableFlow)
        self.horizontalLayout.addWidget(self.widget_left)
        self.widget_mid = QtGui.QWidget(self.centralwidget)
        self.widget_mid.setObjectName(_fromUtf8("widget_mid"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_mid)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(self.widget_mid)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.horizontalLayout.addWidget(self.widget_mid)
        self.widget_right = QtGui.QWidget(self.centralwidget)
        self.widget_right.setObjectName(_fromUtf8("widget_right"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget_right)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tableWidget_2 = QtGui.QTableWidget(self.widget_right)
        self.tableWidget_2.setObjectName(_fromUtf8("tableWidget_2"))
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tableWidget_2)
        self.horizontalLayout.addWidget(self.widget_right)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))

