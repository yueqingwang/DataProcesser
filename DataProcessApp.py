# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 13:20:16 2016

@author: wangyueqing
"""

import sys
from PyQt4 import QtGui, QtCore

import DataProcessUi

class DataProcessApp(QtGui.QMainWindow, DataProcessUi.Ui_MainWindow):
    def __init__(self, parent = None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setupMenuBar()
        self.setupToolBar()
        
        self.splitter = QtGui.QSplitter()
        self.splitter.addWidget(self.widget_left)
        self.splitter.addWidget(self.widget_mid)
        self.splitter.addWidget(self.widget_right)
        self.setCentralWidget(self.splitter)
        
        
    def setupMenuBar(self):
        fileMenu = self.menuBar.addMenu('&File')
        openAction = fileMenu.addAction(QtGui.QIcon('./images/file/fileopen.png'),'&Open')
        openAction.setShortcut('Ctrl+O')
        openfoldAction = fileMenu.addAction('&Open Fold')
        saveAction = fileMenu.addAction(QtGui.QIcon('./images/file/filesave.png'),'&save')
        saveAction.setShortcut('Ctrl+S')
        saveasAction = fileMenu.addAction(QtGui.QIcon('./images/file/filesaveas.png'),'&saveas')
        closeAction = fileMenu.addAction(QtGui.QIcon('./images/file/fileclose.png'),'&close')
        exitAction = fileMenu.addAction(QtGui.QIcon('./images/actions/exit.png'),'&exit')
        exitAction.setShortcut('Ctrl+S')
#        openAction.triggered.connect(self.openActionSlot)
        editMenu = self.menuBar.addMenu('&Edit')
        undoAction = editMenu.addAction(QtGui.QIcon('./images/actions/undo.png'),'&undo')
        undoAction.setShortcut('Ctrl+Z')
        fileMenu.triggered[QtGui.QAction].connect(self.fileMenuActionSlot)
        
        
        
    def setupToolBar(self):               
        self.toolBar.addAction(QtGui.QIcon('./images/console/run_small.png'),'&File')
        
    def fileMenuActionSlot(self,q):
        print("triggered")
        
        if q.text() == '&Open' :
            name = QtGui.QFileDialog.getOpenFileName(self, 'Open file','./',"Datlog files (*.dlg)")
            print(name)
            
        if q.text() == '&Open Fold' :
            name = QtGui.QFileDialog.getExistingDirectory(self, 'Open fold','./')
            print(name)
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = DataProcessApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
