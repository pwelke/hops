'''
Created on Mar 11, 2015

@author: irma
'''
import networkx as nx # @UndefinedVariable
import random
import graph_manipulator.visualization as vis


if __name__ == '__main__':
    Yeast=nx.read_gpickle("/cw/dtailocal/irma/Martin_paper/graph_sampling/graph_sampling/patternSampler/YEAST.gpickle")
    path="/cw/dtailocal/irma/Martin_paper/graph_sampling/graph_sampling/patternSampler/YEAST_smaller.gpickle"
    path="/cw/dtailocal/irma/Martin_paper/graph_sampling/graph_sampling/patternSampler/YEAST_smallest.gpickle"
    min_nr_nodes=float("inf")
    index_min_nr_nodes=0

    con_components=list(nx.connected_component_subgraphs(Yeast))
    for index,comp in enumerate(con_components):
       if len(comp.nodes())>min_nr_nodes:
           min_nr_nodes=len(comp.nodes())
           index_min_nr_nodes=index
    
    random_number_component=random.randint(0,len(list(con_components)))
    
    randomly_chosen_connected_component=con_components[random_number_component]
    minimum_connected_component=con_components[index_min_nr_nodes]
    nx.write_gml(randomly_chosen_connected_component, path)
    nx.write_gml(minimum_connected_component, path)
    print "nr nodes:",len(minimum_connected_component.nodes())
    #vis.visualize_graph(randomly_chosen_connected_component)