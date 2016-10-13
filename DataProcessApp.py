# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 13:20:16 2016

@author: wangyueqing
"""

import sys
import os
import re
from PyQt4 import QtGui, QtCore
import pandas as pd


import DataProcessUi
import TreeModel
import test_flow

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
            tree = test_flow.TestResultTree(self.DataSpace,'.+\.dlg')
            tree_data = tree.treelist
            self.testFlowInfo = pd.DataFrame(tree.flow_info,columns = test_flow.flow_info_col)
#            self.testFlowInfo.reindex()
            print(self.testFlowInfo.index.values)
            self.testFlowInfo = self.testFlowInfo.set_index(['flowID'])
            print(self.testFlowInfo)
            #print(self.testFlowInfo.ix['3'])
#            tree_data = TreeModel.dirsTree(self.DataSpace,'.+\.dlg')
            self.fileTreeModel = TreeModel.TreeModel(tree_data)
            self.treeFile.setModel(self.fileTreeModel)
            self.treeFile.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            self.treeFile.doubleClicked.connect(self.getSelectIndexData)

    def showSelection(self):
        for index in self.treeFile.selectedIndexes() :
            if index.isValid():
                print( TreeModel.getDirs(self.fileTreeModel.getTreePath(index)))
                
    def getSelectIndexData(self,index):
        if self.fileTreeModel.isLeaf(index) == True:
            selectflow = self.fileTreeModel.data(index,QtCore.Qt.DisplayRole)
            print(selectflow)
            print(self.testFlowInfo.ix[[int(selectflow)]])
        
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = DataProcessApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
