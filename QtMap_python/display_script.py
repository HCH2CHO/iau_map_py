# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 09:26:57 2019

@author: HCHO
"""

#添加文件字段，在arcgis中显示
#用于在arcgis中显示线段
import os
#完全合并，添加id字段
def merge1(outputFile,floder):
    lane=open(outputFile,'w')
    laneList=os.listdir(floder)
    for item in laneList:
        file=open(floder+"\\"+item)
        string=item.replace('.txt','')
        line=file.readline()
        while(line):
            line=line.strip('\n')+" "+string+"\n"
            lane.write(line)
            line=file.readline()
    lane.close()
'''
merge("display_lane.txt","Lane")
merge("display_conn.txt","Conn")
'''

#数据合并，并添加线段id及conn的连接字段、lane的road字段
def merge2(outputFile,floder,index_folder):
    roadindex=open(index_folder+"roadindex.txt",'r')
    conn2laneindex=open(index_folder+"conn2laneindex.txt",'r')
    
    roadindex_list=roadindex.readlines()
    roadindex_dic={}
    for item in roadindex_list:
        line=item.strip().split('\t')
        roadindex_dic[line[1]]=line[0]
    
    conn2laneindex_list=conn2laneindex.readlines()
    conn2laneindex_dic={}
    for item in conn2laneindex_list:
        line=item.strip().split('\t')
        conn2laneindex_dic[line[0]]=(line[1],line[2])
    
    roadindex.close()
    conn2laneindex.close()
    
    lane=open(outputFile,'w')
    if "Lane" in floder:
        for item in roadindex_dic:
            file=open(floder+"\\"+item+'.txt')
            line=file.readline()
            while(line):
                line=line.strip('\n')+" "+item+' '+roadindex_dic[item]+"\n"
                lane.write(line)
                line=file.readline()
    elif "Conn" in floder:
        for item in conn2laneindex_dic:
            file=open(floder+"\\"+item+'.txt')
            line=file.readline()
            while(line):
                line=line.strip('\n')+" "+item+' '+conn2laneindex_dic[item][0]+' '+conn2laneindex_dic[item][1]+"\n"
                lane.write(line)
                line=file.readline() 
    lane.close()

merge2("display_lane.txt","outputDATA\\Lane","outputDATA\\")
merge2("display_conn.txt","outputDATA\\Conn","outputDATA\\") 