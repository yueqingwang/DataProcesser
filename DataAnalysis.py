# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 09:31:15 2016

@author: wangyueqing
"""
import pandas as pd
import numpy as np

#根据lists进行数据过滤
#dataframe为数据表，columns为数据列名称，类型为list；
#filter_lists为要筛选的数据集合，类型为list，其中的元素
#为list，与每一列对应
def filter_by_list(dataframe, columns, filter_lists):
    print('1')
    for col,filter_list in zip(columns,filter_lists):
        #判断是否在筛选list内
        print(col)
        print(filter_list)
        dataframe = dataframe[dataframe[col].isin(filter_list)]
    print('2')
    return dataframe
        
#根据范围range进行数据过滤
#dataframe为数据表，columns为数据列名称，类型为list；
#filter_lists为要筛选的数据集合，类型为list，其中的元素
#为tuple，与每一列对应，包含大小值       
def filter_by_range(dataframe, columns, filter_ranges):
    for col,filter_range in zip(columns,filter_ranges):
        #判断是否在筛选range内,取得index
        index = (dataframe[col] >= filter_range[0]) & (dataframe[col] < filter_range[1])
        dataframe = dataframe[index]
    return dataframe

#根据列columns进行数据过滤
#dataframe为数据表，columns为数据列名称，类型为list；
def filter_by_columns(dataframe,columns):
    return dataframe[columns]
    

#将不需要输出的量屏蔽
def hide_index(dataframe,index_to_hide):
    index_to_show = dataframe.index.names.copy()
    #print(index_to_show)
    for i in index_to_hide:
        try:
            index_to_show.remove(i)
        except ValueError:
            pass
    #print(index_to_show)
    df = dataframe.reset_index().drop(index_to_hide,axis=1)
    return df.set_index(index_to_show)
    
    
def get_statistic(dataframe):
    df_statistic = dataframe.describe()
    df_statistic.ix['sigma+'] = df_statistic.ix['mean'] + df_statistic.ix['std']
    df_statistic.ix['sigma-'] = df_statistic.ix['mean'] - df_statistic.ix['std']
    return df_statistic
    
def get_statistic_groupby(dataframe,groups):
    grouped_df = dataframe.groupby(level=groups)
    functions = [('样本数','count'),('最大值','max'),('最小值','min'),
                 ('平均值','mean'),('标准偏差','std'),('sigma+',mean_plus_std),
                 ('sigma-',mean_minus_std)]
    grouped_agg = grouped_df.agg(functions)
    return grouped_agg

#在做统计处理前将数据的单位归一化，处理后，按照最多的数据的单位设置统计数据单位
def get_statistic_groupby_withunit(dataframe,groups):
    df = dataframe.drop(['TestResult'],axis = 1)
    df1 = df.apply(unit_convert,axis = 1)
    #对数据按照选择的分组进行划分
    grouped_data = df1.groupby(level = groups)
    functions = [('样本数','count'),('最大值','max'),('最小值','min'),
                 ('平均值','mean'),('标准偏差','std'),('sigma+',mean_plus_std),
                 ('sigma-',mean_minus_std)]
    grouped_data_agg = grouped_data.agg(functions)
    grouped_unit = df['unit'].groupby(level = groups)
    grouped_unit_agg = grouped_unit.agg(most_count)
    grouped_unit_agg = pd.DataFrame(grouped_unit_agg,columns= ['unit'])
    grouped_unit_agg.columns = [grouped_data_agg.columns.levels[0],['unit']]
    df2 = pd.concat([grouped_data_agg, grouped_unit_agg],axis = 1)
    df2 = df2.apply(unit_reconvert,axis = 1)
    #df2 = pd.concat([df2, grouped_unit_agg],axis = 1)
    return  df2
    
def mean_plus_std(arr):
    return np.mean(arr) + np.std(arr, ddof=1)
    
def mean_minus_std(arr):
    return np.mean(arr) - np.std(arr, ddof=1)

#计算字符串列表中个数最多的字符串
def most_count(arr):
    ddict = {}
    mostkey = None
    mostvalue = 0
    for i in arr:
        if i in ddict:
            ddict[i] += 1
        else:
            ddict[i] = 1
        if ddict[i] > mostvalue :
            mostvalue = ddict[i]
            mostkey = i
    return mostkey
    

#将数据的单位归一化
#如ms、us、ns统一设置成s
def unit_convert(dlist):
    if 'm' in dlist[-1] :
        return dlist[:-1]*1e-3
    if 'u' in dlist[-1] :
        return dlist[:-1]*1e-6
    if 'n' in dlist[-1] :
        return dlist[:-1]*1e-9
    return dlist[:-1]

#设置统计数据单位，按照单位换算数据大小
#列表中第一个数据数据个数，不进行单位换算
def unit_reconvert(dlist):
    base = 1
    if 'm' in dlist[-1] :
        base = 1e3
    if 'u' in dlist[-1] :
        base = 1e6
    if 'n' in dlist[-1] :
        base = 1e9
    return [dlist[0]]+[i*base for i in dlist[1:-1]] + [dlist[-1]]
    
    

if __name__ == '__main__':
    df = pd.DataFrame({
    'item':['a','b','a','b'],
    'item1':['a','a','a','a'],
    'data1':[2.6,2.0,2.4,2.2],
    'unit':['us','ms','ms','ms'],
    'TestResult':[1,1,1,1]
    })
    
    print(filter_by_list(df,['item','item1'],[['a'],['a']]))
    print(filter_by_range(df,['data1'],[(1,3)]))
    df1 = filter_by_columns(df,['item1','data1'])
    df2 = df1.set_index(['item1'])
    print(df2)
    print(get_statistic_groupby(df2,'item1'))

    



