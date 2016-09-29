# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 13:20:16 2016

@author: wangyueqing
"""

import sys
import os
import re
from PyQt4 import QtGui, QtCore

import DataProcessUi
import TreeModel

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
        
        self.DataSpace = None
        self.SelectFiles = []
        
        
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
        undoAction.triggered.connect(self.showSelection)
        
        
    def setupToolBar(self):               
        self.toolBar.addAction(QtGui.QIcon('./images/console/run_small.png'),'&File')
        
    def fileMenuActionSlot(self,q):
        print("triggered")
        
        if q.text() == '&Open' :
            name = QtGui.QFileDialog.getOpenFileName(self, 'Open file','./',"Datlog files (*.dlg)")
            print(name)
            
        if q.text() == '&Open Fold' :
            self.DataSpace = QtGui.QFileDialog.getExistingDirectory(self, 'Open fold','./')
            print(self.DataSpace)
            tree_data = TreeModel.dirsTree(self.DataSpace,'.+\.dlg')
            self.fileTreeModel = TreeModel.TreeModel(tree_data)
            self.treeFile.setModel(self.fileTreeModel)
            self.treeFile.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

    def showSelection(self):
        for index in self.treeFile.selectedIndexes() :
            if index.isValid():
                print( TreeModel.getDirs(self.fileTreeModel.getTreePath(index)))
                
    def getSelectFiles(self):
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = DataProcessApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
