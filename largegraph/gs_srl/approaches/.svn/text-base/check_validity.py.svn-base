'''
Created on May 17, 2015

@author: irma
'''
import argparse,sys,getopt,os
import networkx as nx


def main(args):
   # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"]) 
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    path=args.path
    experiment=args.experiment
    
    if experiment=='dblp':
        relation_predicates=['coauthored','dir','references']
    if experiment=='yeast':
        relation_predicates=['interaction']
    
    
    for p in os.listdir(path):
        if p.endswith(".gml"):
            pattern=os.path.join(path,p)
            #load pattern
            graph=nx.read_gml(pattern)
            if has_double_edge_for_relation_node(graph,relation_predicates):
                with open(os.path.join(path,'not_valid.info'),'w') as f:
                    f.write("not valid")
            
def disallowed_edges_for_relation_node(pattern_graph,relation_node):
    #for node in pattern_graph:
    #    print pattern_graph.node[node]
    for node in pattern_graph.nodes():
        if(pattern_graph.node[node]['predicate']==relation_node):
            if(len(nx.neighbors(pattern_graph, node))<2): #warning: allowed this here!!!
                return False
            if(len(nx.neighbors(pattern_graph, node))>2):
                return True
            else:
                neighbours=nx.neighbors(pattern_graph, node)
                node1=neighbours[0]
                node2=neighbours[1]
                #print "Has ",len(neighbours)," neighbours"
                #print pattern_graph.node[node1]['predicate']
                #print pattern_graph.node[node2]['predicate']
                #print pattern_graph.node[node]['type'].are_allowed_to_connect_undirected(pattern_graph.node[node1]['predicate'],pattern_graph.node[node2]['predicate'])
                if not pattern_graph.node[node]['type'].are_allowed_to_connect_undirected(pattern_graph.node[node1]['predicate'],pattern_graph.node[node2]['predicate']):
                    return True
    return False            
 
 
def has_double_edge_for_relation_node(graph,relation_predicates):
    result=[]
    flag=True
    for relation_node in relation_predicates:
            if(not(disallowed_edges_for_relation_node(graph,relation_node))):
                flag=True
            else:
                flag=False
                break
        if flag==True:
            result.append(graph) 
                
    return result           

if __name__ == '__main__':
    main(sys.argv[1:])