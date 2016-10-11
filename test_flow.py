# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 13:36:34 2016
@author: wangyueqing

状态机说明：
self.fsm = {
's0':判断是否为test flow的起始，是则开始读头文件s1，否则跳行重复执行s0
's1':判断是否flow的头文件是否已经读取完，是则进行头文件处理，并进入s2，否则继续读s1
's2':判断是否为test的起始，若是，则开始test数据的处理s3，否则进入s8
's3':判断是否为pmu test的起始，若是，则开始pmu数据的处理s4，否则进入s5
's4':判断是否为pmu数据格式，若是进行处理，且再次对下一行进行同样判断s4
否则开始返回s3
's5':判断是否为vlog test的起始，若是，则开始vlog数据的处理s6，否则进入s7
's6':判断是否为vlog数据格式，若是进行处理，且再次对下一行进行同样判断s6
否则开始返回s5
's7':判断是否为自定义的数据格式，若是进行处理，且再次对下一行进行同样判断s7
否则开始返回s2，判断是否为新的test的起始，若是，按照新test的流程处理
's8':判断是否为flow的结束，若是进行处理，跳转到s0,执行下一个flow的处理。否则跳转到s9
's9':与s0的判断方法相同，判断是否为test flow的起始，这是由于在测试中发现会有执行完头文件
就开始下一个flow的现象出现。若是，则跳转到s0，且此处不读入下一行数据。若不是，则可能是自
定义的数据之后有其他的格式。首先进入s10
's10':判断是否是 pmu 或是 vlog 测试，是则进入s3开始处理，否则，读取下一行进入s7处理
}

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

r = 'Test.Mods.Site.PHY'
m9 = re.compile(r)

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
        's8':[m8,'s0','s9',True,False,self.update_head_info,self.dummy_loop],
        's9':[m0,'s0','s10',False,True,self.update_head_info,self.dummy_loop],
        's10':[m9,'s3','s7',False,True,self.update_head_info,self.dummy_loop]
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
        pmu_record = [self.flow_id,self.test_id] + list(m4.match(line).groups())
        self.pmu_records.append(pmu_record)
        
    def update_vlog_record(self,line):
        vlog_record = [self.flow_id,self.test_id] + list(m6.match(line).groups())
        self.vlog_records.append(vlog_record)
    
    def update_dlg_record(self,line):
        self.dlg_records.append([self.flow_id,self.test_id,line])
    
    def dummy_loop(self,line):
        pass
            
        

if __name__ == '__main__':
    
    Tree = TestResultTree('D:\\python\\DataProcesser\\1543W','.+\.dlg')
#    print(Tree.treelist)
#    for i in Tree.pmu_records:
#        print(i)
    #print(Tree.pmu_records)