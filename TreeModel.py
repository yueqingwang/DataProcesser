# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:02:38 2016

@author: wangyueqing
"""
############################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
############################################################################
import os
import re
from PyQt4 import QtCore, QtGui


class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = TreeItem(("name",))
        self.setupModelData(data, self.rootItem)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)
        
    def children(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
            
        Item = index.internalPointer()
        childItems = Item.childItems()
        for  c in childItems:
            print(c.row())
            print(c.data(0))
        return [self.createIndex(c.row(), 0, c) for c in childItems]

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
            
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setupModelData(self, lines, parent):
        parents = [parent]
        indentations = [0]
        for line in lines:
            lineData = list(line)
            position = 0
            while lineData.pop(0) == '\t':
                position += 1
            line = line.lstrip('\t')
            if line:
                # Read the column data from the rest of the line.
                columnData = [line]
                if position > indentations[-1]:
                    # The last child of the current parent is now the new
                    # parent unless the current parent has no children.
                    if parents[-1].childCount() > 0:
                        parents.append(parents[-1].child(parents[-1].childCount() - 1))
                        indentations.append(position)
                else:
                    while position < indentations[-1] and len(parents) > 0:
                        parents.pop()
                        indentations.pop()
                # Append a new item to the current parent's list of children.
                parents[-1].appendChild(TreeItem(columnData, parents[-1]))
                
    def isLeaf(self,index):
        if not index.isValid():
            return QtCore.QModelIndex()
        if index.internalPointer().childItems :
            return False
        else:
            return True
                
    def getTreePath(self,index):
        if not index.isValid() :
            return []
        path_list = [index.internalPointer().data(0)]
        parent = self.parent(index)
        while parent.isValid() :
            path_list.append(parent.internalPointer().data(0))
            parent = self.parent(parent)
        return path_list
        
    def isParentMatch(self,index,pattern):
        if not index.isValid():
            return QtCore.QModelIndex()
        parent = self.parent(index)
        if not parent.isValid():
            return QtCore.QModelIndex()
        if re.match(pattern,parent.internalPointer().data(0)):
            return True
        else:
            return False
            
#    def getLeafs(self,index):
#        leafs = []
#        def _getLeaf(index)
#            if not index.isValid() :
#                pass
#            else:
#                if
#                children = self.children
        
            
        
            
            
def dirsTree(startPath,pattern):
    '''树形打印出目录结构'''
    dirsTreeList = []
    for root, dirs, files in os.walk(startPath):
        print(root)
        #获取当前目录相对输入目录的层级关系,整数类型
        level = root.replace(startPath, '').count(os.sep)
        #根据目录的层级关系，重复显示'\t'间隔符，
        indent = '\t' * level 
        dirsTreeList.append('%s%s' % (indent, os.path.split(root)[1]))
        #将该目录下的文件添加到下一级
        for file in files:
            #按照条件筛选文件
            if re.match(pattern,file):
                dirsTreeList.append('%s\t%s' % (indent, file))
    return dirsTreeList
    
    
def getDirs(dirs_list):
    return '\\'.join(dirs_list[-2::-1])



if __name__ == '__main__':
    #print('imported')

    import sys

    app = QtGui.QApplication(sys.argv)
    data = dirsTree('D:\\python\\DataProcesser\\FengZhuangHou','.+\.dlg')
    print(data)
    model = TreeModel(data)
#    print(model.rowCount(model.rootItem ))
#    print(model.rootItem.itemData)
#    for item in model.rootItem.childItems:
#        print(item.itemData)
    index = model.createIndex(0, 0, model.rootItem)
    print(model.columnCount(index),model.itemData(index))
    index = model.index(0,0,index)
    print(model.rowCount(index),model.itemData(index))
    index = model.index(0,0,index)
    print(model.rowCount(index),model.itemData(index))
    index = model.index(0,0,index)
    print(model.rowCount(index),model.itemData(index))
    index = model.index(1,0,index)
    print(model.rowCount(index),model.itemData(index))
    index = model.index(1,0,index)
    print(model.rowCount(index),model.data(index,0))
    path = model.getTreePath(index)
    print(path)
    print(getDirs(path))
