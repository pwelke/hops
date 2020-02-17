import os
import networkx as nx
import tempfile
from networkx.readwrite.gml import read_gml, write_gml
from networkx.drawing.nx_pydot import graphviz_layout
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.algorithms.distance_measures import center
from networkx.algorithms.shortest_paths.generic import shortest_path_length
from GraphDataToGraphList import *
import matplotlib.pyplot as plt
import operator

def main():
    main_path = '/home/...'
    main_out_path = '/ExperimentsWEBKB10hExtended/'
    
    #path of the approaches
    approaches_path =  main_path + '/code/gs_srl/approaches/'
    #path of the graphs
    graph_data_path = main_path + '/data_ravkic/graphs/'
    #path of the tree patterns
    tree_patterns_data = main_path + '/data_ravkic/tree_patterns/'
    #path of the import files
    import_path = 'export PYTHONPATH="' + main_path + '/code/gs_srl/"'
    #path of the experiments output files
    #output_path = main_path + '/code/HOPS_Experiments/'
    output_path = main_path + main_out_path
    
    #name of the database
    data = "YEAST"
    #name of the 
    pickle = "YEAST.gpickle"

    
    def get_maximum_degree_nodes(pattern):
        max=0
        max_node = []
        for node in pattern.nodes():
            if pattern.degree(node)>max:
                max=pattern.degree(node)
                max_node = [node]
            elif pattern.degree(node) == max:
                max_node.append(node)
        return max_node
    
    def get_center_nodes(pattern):
        return center(pattern)
    
    def get_dist_to_center(pattern):
        center_dist = {}
        center = get_center_nodes(pattern)
        for n in pattern.nodes():
            min_length = len(pattern.nodes())
            for center_node in center:
                length = shortest_path_length(pattern, n, center_node)
                if length < min_length:
                    min_length = length
            center_dist[n] = min_length
        return sorted(center_dist.items(), key=operator.itemgetter(1))
            
            
        
    
    graph_path = "/home/.../yeastpattern_44f876cfdc1c429ab91e6fd7ffd45b2f.gml"
    G = nx.read_gml(graph_path, label='id')
    labelstop = {}
    labelsbot = {}
    
    for n in G.nodes.data():
        print(n[1])
        labelstop[n[0]] = n[1]['predicate'] + str(n[1]['target'])
        labelsbot[n[0]] = n[1]['valueinpattern']
    print(G.nodes())
    print(G.edges())
    nodes = get_maximum_degree_nodes(G)
    print(nodes)
    nodes = get_center_nodes(G)
    print(nodes)
    dist_to_center = get_dist_to_center(G)
    print(dist_to_center)
    root_node = 0
    for node in dist_to_center:
        if node[0] in [6, 5, 14]:
            root_node = node[0]
            break
    print(root_node)

    pos = graphviz_layout(G, prog='dot')
    postop = {}
    posbot = {}
    for key, value in pos.items():
        postop[key] = (value[0], value[1]+12)
    for key, value in pos.items():
        posbot[key] = (value[0], value[1]-15)
    nx.draw(G, pos, with_labels = True)
    nx.draw_networkx_labels(G, postop, labelstop)
    nx.draw_networkx_labels(G, posbot, labelsbot)
    plt.show()
    

if __name__ == '__main__':
    main()
