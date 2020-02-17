'''
Created on Nov 30, 2015

@author: irma
'''
import pickle,os
import networkx as nx

if __name__ == '__main__':
    path_to_file="/home/irma/workspace/dblp_graphs_proba/PATTERNS/test_pattern_1/short_data_graph.gml"
    graph=nx.read_gml(path_to_file)
    output=os.path.join("/home/irma/workspace/dblp_graphs_proba/PATTERNS/test_pattern_1/",'short_data.pickle')
    pickout = open(output, 'wb')
    pickle.dump(graph, pickout)
    pickout.close()