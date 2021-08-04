#!/usr/bin/env python
# coding: utf-8

# In[2]:


import networkx as nx 
import random 
import itertools
import csv 
import os
import matplotlib.pyplot as plt


# In[22]:


perez = nx.read_edgelist("perez.edgelist.txt",create_using= nx.Graph()) # creates  non directed graph 


# In[23]:


di_perez = nx.read_edgelist("perez.edgelist.txt", create_using = nx.DiGraph()) #directed graph 


# In[24]:


nx.info(perez)


# In[25]:


print(list(perez.nodes))


# In[13]:


attrs = {}
with open ('perez_attributes.csv', 'r') as csv_file: 
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for line in csv_reader:
        attrs.update( {line[0]: {'alive' : line[1], 'birth_year': line[2]}} )

nx.set_node_attributes(perez, attrs)
print(list(perez.nodes(data = True))) 


# In[11]:


#creating a function where 50% of the family is in a database 
def in_database(percent = 50):
    return random.randrange(100) < percent


# In[12]:


for i in range(0, len(list(perez.nodes))):
    x = in_database()
    bool_attr = {list(perez.nodes)[i]: {'in_database': x}}
    nx.set_node_attributes(perez, bool_attr)


# In[13]:


filtered_nodes = [x for x,y in perez.nodes(data=True) if y['in_database'] == True]
print(filtered_nodes)
print(len(filtered_nodes))


# In[11]:


print(list(perez.nodes(data = True)))


# In[17]:


# function to identify all predecessors for node 
def full_list_predecessors (source):
    p = []
    p.append((list(di_perez.predecessors(source))))
    if len(p[0]) == 2:
        p.append(full_list_predecessors(p[0][0]))
        p.append(full_list_predecessors(p[0][1]))
    elif len(p[0]) == 1:
        p.append(full_list_predecessors(p[0][0]))
    
    p = list(itertools.chain(*p))
        
    return p


# In[60]:


pred19 = full_list_predecessors('19')

#8 and 13 are parents of 19, 1 and 2 are grandparents 
print(pred19)


# In[28]:


#each ID in order of how they are printed in print(str(list(perez.nodes)))
perez_pred = [['','1', '3', '4', '5', '6', '7', '8', '2', '14', '15', '16', '17', '21', '23', '24', '25', '26', '19', '20', '9', '10', '18', '11', '12', '13', '22', '29', '30', '50', '27', '28']]
print(perez_pred)


# In[29]:


#creating large table for node IDs in perez_pred 


#this first for loop stores the full list of predecessors for each node in perez
for id in list(perez.nodes):
    s = str(id)
    id_pred = full_list_predecessors(str(id))
    n = [s]
    
#comparing full list of predecessors between each family member in perez (t's predecessor list being compared to 
# s's predecessor list 

    for i in range (0, len(list(perez.nodes))):
        t = str(list(perez.nodes)[i])
        pred = full_list_predecessors(t)
        common_pred= [i for i in pred if i in id_pred]
        #len(common_pred)>=1 their common predecessor list (common_pred) is greater and equal to 1 
        # t in id_pred;  t is in the predecessor list of s 
        # s in pred, s is in the predeecessor list of t 
        if len(common_pred)>=1 or t in id_pred or s in pred:
            path = nx.shortest_path(perez, source = str(id), target = t)
            num_edges = len(path) - 1
            n.append(num_edges)
        else:
           n.append(0)
    perez_pred.append(n)
        
 #returns list of # of meiosis events between t and s         
print(perez_pred)        


# In[31]:


with open("FamilyMeiosisRelationship.csv",'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(0, len(perez_pred)):
        filewriter.writerow(perez_pred[i])


# In[ ]:


################################


# In[7]:


list(di_perez.predecessors("19"))


# In[8]:


path = nx.shortest_path(perez, source = "19", target = "20")


# In[9]:


print(path)


# In[26]:


#adding attributes continaing gender and age to each node 
profiles = []
with open('birth_year_perez.txt') as x:
    for line in x:
       profiles.append(line.split())  
    
attrs = {}
for d in range(0,len(profiles)):
    x = d +1    
    attrs.update( {str(x): {'gender' : profiles[d][0]}} )


# In[27]:


nx.set_node_attributes(perez, attrs)
print(list(perez.nodes(data = True))) 


# In[34]:


#function to print out relationship statements
def relative_type (path):
    relation = ""
    for x in range(0, len(path)-1):
        relative1 = str(path[x])
        relative2 = str(path[x+1])
        if relative2 in list(di_perez.predecessors(relative1)):
            if perez.nodes[relative2]['gender'] == 'Female':
                relation = relation + "mother"
            elif perez.nodes[relative2]['gender'] == 'Male': 
                relation = relation + "father" 
            else: 
                relation = relation + "parent"
        if relative2 in list(di_perez.successors(relative1)):
            relation = relation + "child"
    print(t, "is 19's", relation)


# In[35]:


id_pred = full_list_predecessors(str(19))
for i in perez.nodes:
    t = str(i)
    pred = full_list_predecessors(t)
    common_pred= [i for i in pred if i in id_pred]
    if len(common_pred)>=1 or t in id_pred:
        path = list(nx.all_shortest_paths(perez, source = "19", target = t))
        print(path)
        if len(path) == 1: 
            relative_type(path[0])
        else: 
            relative_type(path[0])
            relative_type(path[1])
            

