'''
Created on Feb 24, 2015

@author: irma
'''
import math

import matplotlib.pyplot as plt
# matplotlib.use('Qt4Agg')
import networkx as nx  # @UndefinedVariable

import graph.graph_analyzer as man


def convert_readable_format_to_graph(readable_format):
    string_split=readable_format.replace("'","").split("], [")
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
    return G


#Plot one graph with matplotlib
def visualize_graph(graph,name):
    positions = nx.spring_layout(graph)
    node_labels = nx.get_node_attributes(graph,'label')
    list_target_nodes,list_others,head_node=get_target_node_ids(graph)
    nx.draw_networkx_nodes(graph,positions,list_target_nodes,node_color='y',node_size=500,alpha=0.8)
    nx.draw_networkx_nodes(graph,positions,list_others,node_color='r',node_size=500,alpha=0.8)
    nx.draw_networkx_nodes(graph,positions,head_node,node_color='y',node_size=500,alpha=0.8)
    nx.draw_networkx_labels(graph, positions,labels=node_labels)
    nx.draw(graph,positions)
    plt.savefig(name+'.png')
    plt.close()
    
    
    
def visualize_graph_standard(graph): 
     positions = nx.spring_layout(graph)
     limits=plt.axis('off')
     fig = plt.figure(1)
     fig.show()
     nx.draw_networkx_nodes(graph,positions)
     nx.draw_networkx_edges(graph,positions)
     nx.draw_networkx_labels(graph,positions)
     plt.draw()
     plt.show()
     
    
    
#Visualize a list of graphs in matplotlib. The graphs are distributed in #columns and #rows   
def visualize_multiple_graphs(list_of_graphs):
    counter=1
    for graph in list_of_graphs:          
        positions = nx.circular_layout(graph)
        node_labels = nx.get_node_attributes(graph,'label')
        half=math.floor(len(list_of_graphs)/2)
        if(len(list_of_graphs)==1):
            rows=1
            columns=1
        if(len(list_of_graphs)==2):
            rows=2
            columns=1
        else:
            rows=int(half)
            columns=int(half)
        plt.subplot(rows,columns,counter)
        list_target_nodes,list_others,head_node=get_target_node_ids(graph)
        nx.draw_networkx_nodes(graph,positions,list_target_nodes,node_color='b',node_size=500,alpha=0.8)
        nx.draw_networkx_nodes(graph,positions,list_others,node_color='r',node_size=500,alpha=0.8)
        nx.draw_networkx_nodes(graph,positions,head_node,node_color='y',node_size=500,alpha=0.8)
        nx.draw_networkx_labels(graph, positions,labels=node_labels)
        nx.draw(graph,positions)
        counter+=1
    plt.show()

def visualize_multiple_graphs_row_column(rows,columns,list_of_graphs):
    counter=1
    for graph in list_of_graphs:          
        positions = nx.circular_layout(graph)
        node_labels = nx.get_node_attributes(graph,'label')
        plt.subplot(rows,columns,counter)
        list_target_nodes,list_others,head_node=get_target_node_ids(graph)
        nx.draw_networkx_nodes(graph,positions,list_target_nodes,node_color='b',node_size=500,alpha=0.8)
        nx.draw_networkx_nodes(graph,positions,list_others,node_color='r',node_size=500,alpha=0.8)
        nx.draw_networkx_nodes(graph,positions,head_node,node_color='y',node_size=500,alpha=0.8)
        nx.draw_networkx_labels(graph, positions,labels=node_labels)
        nx.draw(graph,positions)
        counter+=1
    plt.show()

def get_target_node_ids(graph):
    result_targets=[]
    result_others=[]
    result_head=[]
    head=[]
    for node in graph.nodes():
        if(graph.node[node]['target']==1):
                result_targets.append(node)
                continue
        if('head' in graph.node[node].keys() and graph.node[node]['head']==1):
                head.append(node)
                continue
        else:
                result_others.append(node)
    return result_targets,result_others,head


# Save graph as gml format
def save_graph_as_gml(graph,path_to_destination):
    nx.write_gml(graph,path_to_destination)    
    

#Given a graph and a label name, print all the nodes in the graph having the label
def print_graph_nodes_labels(graph,label_name):
    str=''
    for i in range(1,len(graph.nodes())+1):
        try:
            str+=graph.node[i]['label']+'-'
        except KeyError:
            continue
    return str

if __name__ == '__main__':
    pattern='/home/irma/work/DATA/DATA/IMDB/experiments_worked_under/PATTERNS/pattern1/pattern.gml'
    graph=nx.read_gml(pattern)
    visualize_graph_standard(graph)
    cycles = man.is_there_cycle_in_graph(graph)