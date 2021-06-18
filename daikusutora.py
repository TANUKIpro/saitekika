import numpy as np
from graphviz import Graph, Digraph

##  既知情報  ##
node_num = 6
edge_num = 9

#( origin | destination | weight )
edges = [(0,1,7),  (0,2,9),  (0,5,14),           #0
         (1,0,7),  (1,2,10), (1,3,15),           #1
         (2,0,9),  (2,1,10), (2,3,11), (2,5,2),  #2
         (3,1,15), (3,2,11), (3,4,6),            #3
         (4,3,6),  (4,5,9),                      #4
         (5,0,14), (5,2,2),  (5,4,9)]            #5
np_edges = np.array(edges)

## 探索条件
con_start = 0
con_goal  = 4

class Node:
    def __init__(self, name, destinations, weights):
        self.name = name
        self.destinations = destinations
        self.weights = weights
        
        self.label = float('INF')
        self.confirmed = False
        self.min_path = None

nodes = []
for i in range(node_num):
    matched_indexes = np.where(np_edges[:,0]==i)
    element_node   = np_edges[matched_indexes][:,1]
    element_weight = np_edges[matched_indexes][:,2]
    
    nd = Node(i, element_node,  weights=element_weight)
    nodes.append(nd)

## 初期設定
cfm = [0]*len(nodes)

s_node = nodes[con_start]
s_node.label = 0        #スタートのラベルを0に設定
s_node.confirmed = True #スタートを確定

min_label    = s_node.label
current_node = s_node

while(True):
    #未確定ノードから最小値のラベルを選択
    min_label = float('INF')
    for node in nodes:
        if (node.confirmed == False) and (min_label > node.label):
            min_label    = node.label
            current_node = node
            
    #ノードの確定
    current_node.confirmed = True
    
    print("#"*10)
    for node in nodes:
        print(node.confirmed)
    print("#"*10)
    
    #接続ノードのラベル更新
    min_weight = float('INF')
    weights = current_node.weights
    for i, dst in enumerate(current_node.destinations):
        dts_nd = nodes[dst]
        if dts_nd.confirmed == False:
            total_cost = current_node.label + weights[i]
            #ラベルの更新
            if dts_nd.label > total_cost:
                dts_nd.label = total_cost
                print(dts_nd.name, dts_nd.label)
            #最善ノードの確定
            if min_weight > total_cost:
                min_weight = dts_nd.label
                best_node  = dts_nd
                
    print("-"*10)
    print(current_node.name, best_node.name)
    #最善ノードの書き込み
    nodes[best_node.name].min_path = current_node.name
    print("----END----")
    
    #全ノードが確定で終了
    cfm[current_node.name] = 1
    if all(cfm):
        break