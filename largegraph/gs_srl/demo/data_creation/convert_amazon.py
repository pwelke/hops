'''
Created on Oct 26, 2016

@author: irma
'''
from graph import visualization as vis
import networkx as nx
import pickle
from graph import graph_analyzer as an

FILE_NAME = "amazon/amazon.gpickle"
edges="DATA/amazon/amazon.txt"

edges_map={}
nodes={}
nr_edges=0
line_nr=0

node_id=0
with open(edges,'r') as f:
    for line in f.readlines():
        line_nr+=1
        print("Line: ",line_nr)
        edge1=int(line.split("\t")[0].rstrip())
        edge2=int(line.split("\t")[1].rstrip())
        if edge1 not in nodes:
            nodes[edge1]=node_id
            node_id+=1
        if edge2 not in nodes:
            nodes[edge2]=node_id
            node_id+=1
        if edge1 in edges_map.keys():
            edges_map[edge1].append(edge2)
            nr_edges+=1
        else:
            edges_map[edge1]=[edge2]
            nr_edges+=1


G=nx.Graph() 
for n in nodes.keys():
    G.add_node(nodes[n],id=nodes[n],predicate='user')
     
for e in edges_map.keys():
    for e1 in edges_map[e]:
      G.add_edge(nodes[e],nodes[e1])
 
pickle.dump(G, open(FILE_NAME,'wb'))

data=nx.read_gpickle(FILE_NAME)
print("Nr nodes AMAZON: ",len(data.nodes()))
print("Nr edges AMAZON: ",len(data.edges()))
print("Max degree AMAZON: ",an.get_maximum_node_degree(data))
print("Density AMAZON: ",nx.density(data))
print("INFO AMAZON:",nx.info(data))
#print an.get_maximum_node_degree(graph)

number_of_pages=0
for node in data.nodes():
        if data.node[node]['predicate']=='page':
            number_of_pages+=1
vis.visualize_graph_standard(data)