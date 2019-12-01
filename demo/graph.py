# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 15:35:15 2019

@author: HCHO
"""

import networkx as nx

g=nx.Graph()#创建空的无向图
#g=nx.DiGraph()#创建空的有向图

#点部分
g.add_node(1)
g.add_nodes_from([2,3,4])
g.nodes()
#NodeView((1, 2,3,4))
#添加属性
g.add_node(1,name='n1',weight=1)

g._node

g.node[1]

g.remove_node(4)

#删除顶点属性
del g.nodes[1]['name'] 

#检查是否有顶点1
g.has_node(1)


#边部分
g.add_edge(2,3)
g.add_edges_from([(1,2),(1,3)])
g.edges()
g.add_edge(1, 2, weight=4.7, relationship='renew')
#获取边权
g.get_edge_data(1,2)

#g.remove_edge(1,2)

del g[1][2]['weight']

g.edges[1,2]['weight'] = 4

g.has_edge(1,2)

#返回邻边属性
g.adj[1][2]
g.adj[1]

#返回EdgeView
g.edges()
g.edges.data()

#返回顶点信息
g.nodes()
g.nodes.data()

#
g.degree()


#图遍历
#查看顶点的相邻顶点
#g[n]
#g.adj[n]
#g.neighbors(n)

#查看图的相邻
for n, nbrs in g.adjacency():
    print(n)
    print(nbrs)
    


#绘制图   
nx.draw(g)
import matplotlib.pyplot as plt
plt.show()

g = nx.cubical_graph()
nx.draw(g, pos=nx.spectral_layout(g), nodecolor='r', edge_color='b')
plt.show()