'''
Created on Oct 12, 2015

@author: irma
'''
import networkx as nx
import networkx.algorithms.isomorphism as iso

pattern1_path="/home/irma/workspace/Martin_Experiment/PATTERNS/PATTERNS_DBLP/patterns_size_4/batch1/patt10/patt10.gml"
pattern2_path="/home/irma/workspace/Martin_Experiment/PATTERNS/PATTERNS_DBLP/patterns_size_4/batch1/patt9/patt9.gml"

patt1=nx.read_gml(pattern1_path)
patt2=nx.read_gml(pattern2_path)

nm = iso.categorical_node_match('label', 'label')
print nx.is_isomorphic(patt1,patt2,nm)