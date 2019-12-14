# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 14:18:29 2019

@author: HCHO
"""

#数据预处理脚本
import os
from Wgs84ToGauss import Wgs84ToGauss
from DouglasPeucker import *
#文件数据整合
#fileList为数据文件名列表,name为输出文件名
def fileMerge(filepath,fileList,name):
    allFile=open(name,'w')
    for file in fileList:
        oneFile=open(filepath+file,'r')
        line=oneFile.readline()
        while(line):
            allFile.write(line)
            line=oneFile.readline()
        oneFile.close()
    allFile.close()
    
#mission点坐标转换
def coordTranse(fileName):
    file=open(fileName,'r')
    output=open(fileName.replace('.txt','')+'_coordTranse.txt','w')
    line=file.readline()
    while(line):
        line=line.split('\t')
        x,y=Wgs84ToGauss(float(line[1]),float(line[0]),6)
        output.write(str(x)+'\t'+str(y)+'\n')
        line=file.readline()    
    file.close()
    output.close()
    
#NovAtel加ID
#choose为0时，加一列id. choose为1时，替换第一列id。结果为重排序id
def reorderID(fileName,outputpath,choose):
    file=open(fileName,'r')
    output=open(outputpath.replace('.txt','')+'_order.txt','w')
    line=file.readline()
    id=0
    while(line):        
        if(choose==0):
            output.write(str(id)+'\t'+line)
        elif(choose==1):
            line=line.split(' ',1)[1]
            output.write(str(id)+'\t'+line)
        id=id+1
        line=file.readline()
    file.close()
    output.close()


#线数据预处理
def lanePreProcessing():
    list_Lane = os.listdir("DATA\\Lane")
    for item in list_Lane:
        reorderID("DATA\\Lane\\"+item,"DATA\\output\\"+item,0)
        outputResult("DATA\\output\\"+item.replace('.txt','')+'_order.txt')
        #print(item)
      
    after_list=os.listdir("DATA\\output")
    for item in after_list:
        if("after" not in item):
            after_list.remove(item)
    fileMerge("DATA\\output\\",after_list,'DATA\\Lane.txt')
    reorderID('DATA\\Lane.txt','Lane.txt',1)

#点数据预处理    
def pointPreProcessing():
    list_MissionPoint = os.listdir("DATA\\MissionPoint")
    fileMerge("DATA\\MissionPoint\\",list_MissionPoint,'DATA\\MissionPoint.txt')
    coordTranse("DATA\\MissionPoint.txt")
    
    