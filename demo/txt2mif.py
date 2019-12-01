# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:13:48 2019

@author: HCHO
"""

#转mif线数据

#arcgis生成点数据
file_input=open("车道拓扑线点.txt")
line=file_input.readline()
line=file_input.readline()
all_Line=[]
id=None
while(line):
    one_line=line.split(',')
    if(id!=one_line[1]):
        all_Line.append([])
        all_Line[-1].append((round(float(one_line[2]),6),round(float(one_line[3]),6)))
        id=one_line[1]
    elif id==one_line[1]:
        all_Line[-1].append((round(float(one_line[2]),6),round(float(one_line[3]),6)))
    line=file_input.readline()


file_output=open("车道拓扑线.mif",'w')
for item in all_Line:
    file_output.write('Pline '+str(len(item))+'\n')
    for little_item in item:
        file_output.write(str(little_item[0])+' '+str(little_item[1])+'\n')
    
file_input.close()
file_output.close()

'''
#采集点数据,即中心线
file_input=open("车道中心线.mid",encoding='utf-8')
line=file_input.readline()
line=file_input.readline()
all_Line=[]
id=None
while(line):
    one_line=line.strip().split('\t')
    id=one_line[0]
    file=open('车道中心线\\'+id+'.txt')
    all_Line.append([])
    aline=file.readline()
    while(aline):
        aline_list=aline.split(' ')
        all_Line[-1].append((round(float(aline_list[4]),6),round(float(aline_list[5]),6)))        
        aline=file.readline()
    file.close()
    line=file_input.readline()


file_output=open("车道中心线.mif",'w')
for item in all_Line:
    file_output.write('Pline '+str(len(item))+'\n')
    for little_item in item:
        file_output.write(str(little_item[0])+' '+str(little_item[1])+'\n')
    
file_input.close()
file_output.close()
'''