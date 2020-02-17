'''
Created on Oct 27, 2015

@author: irma
'''
import argparse,os,itertools
import networkx as nx
import graph_manipulator.graph_analyzer as man
import networkx.algorithms.isomorphism as iso

class Pattern:
    pattern_graph=None
    pattern_path=None
    parent_path=None
    
    def __init__(self, pattern_graph,gml_pattern_path):
        self.pattern_path=gml_pattern_path
        if(pattern_graph==None):
          self.pattern_graph=nx.read_gml(gml_pattern_path)
        else:
          self.pattern_graph=pattern_graph
          
    def __repr__(self):
       return str(man.get_readable_text_format(self.pattern_graph))


def get_all_subgraphs_child(parents_child):
    subgraphs={}
    print "Finding subgraphs ..."
    counter=1
    for pattern in parents_child:
        print "Finding subgraphs of: ",counter,"th child"
        counter+=1
        nodes=pattern.pattern_graph.nodes()
        perms=itertools.permutations(nodes,len(nodes)-1)
        subgraphs_list=[]
        for perm in perms:
            subgraphs_list.append(Pattern(nx.Graph(pattern.pattern_graph.subgraph(perm)),pattern.pattern_path))
        subgraphs[pattern.pattern_path]=subgraphs_list
    return subgraphs

def main(n_minus_1_pattern_path,n_pattern_level_path):
    selected_patterns_parent=[]
    selected_patterns_child=[]
    all_parent_permuted_graphs=[]
    with open(n_minus_1_pattern_path,'r') as f:
        for line in f.readlines():
            selected_patterns_parent.append(Pattern(None,os.path.join(line.replace("RESULTS","PATTERNS").rstrip()+"/"+line.split("/")[-1].rstrip().replace("/","")+".gml")))
    with open(n_pattern_level_path,'r') as f:
        for line in f.readlines():
            selected_patterns_child.append(Pattern(None,os.path.join(line.replace("RESULTS","PATTERNS").rstrip()+"/"+line.split("/")[-1].rstrip().replace("/","")+".gml")))
        
    nm = iso.categorical_node_match('label', 'label')
    print "Loaded all selected graphs ..."
    subgraphs=get_all_subgraphs_child(selected_patterns_child)
    print "Found all subgraphs ..."
    found_matches={}
    counter=1
    for pattern_path in subgraphs.keys():
         print "Processing ",counter,"child pattern"
         counter+=1
         match_found=False
         for parent in selected_patterns_parent:
             if match_found:
                 break
             for subgr in subgraphs[pattern_path]:                  
                if nx.is_isomorphic(subgr.pattern_graph,parent.pattern_graph,nm):
                    match_found=True
                    found_matches[pattern_path]=parent.pattern_path
                    break
                
             
    print "Nr matches: ",len(found_matches)
    for m in found_matches.keys():
        with open(os.path.join(m).replace("gml","parent"),"w") as f:
            f.write(found_matches[m].split("/")[-1].replace(".gml",""))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-parent_list',help='list file of parent selected patterns')
    parser.add_argument('-child_list',help='list file of child selected patterns')
    
    args = parser.parse_args()
    main(args.parent_list,args.child_list)