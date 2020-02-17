import os
import networkx as nx
import tempfile
from networkx.readwrite.gml import read_gml, write_gml

#The directory of the patterns
pattern_dir = ''



for subdir, dirs, files in os.walk(pattern_dir):
    for file in files:
        print(subdir.replace("patterns", "tree_patterns"))
        print(subdir + "/" + file)
        
        if ".gml" in file:
            G = nx.read_gml(subdir + "/" + file, label='id')
            for n in G.nodes():
                print(G.node[n])
            
            """
            if nx.is_tree(G):
                if not os.path.exists(subdir.replace("patterns", "tree_patterns")):
                    os.makedirs(subdir.replace("patterns", "tree_patterns"))
                write_gml(G, subdir.replace("patterns", "tree_patterns") + "/" + file)
        
            print(os.path.join(subdir, file))
            """

print("Found all patterns which are trees")
