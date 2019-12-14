# -*- coding: utf-8 -*-
"""
Created on Thu May 30 08:25:46 2019

@author: HCHO
"""
#GPS点提取软件。用于GPS点截取，道路关系需同时借助excel记录
#即在使用软件选取Lane的同时，生成文件名即为LaneID, 自行定义Road ID匹配
#Conn的对应关系文件，也由人工记录
#后期加入显示路段的功能，从而在截取结束后，可再行记录，确保准确
#导出数据，制表符和空格的问题？

import sys
import PySide2
import os
import pandas as pd
from pandas.core.frame import DataFrame
from PySide2.QtCore import Qt
from PySide2 import QtWidgets,QtCore,QtGui

from PySide2.QtWidgets import (QApplication, QWidget,QGridLayout,QDirModel,QTreeView)
from PySide2.QtCore import QObject, Signal, Slot

import Wgs84ToGauss
import DouglasPeucker
import math

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path 

#自定义点
class userPoint():
    id=''
    #屏幕坐标
    local_point=QtCore.QPointF()
    #绘制点坐标
    draw_point=QtCore.QPointF()

class disPoint():
    def __init__(self,pid,x,y):
        self.id=pid
        self.draw_point=QtCore.QPointF(x,y)
    
#QpointF指小数
#进行坐标系变换。
class MyPainter(QtWidgets.QWidget):
    valueChanged=QtCore.Signal()
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setPalette(QtGui.QPalette(QtGui.QColor(250, 250, 200)))
        self.setAutoFillBackground(True)
        
        #缩放比例、偏移量
        self.scale_wheel_bool=False
        self.mouse_move_bool = False
        self.scale=1
        self.offset=QtCore.QPointF(0, 0)
                       
        #屏幕点，用于计算转换矩阵
        self.scale_point=QtCore.QPointF(0,0)
        self.last_transform=''
        #self.press_point=QtCore.QPointF(0,0)
        
        #self.endMousePosition=QtCore.QPointF(0,0)
        self.preMousePosition=QtCore.QPointF(0,0)
        
        self.Qstart=QtCore.QPointF(0,0)
        #数据
        self.allPoint=[]
        self.displayPoint=[]
        self.missionPoint_list=[]
        self.target_point=0
        
        self.start_point=userPoint()
        self.end_point=userPoint()
        
    #inputData为打开文件的文件名
    #y坐标取相反数
    def addData(self,inputData):
        self.data = pd.read_csv(inputData,header=None,delim_whitespace=True,dtype='double')        
        self.data=self.data.round(10)
        
        self.all_gnss_data=[]
        for i in range (0,self.data.shape[0]):
            t=DouglasPeucker.GnssData(list(self.data.iloc[i,:]))
            self.all_gnss_data.append(t)
        
        #存取数据点信息
        self.allPoint=[]
        self.displayPoint=[]        
        for item in self.all_gnss_data:
            self.allPoint.append(disPoint(item.id,item.y,-item.x))
        #深拷贝
        self.displayPoint=self.allPoint.copy()
        
        #原点，逻辑坐标.定位数据点范围
        if(len(self.allPoint)!=0):
            point0=self.allPoint[0].draw_point
            self.Qstart=self.Qstart+point0
    
    #加载mission点数据
    #y坐标取相反数
    def addPointData(self,inputData):
        self.missionPoint=pd.read_csv(inputData,header=None,delim_whitespace=True,dtype='double') 
        self.missionPoint=self.missionPoint.round(10)
        
        self.missionPoint_list=[]
        for i in range (0,self.missionPoint.shape[0]):
            t=QtCore.QPointF(self.missionPoint.iloc[i,1],-self.missionPoint.iloc[i,0])
            self.missionPoint_list.append(t)
        
        
    #获取逻辑坐标有问题，没有解决好以鼠标为中心缩放的问题
    #没解决Qt默认左上为原点的问题。不宜进行整体翻转，会影响字体及平移。
    #Y轴翻转问题，由self.allPoint.append(disPoint(item.id,item.x,-item.y))解决
    #内容太多，写的不好，宜转换为多个独立函数
    #6.19  22：14鼠标为中心缩放问题，get√
    def paintEvent(self,event):
        self.painter = QtGui.QPainter(self)
        self.painter.begin(self)  
        

        #QRect窗口
        window_rect=self.painter.window()        
        window_rect.setSize(QtCore.QSize(window_rect.width()*self.scale,window_rect.height()*self.scale))
        
        #简单平移缩放
        #self.Qstart=QtCore.QPointF(self.offset.x()*self.scale,self.offset.y()*self.scale)+point0
        #self.Qstart
        self.painter.setWindow(self.Qstart.x(),self.Qstart.y(),window_rect.width(),window_rect.height())
        
        
        #转换矩阵
        transform=self.painter.combinedTransform()
        #存储transform
        self.last_transform=transform
        '''
        #paint部分
        self.painter.setPen(QtCore.Qt.blue)
        self.painter.drawPoint(99,99)
        self.painter.drawPoint(100.5,100.5)
        
        self.painter.setPen(QtCore.Qt.NoPen)
        self.painter.setBrush(QtCore.Qt.black)
        rect=QtCore.QRect(100, 100, 100,100)
        self.painter.drawRect(rect)
        self.painter.drawRect(QtCore.QRect(0,0, 50,50))
        
        #屏幕点坐标转换        
        p=transform.inverted()[0].map(self.press_point)
        #print(p)
        if self.mouse_move_bool == False and self.mouse_move_bool == False:
            if rect.contains(p):
                self.painter.setBrush(QtCore.Qt.blue)
                self.painter.drawRect(rect)
        '''
        #绘制数据点
        
        if(len(self.allPoint)!=0):
            self.painter.setPen(QtCore.Qt.black)
            self.painter.setBrush(QtCore.Qt.black)

            for item in self.displayPoint:
                #self.painter.drawPoint(QtCore.QPointF(item.x,item.y))
                self.painter.drawEllipse(item.draw_point,0.1,0.1)
        
        if(len(self.missionPoint_list)!=0):            
            self.painter.setPen(QtCore.Qt.red)
            self.painter.setBrush(QtCore.Qt.red)
            for item in self.missionPoint_list:
                self.painter.drawEllipse(item,0.2,0.2)

        
        #屏幕点坐标转换
        if(self.target_point):
            p1=transform.inverted()[0].map(self.start_point.local_point)
            if(self.target_point==2):
                p2=transform.inverted()[0].map(self.end_point.local_point)
            #print(p1.x(),p2.x(),0)
            #print(p1)
            #对选取点绘制，平移缩放状态不进行选取。
            if self.scale_wheel_bool == False and self.mouse_move_bool == False:                
                #寻找目标点并存储
                if(self.target_point==1):
                    for item in self.displayPoint:                    
                        distance1=math.sqrt((item.draw_point.x()-p1.x())**2+(item.draw_point.y()-p1.y())**2)
                        if distance1<0.3:
                            self.start_point.id=item.id
                            self.start_point.draw_point=item.draw_point
                            self.valueChanged.emit()
                    if(self.start_point.id==''):
                        self.target_point=0       
                if(self.target_point==2):
                    for item in self.displayPoint:
                        distance2=math.sqrt((item.draw_point.x()-p2.x())**2+(item.draw_point.y()-p2.y())**2)
                        if distance2<0.3:
                            self.end_point.id=item.id
                            self.end_point.draw_point=item.draw_point
                            self.valueChanged.emit()
                    if(self.end_point.id==''):
                        self.target_point=1
                #print(self.start_point.id,self.end_point.id)
            #绘制
            self.painter.setPen(QtCore.Qt.blue)
            self.painter.setBrush(QtCore.Qt.blue)
            self.painter.setRenderHint(self.painter.Antialiasing)
            self.painter.setFont(QtGui.QFont("Times", 1, QtGui.QFont.Bold))
            if(self.target_point==1):
                self.painter.drawEllipse(self.start_point.draw_point,0.1,0.1)
                self.painter.drawText(self.start_point.draw_point ,str(self.start_point.id))
            elif(self.target_point==2):
                self.painter.drawEllipse(self.start_point.draw_point,0.1,0.1)
                self.painter.drawText(self.start_point.draw_point ,str(self.start_point.id))
                self.painter.drawEllipse(self.end_point.draw_point,0.1,0.1)
                self.painter.drawText(self.end_point.draw_point ,str(self.end_point.id))

        '''        
        #显示注释
        self.painter.setPen(QtCore.Qt.black)
        self.painter.setRenderHint(self.painter.Antialiasing);
        self.painter.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold));
        
        self.painter.drawText( 200,200 ,"mia san mia")
        '''
        self.painter.end()
        
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:              # 左键按下            
            if(self.target_point==0):
                self.start_point.local_point = event.localPos()
                self.target_point=1
            elif(self.target_point==1):
                self.end_point.local_point = event.localPos()
                self.target_point=2
            self.preMousePosition = event.localPos()
            print(self.last_transform.inverted()[0].map(event.localPos()))
            self.repaint()
            self.mouse_move_bool = True; 
        
        elif event.buttons() == QtCore.Qt.RightButton: 
            self.target_point=0
            self.start_point.id=''
            self.end_point.id=''
            self.repaint()
            self.valueChanged.emit()
            
            
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:                            # 左键释放
            self.mouse_move_bool = False;
        '''
        elif event.button() == Qt.RightButton:                                 # 右键释放
            self.offset = QtCore.QPointF(0, 0)                                  
            self.scale=1
            self.target_point=0
            self.start_point=''           
            self.end_point=''                             
        '''
    def mouseMoveEvent(self,event):
        if self.mouse_move_bool:                                               # 左键按下
            #self.endMousePosition = event.localPos() - self.preMousePosition        # 鼠标当前位置-先前位置=单次偏移量
            logical_coord1=self.last_transform.inverted()[0].map(event.localPos())
            logical_coord2=self.last_transform.inverted()[0].map(self.preMousePosition)


            #self.offset=self.offset-(logical_coord1-logical_coord2)
            #self.Qstart=QtCore.QPointF(self.offset.x()*self.scale,self.offset.y()*self.scale)
            self.Qstart=self.Qstart-(logical_coord1-logical_coord2)
            self.preMousePosition = event.localPos()                                # 更新当前鼠标在窗口上的位置，下次移动用
            self.repaint()                                                     

    '''无法获取鼠标的逻辑坐标，在此仅实现伪地图缩放'''
    #已解决缩放问题
    def wheelEvent(self, event):
        delta=1.2
        angle=event.angleDelta() / 8                                           # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        self.angleY=angle.y()                                                       # 竖直滚过的距离
        
        self.scale_point=event.posF()        
        self.scale_wheel_bool=True
        
        logical_coord=self.last_transform.inverted()[0].map(self.scale_point)
        o_coord=self.last_transform.inverted()[0].map(QtCore.QPointF(0,0))
        if self.angleY > 0:                                                    # 滚轮上滚
            self.scale=self.scale*delta
            new_coord=logical_coord+(o_coord-logical_coord)*delta
        else:                                                                  # 滚轮下滚
            self.scale=self.scale/delta
            new_coord=logical_coord+(o_coord-logical_coord)/delta
        
        self.Qstart=new_coord
        self.repaint()                                                   
        self.scale_wheel_bool=False
    
    
    def get_point_id(self):
        pass
        

        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        #QWidget.__init__(self)
        
        self.createActions()
        self.createMenus()
        self.setWindowTitle("Map")
        self.painter=MyPainter()
        self.createLayout()
        
        self.fileName=''
        
        #按钮 选取状态
        self.state=False
        #QObject.connect(self.painter, QtCore.SIGNAL("get_point_id()"), self, QtCore.SLOT("stateDisplay()"))
        self.painter.valueChanged.connect(self.stateDisplay)
        self.button3.clicked.connect(self.clearPoint)
        self.button0.clicked.connect(self.displayPoint)
        self.button4.clicked.connect(self.createLane)
        self.button5.clicked.connect(self.createConn)

    #读取点号
    def stateDisplay(self):  
        self.brower1.setText(str(self.painter.start_point.id))
        self.brower2.setText(str(self.painter.end_point.id))
    
    def clearPoint(self):
        self.painter.target_point=0
        self.painter.start_point.id=''
        self.painter.end_point.id=''
        self.painter.repaint()        
        self.brower1.setText(str(self.painter.start_point.id))
        self.brower2.setText(str(self.painter.end_point.id))
    
    #根据输入框内id显示点号。当不显示时，需点击鼠标两下，由self.target_point的设计决定
    def displayPoint(self):
        self.painter.start_point.id=int(self.brower1.text())
        self.painter.start_point.draw_point=self.painter.allPoint[self.painter.start_point.id].draw_point
        self.painter.end_point.id=int(self.brower2.text())
        self.painter.end_point.draw_point=self.painter.allPoint[self.painter.end_point.id].draw_point
        self.painter.repaint() 
        
    #可能需要加入条件，起始点id小于终止点id。conn同
    def createLane(self):
        #self.painter.data
        msgBox = QtWidgets.QMessageBox()
        
        if(self.painter.start_point.id=='' or self.painter.end_point.id==''):
            msgBox.setText("输入错误")
        else:
            startline=self.painter.data[self.painter.data[0]==self.painter.start_point.id]
            endline=self.painter.data[self.painter.data[0]==self.painter.end_point.id]

            start_index=startline.index.values[0]
            end_index=endline.index.values[0]
            output_data=self.painter.data.iloc[start_index:end_index+1,:]
            #输出
            output_data[0]=output_data[0].astype('int64')
            num=len(os.listdir("outputDATA\\Lane"))
            output_data.to_csv('outputDATA\\Lane\\'+str(num)+'.txt',sep='\t',index=False,header=False)
            
            #此处不加等于即路段留有衔接点
            #存有部分点没删除？for in和remove的问题。
			#12.12 保留路段末尾处衔接点，用于生成道路
            for item in self.painter.allPoint:
                if int(item.id)>=int(self.painter.start_point.id) and int(item.id)<int(self.painter.end_point.id):                    
                    self.painter.displayPoint.remove(item)
                    #print(item.id,self.painter.start_point.id,self.painter.end_point.id)
            self.painter.repaint()      
                          
            msgBox.setText("已生成目标道路Lane"+str(num))
        msgBox.exec_()
    
    def createConn(self):
        #self.painter.data
        msgBox = QtWidgets.QMessageBox()
        if(self.painter.start_point.id=='' or self.painter.end_point.id==''):
            msgBox.setText("输入错误")
        else:
            startline=self.painter.data[self.painter.data[0]==self.painter.start_point.id]
            endline=self.painter.data[self.painter.data[0]==self.painter.end_point.id]
                
            start_index=startline.index.values[0]
            end_index=endline.index.values[0]
            output_data=self.painter.data.iloc[start_index:end_index+1,:]
            #输出
            output_data[0]=output_data[0].astype('int64')
            num=len(os.listdir("outputDATA\\Conn"))
            output_data.to_csv('outputDATA\\Conn\\'+str(num)+'.txt',sep='\t',index=False,header=False)
            
            for item in self.painter.allPoint:
                if int(item.id)>=int(self.painter.start_point.id) and int(item.id)<int(self.painter.end_point.id):                    
                    self.painter.displayPoint.remove(item)
                    #print(item.id,self.painter.start_point.id,self.painter.end_point.id)
            self.painter.repaint()
            
            msgBox.setText("已生成目标道路Conn"+str(num))
        msgBox.exec_()
    
    def fileList(self):
        #树状文件列表
        self.model = QDirModel()
        self.view = QTreeView(self)
        self.view.setModel(self.model)
        self.view.setColumnHidden(1,True)
        self.view.setColumnHidden(2,True)
        self.view.setColumnHidden(3,True)        
        self.view.setHeaderHidden(True)
        #self.view.setRootIndex(self.model.index("c:/"))
        self.layout.addWidget(self.view,0,0,2,1)
     
    def createLayout(self):
        self.widget=QWidget()
        self.setCentralWidget(self.widget)
        
        #栅格布局
        self.layout = QGridLayout()
        #设置拉伸因子，每一列的比例
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 4)
        #控件
        self.fileList()                
        self.layout.addWidget(self.painter,0,1)
        #页面
        self.button1 = QtWidgets.QLabel("起始点")
        self.brower1=QtWidgets.QLineEdit()
        self.button2 = QtWidgets.QLabel("终止点")
        self.brower2=QtWidgets.QLineEdit()                
        self.button3 = QtWidgets.QPushButton("清除")
        
        self.button0 = QtWidgets.QPushButton("显示点号")
        self.button4 = QtWidgets.QPushButton("生成Lane")
        self.button5 = QtWidgets.QPushButton("生成Conn")

        labelLayout1 = QtWidgets.QHBoxLayout()
        labelLayout2 = QtWidgets.QHBoxLayout()

        labelLayout1.addWidget(self.button1)
        labelLayout1.addWidget(self.brower1)
        labelLayout1.addWidget(self.button2)
        labelLayout1.addWidget(self.brower2)        
        labelLayout1.addWidget(self.button3)
        
        labelLayout2.addWidget(self.button0)
        labelLayout2.addWidget(self.button4)
        labelLayout2.addWidget(self.button5)
        
        self.layout.addLayout(labelLayout1,1,1)
        self.layout.addLayout(labelLayout2,2,1)
        self.widget.setLayout(self.layout)

        
    def createActions(self):
        self.openRoadAct = QtWidgets.QAction("加载道路数据", self, shortcut="Ctrl+O",triggered=self.openRoad)
        
        self.openPointAct = QtWidgets.QAction("加载点数据", self, shortcut="Ctrl+P",triggered=self.openPoint)
        #self.saveAsAct = QtWidgets.QAction("&Save As...", self, shortcut="Ctrl+S",triggered=self.saveAs)

        self.exitAct = QtWidgets.QAction("退出", self, shortcut="Ctrl+Q",triggered=self.close)

        #self.aboutAct = QtWidgets.QAction("&About", self, triggered=self.about)

        #self.aboutQtAct = QtWidgets.QAction("About &Qt", self,triggered=QtWidgets.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&打开")
        self.fileMenu.addAction(self.openRoadAct)
        self.fileMenu.addAction(self.openPointAct)
        #self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addAction(self.exitAct)
        
        self.menuBar().addSeparator()

        #self.helpMenu = self.menuBar().addMenu("&Help")
        #self.helpMenu.addAction(self.aboutAct)
        #self.helpMenu.addAction(self.aboutQtAct)
        
    #加载NovAtel文件数据
    def openRoad(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,
                "加载数据", QtCore.QDir.currentPath(), "Files (*.txt *.csv)")[0]

        if not fileName:
            return

        inFile = QtCore.QFile(fileName)
        if not inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtWidgets.QMessageBox.warning(self, "Text",
                    "Cannot read file %s:\n%s." % (fileName, inFile.errorString()))
            return

        #data = QtCore.QTextStream(inFile)
        #self.line=data.readAll()
        inFile.close()
        self.painter.addData(fileName)
    
    #加载MissionPoint文件数据
    #getOpenFileNames()函数，可打开多个文件
    def openPoint(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,
                 "加载数据", QtCore.QDir.currentPath(),"Files (*.txt *.csv)")[0] 
        if not fileName:
            return
        
        inFile = QtCore.QFile(fileName)
        if not inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtWidgets.QMessageBox.warning(self, "Text",
                    "Cannot read file %s:\n%s." % (fileName, inFile.errorString()))
            return
        inFile.close()
        self.painter.addPointData(fileName)
        
if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1600,1000)
    window.show()
    sys.exit(app.exec_())
     