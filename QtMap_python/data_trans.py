# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 17:30:23 2019

@author: HCHO
"""
#自动转换脚本
#由roadindex和conn2laneindex生成connindex文件
def data_trans(filepath):
    road=open(filepath+"roadindex.txt",'r')
    conn=open(filepath+"connindex.txt",'w')
    conn2lane=open(filepath+"conn2laneindex.txt",'r')
    
    road_dic={}
    line1=road.readline()
    while(line1):
        line1=line1.strip().split('\t')
        if line1[1] not in road_dic:
            road_dic[line1[1]]=line1[0]
        else:
            road_dic[line1[1]]=line1[0]
        line1=road.readline()
    
    line2=conn2lane.readline()
    while(line2):
        try:
            line2=line2.strip().split('\t')
            conn.write(line2[0]+'\t'+road_dic[line2[1]]+'\t'+road_dic[line2[2]]+'\n')
            line2=conn2lane.readline()
        except:
            line2=conn2lane.readline()
        
    road.close()
    conn.close()
    conn2lane.close()