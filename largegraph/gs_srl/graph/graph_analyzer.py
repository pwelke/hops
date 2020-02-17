'''
Created on Feb 25, 2015

@author: irma
'''
import networkx as nx
from collections import defaultdict
from operator import itemgetter
import operator
from graph.nodes import *
from graph.nodes import Randvar_value_test
from networkx.algorithms.distance_measures import center
from networkx.algorithms.shortest_paths.generic import shortest_path_length


def pattern_to_readable_text_format(pattern,output_file):
    '''
    Given a pattern in networkx format, make a text file that will have the pattern in format:
    nodes: [(node1,node2...nodeN)]
    edges: [(node1,node2),(node2,nodeN)...]
    '''
    nodes=[] #array of labels
    all_edges=[] #array of tuples
    dictionary_number={}
    for n in pattern.nodes():
        nodes.append(pattern.node[n]['label'])
        edges=pattern.neighbors(n)
        for edge in edges:
           connection=[pattern.node[n],pattern.node[edge]]
           reverse_connection=connection[::-1]
           #the edges are considered to be bidirectional
           if not reverse_connection in all_edges:
              all_edges.append(connection)
    with open(output_file,'w') as f:
        f.write("Nodes: "+str(nodes)+"\n")
        f.write("Edges: "+str(all_edges)+"\n")
        
def get_readable_text_format(pattern):
    '''
    Given a pattern in networkx format, make a text file that will have the pattern in format:
    nodes: [(node1,node2...nodeN)]
    edges: [(node1,node2),(node2,nodeN)...]
    '''
    nodes=[] #array of labels
    all_edges=[] #array of tuples
    dictionary_number={}
    for n in pattern.nodes():
        nodes.append(str(pattern.node[n]['id'])+":"+pattern.node[n]['label'])
        edges=pattern.neighbors(n)
        for edge in edges:
           connection=[str(pattern.node[n]['id']),str(pattern.node[edge]['id'])]
           reverse_connection=connection[::-1]
           #the edges are considered to be bidirectional
           if not reverse_connection in all_edges:
              all_edges.append(connection)
    return (nodes,all_edges)
    
        
def get_graph_shape(pattern):
    if nx.is_bipartite(pattern) and nr_nodes_with_degree_bigger_than(pattern,4)==1:
        return "star"
    if nx.is_bipartite(pattern) and nr_nodes_with_degree_bigger_than(pattern,4)>1:
        return str(nr_nodes_with_degree_bigger_than(pattern,4))+"_star"
    if is_there_cycle_in_graph(pattern):
        return "cycle"
    if not is_there_cycle_in_graph(pattern) and nr_nodes_with_degree(pattern,1)==2:
        return "chain"
    if not is_there_cycle_in_graph(pattern) and nr_nodes_with_degree(pattern,3)==1:
        return "T"
    if not is_there_cycle_in_graph(pattern) and nr_nodes_with_degree(pattern,3)>1:
        return str(nr_nodes_with_degree(pattern,3))+"_T"

def nr_nodes_with_degree_bigger_than(pattern,threshold):
    counter=0
    for node in pattern.nodes():
       if pattern.degree(node)>threshold:
           counter+=1
    return counter

def nr_nodes_with_degree(pattern,degree):
    counter=0
    for node in pattern.nodes():
       if pattern.degree(node)==degree:
           counter+=1
    return counter

def get_N_nodes_with_the_highest_degree(data_graph,predicate_name,N):
    '''
    :param data_graph:
    :param predicate_name:
    :param N:
    :return:
    '''
    if(N==0):
        return []
    
    if(isinstance(data_graph,str)):
        data_graph=nx.read_gpickle(data_graph)
        
    nodes=sorted(data_graph.degree_iter(),key=itemgetter(1),reverse=True)[0:len(data_graph.nodes())]
    selected_nodes=[]
    selected_labels=[]
    res=[]

    
    for nd,degree in nodes:
        
        if(data_graph.node[nd]['predicate']==predicate_name):
            selected_nodes.append(data_graph.node[nd])
        
    for nd in selected_nodes:
       
        if(not(nd['label'] in selected_labels)):
            res.append(nd)
            selected_labels.append(nd['label'])
            if len(res)==N:
                break
    return res

def getNumberOfDistinctNodeValue(data_graph,predicate_name):
    number=0
    seen=[]
    for n in data_graph.nodes():
        if(data_graph.node[n]['predicate']==predicate_name):
            if(not(data_graph.node[n] in seen)):
                seen.append(data_graph.node[n])
                number+=1
    return number


def get_all_possible_constants(data_graph, predicate_name):
    '''
    Get all the nodes with values from data graph for a specific predicate
    '''
    nodes_with_values = []
    nodes = []

    for n in data_graph.nodes():
        if data_graph.node[n]['predicate'] == predicate_name:
            if (not (data_graph.node[n]['name'] in nodes_with_values)):
                nodes_with_values.append(data_graph.node[n]['name'])
                nodes.append(data_graph.node[n])
    return nodes

def get_all_possible_values(data_graph, predicate_name):
    '''
    Get all the nodes with values from data graph for a specific predicate
    '''
    values = []

    for n in data_graph.nodes():
        if data_graph.node[n]['predicate'] == predicate_name:
            if (not (data_graph.node[n]['name'] in values)):
                values.append(data_graph.node[n]['value'])
    return values


def get_all_possible_nodes_wtih_values_in_data_graph(data_graph,predicate_name,subset):
    '''
    Get all the nodes with values from data graph for a specific predicate
    '''
    frequency={}
    nodes_with_values=[]
    nodes=[]
    
    for n in data_graph.nodes():
        if(data_graph.node[n]['predicate']==predicate_name and 'value' in data_graph.node[n].keys()):
            if not data_graph.node[n]['value'] in frequency.keys():
                frequency[data_graph.node[n]['value']]=1
            else:
                frequency[data_graph.node[n]['value']]+=1
            if(not(data_graph.node[n]['value'] in nodes_with_values)):
                nodes_with_values.append(data_graph.node[n]['value'])
                nodes.append(data_graph.node[n])
    if subset:
        sorted_x = sorted(frequency.items(), key=operator.itemgetter(1))
        selected_labels=sorted_x[-5:]
        label_names=[]
        for s in selected_labels:
            label_names.append(s[0])
        selected_nodes=[]
        for s in nodes:
            if s['value'] in label_names:
                selected_nodes.append(s)
        return selected_nodes
    return nodes
        
def add_values_in_pattern_for_graph_if_missing(pattern):
    for node in pattern.nodes():
        if pattern.node[node]['valueinpattern']==1:
            if('value' in pattern.node[node] and pattern.node[node]['value']!=None):
                continue
            value=pattern.node[node]['label'].split('=')[1].lstrip()
            pattern.node[node]['value']=value
    
             
def get_sorted_labels_by_occurence_frequency_in_graph(data_graph_path):
    '''
    Given  a data graph, find histogram w.r.t. predicate names of the nodes. The method returns
    a list of tuples sorted from least occurring to most occurring nodes in the graph.
    :param data_graph_path: path to the domain graph
    :param labels: labels of interest
    :return: return list of tuples (predicate_name,number_of_occurences) (sorted from least occurring, to most occurring)
    '''
    if(isinstance(data_graph_path,str)):
        if(data_graph_path.endswith(".gpickle")):
          data_graph=nx.read_gpickle(data_graph_path)
        else:
          data_graph=nx.read_gml(data_graph_path)
    
    
    f=lambda s,d={}:([d.__setitem__(data_graph.node[i]['predicate'],d.get(data_graph.node[i]['predicate'],0)+1) for i in s],d)[-1]   
    hist=f(data_graph.nodes())
    sorted_x = sorted(hist.items(), key=operator.itemgetter(1))
    return sorted_x

def get_sorted_labels_by_occurence_frequency_in_graph_hops(data_graph):
    '''
    Given  a data graph, find histogram w.r.t. predicate names of the nodes. The method returns
    a list of tuples sorted from least occurring to most occurring nodes in the graph.
    :param data_graph_path: path to the domain graph
    :param labels: labels of interest
    :return: return list of tuples (predicate_name,number_of_occurences) (sorted from least occurring, to most occurring)
    '''

    f=lambda s,d={}:([d.__setitem__(data_graph.node[i]['predicate'],d.get(data_graph.node[i]['predicate'],0)+1) for i in s],d)[-1]   
    hist=f(data_graph.nodes())
    sorted_x = sorted(hist.items(), key=operator.itemgetter(1))
    return sorted_x


def count_nr_randvars_in_graph(pattern):
    tmp=0
    for node in pattern.nodes():
        if pattern.node[node]['valueinpattern']==1:
           tmp+=1
    return tmp

def is_there_cycle_in_graph(pattern):
    if len(list(nx.cycle_basis(pattern)))>0:
        return True
    else:
        return False
    

def get_maximum_node_degree(pattern):
    max=0
    for node in pattern.nodes():
       if pattern.degree(node)>max:
           max=pattern.degree(node)
    return max

#Hops code
def get_maximum_degree_nodes(pattern):
    max=0
    max_node = []
    for node in pattern.nodes():
        if pattern.degree(node)>max:
            max=pattern.degree(node)
            max_node = [node]
            max_node_predicates = [pattern.node[node]["predicate"]]
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
 

#

def get_average_node_degree(pattern):
    avg=0.0
    for node in pattern.nodes():
       avg+=pattern.degree(node)     
    return avg/len(pattern.nodes())

def get_nr_target_nodes_other_than_head(pattern):
    n=0
    for node in pattern.nodes():
        if pattern.node[node]['target']==1:
            n+=1
    return n

#Given a list of predicates for which we want all possible ranvar value tests,
#and given an input data graph, we extract a mapping from predicate to the randvar value tests
def extract_possible_randvar_tests_from_input_graph(input_data_graph_path,randvar_value_tests_predicates):
    Graph=nx.read_gpickle(input_data_graph_path)
    predicate_nodes_map=defaultdict(list)
    nr_vertices=len(nx.nodes(Graph))
    for counter in range(0,nr_vertices):
        for randvar_test_predicate in randvar_value_tests_predicates:
            if Graph.node[counter]['predicate']==randvar_test_predicate:
                predicate_nodes_map[Graph.node[counter]['predicate']].append(Graph.node[counter]['label'])
    return predicate_nodes_map
    

#checks if the new graph is isomorphic to the existing graphs 
def is_isomorphic_to_current_list(new_graph,existing_graphs):
    for graph in existing_graphs:
        if(nx.is_isomorphic(new_graph,existing_graphs)):
            return True
        else:
            return False

    '''
    given a label extract value of the node
    '''
def get_value(label): 
        strings=label.split('=')
        return strings[1]

def get_data_graph_summary(graph):
    info_tuples=[]
    has_values_in_patterns=[]
    neighbours={}
    for node in graph.nodes():
        predicate=graph.node[node]['predicate']
        if predicate=='constant':
             neighb=nx.neighbors(graph, node)
             #if len(neighb)==1:
             print(graph.node[node])
             print("******************************")
             for ne in neighb:
                print(graph.node[ne])
             print("-------------------------------------")
        #get neighbours
        if not predicate in neighbours.keys():
            neighb=nx.neighbors(graph, node)
            neighbors=[]
            for ne in neighb:
                neighbors.append(graph.node[ne]['predicate'])
            neighbours[predicate]=neighbors

    
def create_randvar_value_test(node,associated_type):
        return Randvar_value_test(node, node['value'],associated_type)
    
def count_nr_target_predicates(pattern):
    targets=0
    for node in pattern.nodes():
        if "target" in pattern.node[node].keys():
            if pattern.node[node]['target']==1:
                targets+=1
    return targets
        
if __name__ == '__main__':
    pattern_path='/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/PATTERNS_proba_2_brisi/patterns_size_4/batch1/yeastpattern_1457560400/yeastpattern_1457560400.gml'
    pattern=nx.read_gml(pattern_path)
    pattern_to_readable_text_format(pattern,'/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/PATTERNS_proba_2_brisi/patterns_size_4/batch1/yeastpattern_1457560400/yeastpattern_1457560400.readable')
    



