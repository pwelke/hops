'''
Created on Nov 12, 2015

@author: irma
'''
'''
jusr for some short scripts
'''
import os,pickle
import networkx as nx

if __name__ == '__main__':
    path="/home/irma/workspace/Martin_Experiment/PATTERNS/PATTERNS_DBLP/test_pattern/short_data_graph.gml"
    data_graph=nx.read_gml(path)
    pickout = open(os.path.join("/home/irma/workspace/Martin_Experiment/PATTERNS/PATTERNS_DBLP/test_pattern/",'short_data.pickle'), 'wb')
    pickle.dump(data_graph, pickout)
    pickout.close()