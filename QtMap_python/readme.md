## QtMap_python

#### 背景说明

1. 依赖环境：python3，开发库PySide2
2. 功能：由采集的原始的轨迹数据Lane和点数据MissionPoint生成规定的地图数据格式。
3. 原始数据格式：

- Lane	数据数据

- MissionPoint	标记点

  ###### 样例见DATA文件夹

4. 目标数据格式：

- Conn	连接线轨迹，文件名为connId

- Lane	车道线轨迹，文件名为laneId

- roadindex	第一列为road，第二列为lane

- connindex	第一列为conn，第二列为起始端road，第三列为连接端road

- conn2laneindex	第一列为conn，第二列为起始端lane，第三列为连接端lane

  ###### 样例见xc文件夹

###### 可参考“地图数据组织和功能模块”文件了解内容，文档有待完善。



#### 代码说明

##### dataPreProcessing.py

功能：数据预处理，包括①道路数据：添加id，数据压缩，文件合并，重赋id  ②点数据，文件合并，坐标转换

函数：pointPreProcessing()

说明：MissionPoint点数据预处理，将经纬度转为高斯坐标，生成MissionPoint_coordTranse.txt文件





函数：lanePreProcessing()

说明：Lane数据预处理，添加id，数据压缩，文件合并，重赋id，生成Lane_order.txt文件



##### Map.py

功能路径提取主程序，生成文件存在Lane和Conn文件夹下



##### DouglasPeucker.py

函数：outputResult(fileName)

说明：道格拉斯压缩算法函数

参数：输入参数为文件名fileName，输出文件为fileName_after.txt



##### Wgs84ToGauss.py

函数：Wgs84ToGauss(lon,lat,distinguish)

说明：坐标转换函数，WGS84转北京54坐标

参数：输入参数为经度、纬度、分带度数，返回值为北京54坐标



##### display_script.py

函数：merge1(outputFile,floder)

说明：全部数据合并，添加文件名字段，用于在arcgis中显示处理

参数：输入参数为输出文件名、文件夹名，输出为文件outputFile。



函数：merge2(outputFile,floder)

说明：全部数据合并，添加线段id及conn的连接字段、lane的road字段

参数：输入参数为输出文件名、文件夹名，输出为文件outputFile。



##### data_trans.py

函数：data_trans(filepath)

说明：自动转换脚本，由roadindex和conn2laneindex生成connindex文件

参数：输入参数为文件夹路径filepath，输出为文件connindex.txt



##### connindex_test.py

说明：connindex检查脚本，删除部分重复的Lane之后，检查connindex中需要修改的部分



### 使用说明

①操作文件夹按下面格式创建文件夹目录

- 文件夹
  - py文件...
  - DATA
    - Lane
    - MissionPoint
    - output
  - outputDATA
    - Conn
    - Lane

②在原始数据文件夹DATA内创建output文件夹，运行dataPreProcessing的pointPreProcessing和lanePreProcessing

③在DATA的同级目录下创建outputDATA，并在其下面创建Conn、Lane

④运行Map.py，点击打开加载道路数据Lane_order.txt，加载点数据MissionPoint_coordTranse.txt

然后开始点数据编辑，点击一个目标起始点和一个目标终止点，蓝色字会显示点号，确认为目标路段则点击生成Lane或Conn，则在outputDATA对应位置生成文件。同时这部分点会在界面上消失，避免影响之后绘制。当发现选择的点号不对时（终止点点号小于起始点，或着点错，过大等等），可点击鼠标右键或清除按钮。完成一次后点击清除或鼠标右键，开始下一次绘制。

![1571909937380](C:\Users\HCHO\AppData\Roaming\Typora\typora-user-images\1571909937380.png)





![1571909952714](C:\Users\HCHO\AppData\Roaming\Typora\typora-user-images\1571909952714.png)


