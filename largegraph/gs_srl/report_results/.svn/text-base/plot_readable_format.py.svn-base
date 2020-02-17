'''
Created on Oct 18, 2015

@author: irma
'''
import networkx as nx
import graph_manipulator.visualization as vis
import graph_manipulator.graph_analyzer as man

#readable_format="[['0', '1'], ['1', '2'], ['1', '3'], ['1', '4'], ['1', '9'], ['1', '10'], ['1', '11'], ['1', '12'], ['3', '5'], ['5', '8'], ['5', '6'], ['5', '7']]"
readable_format="[['0', '1'], ['1', '2'], ['1', '3'], ['1', '4'], ['1', '6'], ['1', '13'], ['3', '5'], ['5', '8'], ['5', '9'], ['5', '7'], ['6', '10'], ['10', '11'], ['10', '12'], ['13', '14']]"
string_split=readable_format.split("], [")
nodes=[]
edges=[]
for s in string_split:
    new_s=s.replace("'","").replace("[[","").replace("]]","")
    split_nodes=new_s.split(",")
    nodes.append(split_nodes[0].rstrip().lstrip())
    nodes.append(split_nodes[1].rstrip().lstrip())
    edges.append((split_nodes[0].rstrip().lstrip(),split_nodes[1].rstrip().lstrip()))

G=nx.Graph()
G.add_edges_from(edges)

vis.visualize_graph_standard(G)
print man.get_graph_shape(G)




