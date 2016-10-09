# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 13:36:34 2016

@author: wangyueqing
"""

import pandas as pd
import os
import re


r = 'Tester ID:'
m0 = re.compile(r)

r = 'Users_C:'
m1 = re.compile(r)

r = 'Test '
m2 = re.compile(r)

r = 'Test.Mods.Site.PHY  Pin/Grp'
m3 = re.compile(r)

r = '\s*(\w+\.\w+\.\w+\..{3})\s+'
r+= '(\w+)\s+(\w+)\s+'
r+= '(-?\d+\.?\d*)([\s|m|u|n][V|A])/(-?\d+\.?\d*)([\s|m|u|n][V|A])\s+'*3
r+= '(\w+)'
m4 = re.compile(r)

r = 'Test.Mods.Site.PHY    Type'
m5 = re.compile(r)

r = '\s*(\w+\.\w+\.\w+\..{3})\s+'
r+= '(\w+)\s+(\w+)\s+(\w+)\s+'
r+= '(\d+\.?\d*)([\s|m|u|n]s)\s+'
r+= '(\d+\.?\d*)([\s|m|u|n]s)/(\d+\.?\d*)([\s|m|u|n]s)\s+'
r+= '(\w+)'
m6 = re.compile(r)

r = '\s*\w+\.\w+\.\*{3}\.\*{3}'
m7 = re.compile(r)

r = 'Kalos2 '
m8 = re.compile(r)

def fsm_fun(argfunc,arg):
    argfunc(arg)

def match_fsm(fsm,state,line):
    if fsm[state][0].match(line):
        fsm_fun(fsm[state][5],line)
        return fsm[state][1],fsm[state][3]
    else:
        fsm_fun(fsm[state][6],line)
        return fsm[state][2],fsm[state][4]

class TestResultTree(object):
    def __init__(self,startPath,pattern):
        self.root_path = startPath
        self.head_info = []
        self.head_records = []
        self.pmu_records = []
        self.vlog_records = []
        self.dlg_records = []
        self.sub_flow = []
        self.flow_id = 0 
        self.test_id = None
        self.fsm = {
        's0':[m0,'s1','s0',True,True,self.update_flow,self.dummy_loop],
        's1':[m1,'s2','s1',True,True,self.collect_head_info,self.collect_head_info],
        's2':[m2,'s3','s8',True,False,self.update_test,self.dummy_loop],
        's3':[m3,'s4','s5',True,False,self.dummy_loop,self.dummy_loop],
        's4':[m4,'s4','s3',True,False,self.update_pmu_record,self.dummy_loop],
        's5':[m5,'s6','s7',True,False,self.dummy_loop,self.dummy_loop],
        's6':[m6,'s6','s5',True,False,self.update_vlog_record,self.dummy_loop],
        's7':[m7,'s7','s2',True,False,self.update_dlg_record,self.dummy_loop],
        's8':[m8,'s0','s7',True,True,self.update_head_info,self.dummy_loop]
        }
        
        self.setupTree(pattern)
        
        
        
    def setupTree(self,pattern):
        self.treelist = []
        for root, dirs, files in os.walk(self.root_path):
            #print(root)
            #获取当前目录相对输入目录的层级关系,整数类型
            level = root.replace(self.root_path, '').count(os.sep)
            #根据目录的层级关系，重复显示'\t'间隔符，
            indent = '\t' * level 
            self.treelist.append('%s%s' % (indent, os.path.split(root)[1]))
            #将该目录下的文件添加到下一级
            for file in files:
                file_indent = indent + '\t' 
                file_path = root + '\\' + file
                #print(file_path)
                #按照条件筛选文件
                if re.match(pattern,file):
                    self.treelist.append('%s%s' % (file_indent, file))
                    self.processFile(file_path)
                    for subflow in self.sub_flow:
                        self.treelist.append('%s\t%s' % (file_indent, subflow))
                    
    def processFile(self,file_path):
        nextstate = 's0'
        match_count = 0
        line_count = 0
        self.sub_flow = []
        with open(file_path,'r') as f:
            for line in f:
                line_count += 1
                if line != '\n':
                    nextstate,result = match_fsm(self.fsm,nextstate,line)
                    match_count += 1
                    if match_count > 10000 :
                        break
                    while not result:
                        nextstate,result = match_fsm(self.fsm,nextstate,line)
                        match_count += 1
                        if match_count > 10000 :
                            break
            f.close()
        return self.sub_flow
    
    def update_test(self,line):
        self.test_id = line.split()[-1]
        pass
    
    def update_flow(self,line):
        self.flow_id += 1
        self.head_records = []
    
    def collect_head_info(self,line):
        self.head_records.append(line)
    
    def update_head_info(self,line):
        self.sub_flow.append(self.flow_id)
        self.head_info.append(self.flow_id)
    
    def update_pmu_record(self,line):
        self.pmu_records.append([self.flow_id,self.test_id,line])
        
    def update_vlog_record(self,line):
        self.vlog_records.append([self.flow_id,self.test_id,line])
    
    def update_dlg_record(self,line):
        self.dlg_records.append([self.flow_id,self.test_id,line])
    
    def dummy_loop(self,line):
        pass
            
        

if __name__ == '__main__':
    
    Tree = TestResultTree('D:\\python\\DataProcesser\\1543W','.+\.dlg')
    print(Tree.treelist)
#    for i in Tree.pmu_records:
#        print(i)
    #print(Tree.pmu_records)