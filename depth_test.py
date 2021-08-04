#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:51:46 2019

@author: cynthiaperez818gmail.com
"""


# wanted to gather the depth of each tree another way of measuring number of generations
#also wanted to calculate size of each family tree 
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
#from networkx.readwrite import json_graph

print("Loading Family")
familinx = nx.read_edgelist("familinx_directed.txt",create_using= nx.DiGraph())
print(nx.info(familinx))

# def FindRootNode(Graph,Node):
#     NodePred=(list(Graph.predecessors(Node))) #get the two parents of this node
#     if(len(NodePred)==0): #If the list is empty then we have found the root node so we then break from recursion
#         return Node
#     else: #If the list is full when we have will take the first parent and return to the top if this function
#         PredList=[list(Graph.predecessors(NodePred[0])),list(Graph.predecessors(NodePred[1]))]
#         if(len(PredList[0])==2):
#             NewNode=NodePred[0]
#         else:
#             NewNode=NodePred[1]
#         return FindRootNode(Graph,NewNode)

def FindRootNode(Graph):
    Node={} #Creates an empty dictionary to add founder nodes and thier parent too.
    for node in Graph.nodes: #Iterates though all the nodes inside the subfamily
        if(len(list(Graph.predecessors(node)))==0): #Checks if the node's predecessors is empty, meaning they are a founder
            NodeDepth=(nx.shortest_path_length(G=H, source=node)) #Calculates the depth of the family
            keys = list(NodeDepth.keys()) #gets an array of all the key values
            Node[node]=NodeDepth[keys[-1]]
    RootNode = max(Node, key=Node.get) #Gets the key with the max depth of the family.
    print("The Root Node of the graph is Node "+str(RootNode)+" with a depth of " + str(Node[RootNode]+1)+" generation")
    return(Node[RootNode]+1)


print("Loading Family Data")
#connected families is a text file where each row is a family including individual IDs
f = open("connectedfamilies.txt", "r")
f.readline()
families = []
for line in f:
   families.append([line.strip('\n').split(',')]) 

new_families = []
for i in range(0, len(families)):
    if len(families[i][0]) >= 10:
        new_families.append(families[i][0])
print("Family Data Loaded")

# fam_6 = familinx.subgraph(new_families[6])
# print(list(fam_6.nodes))
# nx.draw(fam_6,with_labels=True, font_weight='bold')
# plt.savefig("subfamily_" + str(6) + ".png")
# plt.show()
  
FamilyDepth=[]
FamilySize=[]
for j in range(0,591761):
    print(j)
    sub_family = new_families[j]
    H = familinx.subgraph(sub_family)
    FamilyDepth.append(FindRootNode(H))
    FamilySize.append(len(H.nodes))
        # nx.draw(H,with_labels=True, font_weight='bold')
        # for i in sub_family:
        #     if(len(list(H.predecessors(i))) == 2):
        #         root_node = FindRootNode(H,i)
        # print(root_node)
        # print(nx.info(H))
        # Shortest_Path=nx.shortest_path_length(G = H, source = root_node)
        # keys=list(Shortest_Path.keys())
        # FamilyDepth.append(Shortest_Path[keys[-1]]+1)

np.save("FamilyDepth",FamilyDepth)
np.save("FamilySize",FamilySize)
      
        
