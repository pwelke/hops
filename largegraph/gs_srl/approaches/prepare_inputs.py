import os

import networkx as nx
import time

from OBDs import OBDsearch
from graph import graph_analyzer as analyzer
#from sampling_core import sampling_utils as utils
from approaches import utils as utils	

def prepare_params(args):
    if args.t==None:
        args.t=args.max_time
    monitoring_marks = utils.generate_monitoring_marks(args.t, args.max_time)
    try:
        data_graph = nx.read_gpickle(args.d)
    except:
        data_graph = nx.read_gml(args.d)
    
    pattern = nx.read_gml(args.p)
    if (not (os.path.exists(args.o))):
        os.makedirs(args.o)
        
    # DETERMINING ROOT NODE
    if args.root_node_name==None or args.root_node_id==None:
        ####hops make this faster
        hist = analyzer.get_sorted_labels_by_occurence_frequency_in_graph_hops(data_graph)
        ###
        #max degree node in pattern (hoPS)
        max_degree_nodes = None #analyzer.get_maximum_degree_nodes(pattern)
        root_node, root_node_predicate_name = utils.choose_root_node(pattern, None, hist, max_degree_nodes)
    else:
        root_node=args.root_node_id
        root_node_predicate_name=args.root_node_name

    # get images of root node in the data graph
    root_nodes = [x for x in data_graph.nodes() if data_graph.node[x]['predicate'] == root_node_predicate_name]
    OBdecomp = OBDsearch.get_heuristic4_OBD(pattern, startNode=root_node)
    if OBdecomp == None:
        no_obd_decomp = True
        OBdecomp = OBDsearch.get_flatList(pattern, startNode=root_node)
    Plist = [item for sublist in OBdecomp for item in sublist]
    return data_graph,pattern,OBdecomp,root_node,root_node_predicate_name,args.t,args.max_time,monitoring_marks,root_nodes,Plist
