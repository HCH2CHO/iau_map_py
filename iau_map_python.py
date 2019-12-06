# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 08:38:43 2019

@author: HCHO
"""

import math
import networkx as nx
import matplotlib.pyplot as plt

#是否显示图像
show_animation = True

#定义节点.Graph中的Node包含以下信息      
class Node:
    def __init__(self,node_id,x,y):
        self.node_id=node_id
        self.x = x  #x坐标
        self.y = y  #y坐标
        self.cost=int #消耗
        self.pind=str #上一节点

            
class Planning:
    #建立路网图结构    
    def __init__(self,g):
        pass 
        
    #曼哈顿距离计算
    def calculate_distance(self,node1, node2):
        weight = 1 # weight of heuristic
        dis = weight * (abs(graph.node[node1]['x'] - graph.node[node2]['x']) + abs(graph.node[node1]['y'] - graph.node[node2]['y']) )
        return dis
    
    #根据pind寻找最短路径
    #ngoal为目的地，closedset为close表.返回值为最短路径列表
    def calculate_final_path(self, ngoal_id, closedset):
        final_path=[ngoal_id]
        pind = graph.node[ngoal_id]['pind']
        while pind != -1:
            n = pind
            final_path.append(n)
            pind = graph.node[n]['pind']
        final_path.reverse()
        return final_path
    
    #规划核心代码
    #node_start为起始点id，node_goal为目标点id
    def Astar_planning(self, start_nodeId,goal_nodeId):        
        open_set, closed_set =set(),set()
        open_set.add(start_nodeId)
        
        while 1:
            if len(open_set) == 0:
                print("Open set is empty..")
                break

            c_id = min(open_set, key=lambda item: graph.node[item]['cost'] + self.calculate_distance(goal_nodeId,item))
            current_id = c_id

            # show graph
            if show_animation:  # pragma: no cover
                plt.plot(graph.node[current_id]['x'],graph.node[current_id]['y'], "xc")
                if len(closed_set) % 2 == 0:
                    plt.pause(0.001)

            if current_id == goal_nodeId:
                print("Find goal")
                graph.node[goal_nodeId]['pind'] = graph.node[current_id]['pind']
                graph.node[goal_nodeId]['cost'] = graph.node[current_id]['cost']
                break

            # Remove the item from the open set
            open_set.remove(current_id)

            # Add it to the closed set
            closed_set.add(current_id)

            # expand_grid search grid
            for item in graph[current_id]:
                current_cost=graph.node[current_id]['cost']+graph[current_id][item]['weight']               
                if item in closed_set:
                    continue
                
                if item not in open_set:
                    open_set.add(item)  # discovered a new node
                    graph.node[item]['cost']=current_cost
                    graph.node[item]['pind']=current_id
                else:
                    if graph.node[item]['cost'] > current_cost:
                        graph.node[item]['cost']=current_cost
                        graph.node[item]['pind']=current_id
                

        path_return = self.calculate_final_path(goal_nodeId, closed_set)
        return path_return
    
if __name__ == '__main__':
    snode=Node(1,0,0)
    gnode=Node(9,4,4)
    
    #图的初始化
    graph=nx.DiGraph()
    #g.add_nodes_from([1,2,3,4,5,6,7,8,9])
    graph.add_node(1,x=0,y=0,cost=0,pind=-1)
    graph.add_node(2,x=2,y=0)
    graph.add_node(3,x=4,y=0)
    graph.add_node(4,x=0,y=2)
    graph.add_node(5,x=2,y=2)
    graph.add_node(6,x=4,y=2)
    graph.add_node(7,x=0,y=4)
    graph.add_node(8,x=2,y=4)
    graph.add_node(9,x=4,y=4,cost=0,pind=-1)
    graph.add_weighted_edges_from([(1,2,2.1),(2,3,2),(1,4,2),(2,5,2),(3,6,2),(4,7,2),(5,8,2),(6,9,2),(4,5,2),(5,6,2),(7,8,2),(8,9,2.1)])
    #nx.draw(g)
    
    if show_animation:
        plt.plot(snode.x, snode.y, "og")
        plt.plot(gnode.x, gnode.y, "xb")
        plt.grid(True)
        plt.axis("equal")
    
    planning = Planning(graph)
    path = planning.Astar_planning(snode.node_id, gnode.node_id)
    
    #最短路径的x,y
    path_x=[]
    path_y=[]
    for item in path:
        path_x.append(graph.node[item]['x'])
        path_y.append(graph.node[item]['y'])
        
    if show_animation:  # pragma: no cover
        plt.plot(path_x, path_y, "-r")
        plt.show()