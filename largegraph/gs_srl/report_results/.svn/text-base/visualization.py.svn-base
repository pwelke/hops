'''
Created on Feb 24, 2015

@author: irma
'''
import networkx as nx # @UndefinedVariable
import matplotlib.pyplot as plt

def visualize_graph(graph):
    positions = nx.spring_layout(graph)
    node_labels = nx.get_node_attributes(graph,'label')
    nx.draw_networkx_labels(graph, positions,labels=node_labels)
    nx.draw(graph,positions)
    plt.show()