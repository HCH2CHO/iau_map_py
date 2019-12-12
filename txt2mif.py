# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:44:46 2019

@author: HCHO
"""

import numpy as np
import os


#读取原始数据
def ReadAllData(dic,data_list):
    for item in Conn_list:
        lane_id=int(item.replace('.txt',''))
        lane_data=np.loadtxt(Lane_data_path+"\\"+item) 
        #lane_data=np.delete(lane_data,[7,8,10,11,12],axis = 1)
        dic[lane_id]=lane_data.copy()
    return dic

if __name__=="__main__":
    xc_data_path="data\\xc"
    Conn_data_path=xc_data_path+"\\Conn"
    Lane_data_path=xc_data_path+"\\Lane"
    
    Conn_list=os.listdir(Conn_data_path)
    Lane_list=os.listdir(Lane_data_path)
    Conn={}
    Lane={}
    
    Conn=ReadAllData(Conn,Conn_list)
    Lane=ReadAllData(Lane,Lane_list)
    
    
    
    #数据融合    
    
    