# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 09:56:10 2019

@author: HCHO
"""

#删除部分Lane之后，根据新老roadindex文件，检查connindex中需要修改的部分
#road=open("C:\\Users\\HCHO\\Desktop\\Map\\xc\\roadindex.txt",'r')
new_road=open("outputDATA\\new_roadindex.txt",'r')
conn2lane=open("outputDATA\\conn2laneindex.txt",'r')
new_conn2lane=open("outputDATA\\new_conn2laneindex.txt",'w')

lane_set=set()
line1=new_road.readline()
while(line1):
    line1=line1.strip().split('\t')
    if line1[1] not in lane_set:
        lane_set.add(line1[1])
    line1=new_road.readline()

line2=conn2lane.readline()
while(line2):
    
    line2=line2.strip().split('\t')
    if (line2[1] in lane_set and line2[2] in lane_set):
        new_conn2lane.write(line2[0]+'\t'+line2[1]+'\t'+line2[2]+'\n')
    elif(line2[1] in lane_set):
        new_conn2lane.write(line2[0]+'\t'+line2[1]+'\n')
    elif(line2[2] in lane_set):
        new_conn2lane.write(line2[0]+'\t'+'\t'+line2[2]+'\n')
    else:
        new_conn2lane.write(line2[0]+'\n')
    line2=conn2lane.readline()

    
new_road.close()
new_conn2lane.close()
conn2lane.close()