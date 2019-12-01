# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 15:06:19 2019

@author: HCHO
"""
#道路生成
#Douglas压缩后存mif文件
from DouglasPeucker import *
import os

list_Lane = os.listdir("data\\lane")
for item in list_Lane:
    #reorderID("data\\lane\\"+item,"data\\output\\"+item,0)
    pass
    
    
#DouglasPeucker将每条轨迹抽稀后，每条轨迹中点的id从1~∞
#在arcgis中，根据MissionPoint对点添加截断属性，视该点为父点
    
#读取轨迹，并根据父点分割轨迹为lane，并生成lane之间的连接关系
#点id值需要重新赋值
def GenerateLane():
    pass


#道路去重算法，利用最小二乘法判断两条lane是否为同一lane，
#并结合方向判断是否为同一Road，生成road文件
#由lane的连接
def LaneMerge():
    pass