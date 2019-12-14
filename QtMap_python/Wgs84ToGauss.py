# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 14:51:00 2019

@author: HCHO
"""
import math
#输入参数，经度、纬度、分带度数
def Wgs84ToGauss(lon,lat,distinguish):
    RHO = 206265;
    order = 0;
    if (distinguish == 6):
        order = int(lon / 6) + 1
    else:
        order = int(lon / 3 + 0.5)

    L0 = 0
    if (distinguish == 6):
        L0 = 6 * order - 3
    else:
        L0 = 3 * order
    #print(L0)    
    CosB = math.cos(lat*math.pi/180)
    SinB = math.sin(lat*math.pi/180)
    CosBSquare = CosB * CosB
    #SinBSquare = SinB * SinB

    l = ((lon - L0) * 3600) / RHO;
    N = 6399698.902 - (21562.267 - (108.973 - 0.612 * CosBSquare) * CosBSquare) * CosBSquare;
    a0 = 32140.404 - (135.3302 - (0.7092 - 0.0040 * CosBSquare) * CosBSquare) * CosBSquare;
    a4 = (0.25 + 0.00252 * CosBSquare) * CosBSquare - 0.04166;
    a6 = (0.166 * CosBSquare - 0.084) * CosBSquare;
    a3 = (0.3333333 + 0.001123 * CosBSquare) * CosBSquare - 0.1666667;
    a5 = 0.0083 - (0.1667 - (0.1968 + 0.0040 * CosBSquare) * CosBSquare) * CosBSquare;
    x = 6367558.4969 * (lat * 3600) / RHO - (a0 - (0.5 + (a4 + a6 * l * l) * l * l)* l * l * N) * SinB * CosB;
    y = (1 + (a3 + a5 * l * l) * l * l) * l * N * CosB+500000;
    return x,y