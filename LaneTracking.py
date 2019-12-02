# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 12:35:19 2019

@author: HCHO
"""
from DouglasPeucker import *
import sys
import os
import math
import pandas as pd
import numpy as np


#命令行输入车道路径,如python  LaneTracking.py  lane/1.txt
#后面按代码规范修改下
if __name__=="__main__":    
    #lane_path = sys.argv[1]
    #print(lane_path)
    
    #测试用
    lane_path="data\\lane\\NovAtel2019-11-22-11-35-10.txt"
    
    
    father_path=os.path.dirname(lane_path)
    list_Lane = os.listdir(father_path)
    is_DouglasPecker_processing=True
    for item in list_Lane:
        if("after" in item):
            is_DouglasPecker_processing=False
                
    if(is_DouglasPecker_processing):
        outputResult(lane_path,1)
        
    after_lane_path=lane_path.replace('.txt','.after.txt')
    #after_lane列表 id，timestamp,lon,lat,gauss_Y,guass_X,height,index
    after_lane=pd.read_csv(after_lane_path,header=None,delim_whitespace=True,dtype='double')
    
    #建立索引
    x_max=after_lane[4].max()
    x_min=after_lane[4].min()
    y_max=after_lane[5].max()
    y_min=after_lane[5].min()
    x_difference=x_max-x_min
    y_difference=y_max-y_min
    x_index_num=math.ceil(x_difference/10)
    y_index_num=math.ceil(y_difference/10)
    
    #网格索引
    #计算方法：floor(x-x_min)+ceil(y-y_min)*x_index_num
    after_lane_np=after_lane.values
    index_row=np.floor((after_lane_np[:,4]-x_min)/10)+np.ceil((after_lane_np[:,5]-y_min)/10)*x_index_num
    after_lane[8]=index_row
    #检索
    current_gird=after_lane[after_lane[8]==32].copy()
        
    #传入坐标点position
    #x=position.x
    #y=position.y
    
    x=after_lane.loc[0,4]
    y=after_lane.loc[0,5]
    
    current_gird[9]=((current_gird[4]-x)**2+(current_gird[5]-y)**2)**0.5
    current_point_id=current_gird[9].idxmin()
    
    if(current_point_id-10>=0):
        min_point_id=current_point_id-10
    else:
        min_point_id=0
    if(current_point_id+50<=after_lane.shape[0]):
        max_point_id=current_point_id+50
    else:
        max_point_id=lane_path.shape[0]
        
