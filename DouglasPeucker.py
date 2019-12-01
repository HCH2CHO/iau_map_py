# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 11:47:42 2019

@author: HCHO
"""

#对原始数据进行数据压缩

import math
#import Wgs84ToGauss
import pandas as pd

from pandas.core.frame import DataFrame

class DouglasPeucker():
    GeoDisThreshold=1.0
    GeoAngleThreshold=math.pi/2
    
    def __init__(self, sparse=0.1,dense=1.0):
        self.m_SparseThreshold=sparse;
        self.m_DenseThreshold=dense;
    
    #idlst为一维数组
    #const std::vector<int> &idlst,int id
    def Contain(self,idlst,id):
        for val in idlst:
            if(val==id):
                return True;
        return False;
    
    #caculate the distance from p3 to line (p1~p2)
    #const GnssData &p1, const GnssData &p2,const GnssData &p3
    def CalDist(self,p1, p2,p3):
        A = p2.y - p1.y;
        B = p1.x - p2.x;
        C = 0.0 - (p1.y*B + p1.x*A);
        m_dist = abs((A*p3.x + B*p3.y + C) / math.sqrt(A*A + B*B));
        return m_dist;
    
    #const GnssVec &input,bool check
    def Process(self,input,check):
        #std::cout << "[ Douglas Peucker ]Origin data : " << input.size() << std::endl;
        lane=[]
        lane=input[:];
        
        if(check):
            removelst=[];
            self.CheckMapBase(lane, removelst);

            tmp=[];
            for item in lane:
                if self.Contain(removelst, item.id):
                    continue
                else:
                    tmp.append(item)
            lane.swap(tmp);
            #std::cout << "[ Douglas Peucker ]After MapBase check : " << input.size() << std::endl;


        idLst=[];
        self.Doglas_Puke(0, len(lane) - 1, idLst, lane);
        idLst.append(lane[0].id);
        idLst.append(lane[-1].id);
        #std::cout << "[ Douglas Peucker ]Sparse result : " << idLst.size() << std::endl;

        idLst.sort()
        #为什么对sparse_data，dense_data做相同操作
        sparse_data=[];
        for item in lane:
            id=item.id
            if self.Contain(idLst,id):
                sparse_data.append(item)
                
        self.Dense(idLst, lane);
        #std::cout << "[ Douglas Peucker ]Dense result : " << idLst.size() << std::endl;
        dense_data=[];
        for item in lane:
            id=item.id
            if self.Contain(idLst,id):
                dense_data.append(item)
        return dense_data;


    #const GnssVec &data,std::vector<int> &idlst
    def CheckMapBase(self,data,idlst):
        check_iter=0

        iter1=check_iter;
        iter2=check_iter+1;
        iter3=check_iter+2;
        num=len(data)
        while(iter1!=num and iter2!=num and iter3!=num ):
            dis=self.CalDist(data[iter1],data[iter3],data[iter2]);

            vec1_x=data[iter1].x-data[iter2].x;
            vec1_y=data[iter1].y-data[iter2].y;
            vec1_module=math.sqrt(vec1_x*vec1_x+vec1_y*vec1_y);

            vec2_x=data[iter3].x-data[iter2].x;
            vec2_y=data[iter3].y-data[iter2].y;
            vec2_module=math.sqrt(vec2_x*vec2_x+vec2_y*vec2_y);

            vec_pro=vec1_x*vec2_x+vec1_y*vec2_y;
            cos=vec_pro/(2*vec1_module*vec2_module);

            angle=math.acos(cos);

            if(dis>self.GeoDisThreshold or angle<self.GeoAngleThreshold):
                idlst.append(data[iter2].id);
                iter2+=1;
                iter3+=1;
            else:
                iter1+=1;
                iter2+=1;
                iter3+=1;
    
    #int start, int end, std::vector<int> &idlst,const GnssVec &data        
    def Doglas_Puke(self,start,  end, idlst,data):
        if (start + 1 == end):       
            return;
        #maxDis = std::numeric_limits<double>::min();
        maxDis=0
        pos = -1;
        for i in range(start+1,end):
            dis = self.CalDist(data[start], data[end], data[i]);
            if (dis > maxDis):
                maxDis = dis;
                pos = i;

        if (maxDis < self.m_SparseThreshold or pos==-1):
            return;
        else:
            idlst.append(data[pos].id);
            self.Doglas_Puke(start, pos, idlst, data);
            self.Doglas_Puke(pos, end, idlst, data);

    
    #std::vector<int> &idlst, const GnssVec &data
    def Dense(self,idlst,data):
        disSum = 0;
        for i in range(0,len(data)-1):
            #p1 = data[i].copy();
            #p2 = data[i + 1].copy();
            p1 = data[i]
            p2 = data[i + 1]

            
            if(self.Contain(idlst,p2.id)):
                disSum=0;
                continue;

            distance=math.sqrt(abs(p1.x-p2.x)**2+abs(p1.y-p2.y)**2)
            
            disSum += distance;
            if (disSum > self.m_DenseThreshold):
                idlst.append(p2.id);
                disSum = 0;


class GnssData():
    def __init__(self, param):
    #def __init__(self, id=0):
        self.id=int(param[0]);        
        self.timestamp=param[1];
        self.lon=param[2];
        self.lat=param[3];
        self.x=param[4];
        self.y=param[5];
        self.hgt=param[6];
        self.roll=param[7];
        self.pitch=param[8];
        self.yaw=param[9];
        self.north= param[10];
        self.up=param[11];
        self.east=param[12];

        
#函数调用，处理地图数据，isId决定是否添加一列id
def outputResult(fileName,isId):
    gnss_data = pd.read_csv(fileName,header=None,delim_whitespace=True,dtype='double')
    #保留十位小数，如不设置保留位数会出现问题
    gnss_data=gnss_data.round(10)
    
    #根据isId判断是否需要插入id列
    if(isId):
        the_id=[i for i in range(0,gnss_data.shape[0])]
        the_id_dataframe=DataFrame(the_id)
        #axis  0沿着行的垂直往下，1沿着列的方向水平延伸
        gnss_data=pd.concat([the_id_dataframe,gnss_data],axis=1)
    
    #对全部数据建立GnssData对象
    all_gnss_data=[]
    for i in range (0,gnss_data.shape[0]):
        t=GnssData(list(gnss_data.iloc[i,:]))
        all_gnss_data.append(t)
    
    
    dp=DouglasPeucker()
    get_data=dp.Process(all_gnss_data,False)
    #get_data类型为列表，每一项为GnssData
    #数据压缩后重新赋id
    for i in range(0,len(get_data)):
        get_data[i].id=i
        
    #将get_data按原格式写入文件，or获取id，从gnss_data写入
    #去除row，yaw，pitch，加速度
    output=open(fileName.replace('.txt','')+'.after.txt','w')
    for item in get_data:
        #item_dict=item.__dict__
        line=''
        line=str(item.id)+' '+str(item.timestamp)+' '+str(item.lon)+' '+str(item.lat)+' '+str(item.x)+' '+str(item.y)+' '+str(item.hgt)+'\n'
        '''
        for word in item_dict:
            line=line+str(item_dict[word])+' '
        line=line+'\n'
        '''
        output.write(line)
    output.close()