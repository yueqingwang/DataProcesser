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
import infoWidgetUi
import DataAnalysis as das

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
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.tabClose)
        self.DataSpace = None
        self.SelectFiles = []
        
    #菜单栏初始化
    def setupMenuBar(self):
        #file Menu setup
        fileMenu = self.menuBar.addMenu('&File')
        openAction = fileMenu.addAction(QtGui.QIcon('./images/file/fileopen.png'),'&Open')
        openAction.setShortcut('Ctrl+O')
        saveAction = fileMenu.addAction(QtGui.QIcon('./images/file/filesave.png'),'&save')
        saveAction.setShortcut('Ctrl+S')
        saveasAction = fileMenu.addAction(QtGui.QIcon('./images/file/filesaveas.png'),'&saveas')
        closeAction = fileMenu.addAction(QtGui.QIcon('./images/file/fileclose.png'),'&close')
        exitAction = fileMenu.addAction(QtGui.QIcon('./images/actions/exit.png'),'&exit')
        exitAction.setShortcut('Ctrl+S')
        fileMenu.triggered[QtGui.QAction].connect(self.fileMenuActionSlot)

        #edit Menu setup
        editMenu = self.menuBar.addMenu('&Edit')
        undoAction = editMenu.addAction(QtGui.QIcon('./images/actions/undo.png'),'&undo')
        undoAction.setShortcut('Ctrl+Z')
        showinfoAction = editMenu.addAction(QtGui.QIcon('./images/actions/show.png'),'&show')
        undoAction.triggered.connect(self.showSelection)
        showinfoAction.triggered.connect(self.showInfo)
        
        #analysis Menu setup
        analysisMenu = self.menuBar.addMenu('&Analysis')
        getPmuAction = analysisMenu.addAction('&Get Selected PMU')
        getVlogAction = analysisMenu.addAction('&Get Selected Vlog')
        getDlgAction = analysisMenu.addAction('&Get Selected Dlg')
        analysisMenu.triggered[QtGui.QAction].connect(self.analysisMenuActionSlot)

        
        #Statistics Menu setup
        statMenu = self.menuBar.addMenu('&Statistics')
        getPmuStatAction = statMenu.addAction('&Statistics on PMU')
        getVlogStatAction = statMenu.addAction('&Statistics on Vlog')
        getDlgStatAction = statMenu.addAction('&Statistics on Dlg')
        statMenu.triggered[QtGui.QAction].connect(self.statMenuActionSlot)
        
        #Plot Menu setup
        plotMenu = self.menuBar.addMenu('&Plot')
        getLineAction = plotMenu.addAction('&Line')
        getHistAction = plotMenu.addAction('&Histgram')
        
        #setting Menu setup
        settingMenu = self.menuBar.addMenu('&Setting')
        
        
    #工具栏初始化
    def setupToolBar(self):               
        new = self.toolBar.addAction(QtGui.QIcon('./images/console/run_small.png'),'&File')
        goto = self.toolBar.addAction(QtGui.QIcon('./images/editor/gotoline.png'),'&Goto')
        goto.triggered.connect(self.showRawData)
        #new.triggered.connect(self.showDataTable)
        
    #file menu slot
    def fileMenuActionSlot(self,q):
        print("file Menu Action triggered")
        
        #打开操作，打开处理的数据目录，加载数据到表中
        if q.text() == '&Open' :
            self.DataSpace = QtGui.QFileDialog.getExistingDirectory(self, 'Open fold','./')
            tree = test_flow.TestResultTree(self.DataSpace,'.+\.dlg')
            #获取数据表
            #测试信息表
            self.testFlowInfo = pd.DataFrame(tree.flow_info,columns = test_flow.flow_info_col)
            self.testFlowInfo = self.testFlowInfo.set_index(['flowID'])
            #pmu数据表
            self.PmuRecords = pd.DataFrame(tree.pmu_records,columns = test_flow.pmu_record_col )
            #vlog数据表
            self.VlogRecords = pd.DataFrame(tree.vlog_records,columns = test_flow.vlog_record_col )
            #dlg数据表
            self.DlgRecords = pd.DataFrame(tree.dlg_records,columns = test_flow.dlg_record_col )
            
            #设置数据文件结构树
            file_tree_data = tree.treelist
            self.fileTreeModel = TreeModel.TreeModel(file_tree_data)
            self.treeFile.setModel(self.fileTreeModel)
            self.treeFile.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            self.treeFile.doubleClicked.connect(self.getSelectIndexData)
            #self.treeFile.
            
            #设置程序FLOW结构树
            flow_tree_data = tree.flowtreeList
            self.flowTreeModel = TreeModel.TreeModel(flow_tree_data)
            self.treeFlow.setModel(self.flowTreeModel)
            self.treeFlow.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            
            return True


    #Analysis menu slot
    def analysisMenuActionSlot(self,q):
        print("analysis Menu Action triggered")
        #显示选中的pmu结果
        if q.text() == '&Get Selected PMU' :
            self.showPMU()

    #Statistics menu slot
    def statMenuActionSlot(self,q):
        print("Statistics Menu Action triggered")
        #显示选中的pmu结果
        if q.text() == '&Statistics on PMU' :
            self.showPmuStat()
            
    def showSelection(self):
        for index in self.treeFile.selectedIndexes() :
            if index.isValid():
                print( TreeModel.getDirs(self.fileTreeModel.getTreePath(index)))
                
    def getSelectIndexData(self,index):
        if self.fileTreeModel.isLeaf(index) == True:
            selectflow = self.fileTreeModel.data(index,QtCore.Qt.DisplayRole)
            infoList = [selectflow] + list(self.testFlowInfo.ix[int(selectflow)])
            self.Info = InfoWidget()
            self.Info.setLineEdits(infoList)
            self.Info.show()            

    def showRawData(self):
        if len(self.treeFile.selectedIndexes()) == 1:
            for index in self.treeFile.selectedIndexes():
                if self.fileTreeModel.isLeaf(index) == True:
                    selectflow = self.fileTreeModel.data(index,QtCore.Qt.DisplayRole)
                    path = list(self.testFlowInfo.ix[int(selectflow)])[:3]
                    sl,el = int(path[1]),int(path[2])
                    TextEdit = QtGui.QTextEdit()
                    with open(path[0],'r') as f:
                        linecount = 0
                        for line in f:
                            linecount += 1
                            if linecount > el:
                                break
                            if linecount > sl:
                                TextEdit.append(line.strip())
                        f.close()
                    self.tabNew(TextEdit)
        return 0
        
    def showInfo(self):
        self.Info = InfoWidget()
        testList ='abcdefghijklmnopqrstuvw'
        print(testList)
        self.Info.setLineEdits(testList)
        self.Info.show()
        
    def showPMU(self):
        print('showPMU trigglerd')
        SelectedDevice = self.getSelectedDevice()
        SelectedTest = self.getSelectedTest('pmu')
        records = self.PmuRecords
        records = das.filter_groupby_list(records,[['flowID'],['TestName','Pin']],[SelectedDevice,SelectedTest])
        records= records.reset_index(drop=True)
        self.showDataTable(records)
        
    def showPmuStat(self):
        print('showPMU trigglerd')
        SelectedDevice = self.getSelectedDevice()
        SelectedTest = self.getSelectedTest('pmu')
        records = self.PmuRecords
        records = das.filter_groupby_list(records,[['flowID'],['TestName','Pin']],[SelectedDevice,SelectedTest])
        records= records.reset_index(drop=True)
        records = das.get_statistic_groupby_withunit(records,['TestName','Pin'],'Measure','MeasureU')
        records = records.reset_index()
        self.showDataTable(records)        
    
    def showDataTable(self,DataTable):
        table = QtGui.QTableWidget()
        row = len(DataTable.index)
        rows = DataTable.index
        col = len(DataTable.columns)
        cols = DataTable.columns
        table.setRowCount(row)
        table.setColumnCount(col)
        table.setHorizontalHeaderLabels(list(DataTable.columns))
        for i in range(row):
            for j in range(col):
                data = str(DataTable.get_value(rows[i],cols[j]))
                newItem =  QtGui.QTableWidgetItem(data)
                table.setItem(i, j , newItem)
        self.tabNew(table)
        
    #tabwitdge中新建tab            
    def tabNew(self,tab):
        #tab_count来控制tab的编号，每次新建在之前的基础上加1，无tab时设置为1
        if self.tabWidget.count() :
            self.tab_count += 1
        else:
            self.tab_count = 1
        self.tabWidget.addTab(tab,'tab{:d}'.format(self.tab_count))
        

    #关闭tab
    def tabClose(self,index):
        print(index)
        self.tabWidget.removeTab(index)
        
        
    def getSelectedDevice(self):
        SelectedDevice = []
        for index in self.treeFile.selectedIndexes() :
            if index.isValid():
                leafIndex = self.fileTreeModel.getLeafs(index)
                deviceIndex = filter(lambda x :self.fileTreeModel.isParentMatch(x,'.+\.dlg'), leafIndex)
                for device in deviceIndex:
                    deviceData = int(self.fileTreeModel.data(device,QtCore.Qt.DisplayRole))
                    SelectedDevice.append((deviceData,))
        return SelectedDevice
        
    def getSelectedTest(self,DataType):
        SelectedTest = []
        for index in self.treeFlow.selectedIndexes():
            if index.isValid():
                leafIndex = self.flowTreeModel.getLeafs(index)
                valIndex = filter(lambda x :self.flowTreeModel.isParentMatch(x,DataType), leafIndex)
                for val in valIndex:
                    test = self.flowTreeModel.parent(self.flowTreeModel.parent(val))
                    valData = self.flowTreeModel.data(val,QtCore.Qt.DisplayRole)
                    testData = self.flowTreeModel.data(test,QtCore.Qt.DisplayRole)
                    SelectedTest.append((testData,valData))
        return SelectedTest
        

class InfoWidget(QtGui.QWidget,infoWidgetUi.Ui_FormInfo):
    def __init__(self, parent = None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.LineEditList = [self.lineEdit_1,self.lineEdit_2,
                             self.lineEdit_3,self.lineEdit_4,self.lineEdit_5,
                             self.lineEdit_6,self.lineEdit_7,self.lineEdit_8,
                             self.lineEdit_9,self.lineEdit_10,self.lineEdit_11,
                             self.lineEdit_12,self.lineEdit_13,self.lineEdit_14,
                             self.lineEdit_15,self.lineEdit_16,self.lineEdit_17,
                             self.lineEdit_18,self.lineEdit_19,self.lineEdit_20,
                             self.lineEdit_21,self.lineEdit_22]

    def setLineEdits(self,testList):
        lenth = min([len(self.LineEditList),len(testList)])
        for i in range(lenth):
            self.LineEditList[i].setText(str(testList[i]))
            
            
    def getLineEditText(self):
        return [lineEdit.displayText() for lineEdit in self.LineEditList]
    
            
        

def main():
    app = QtGui.QApplication(sys.argv)
    ex = DataProcessApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
