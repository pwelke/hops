'''
Created on May 13, 2015

@author: irma
'''
import math
import random
import tempfile
import networkx as nx
import operator
from OBDs import OBDsearch
from graph import graph_analyzer as analyzer

#hops code
from networkx.algorithms.distance_measures import center
from networkx.algorithms.shortest_paths.generic import shortest_path_length

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

def choose_root_node(pattern, root_node_predicate_name, hist, root_node_list = None, root_node_alg = None):
    #start hops code choose different root nodes
    if root_node_list != None and root_node_alg == "MaxDeg":
        ran = random.randint(0, len(root_node_list) - 1)
        root_node = root_node_list[ran]
    elif root_node_alg == "MinLabel":
        for i in xrange(0, len(hist)):
            root_node_predicate_name = hist[i][0]  # choose the root node predicate with min label occurance
            if root_node_predicate_name == 'references':
                continue
            possible_root_nodes = [x for x in pattern.nodes() if pattern.node[x]['predicate'] == root_node_predicate_name and pattern.node[x][
                                       'valueinpattern'] == 0]
            if (len(possible_root_nodes) == 0):
                continue
            break
        ran = random.randint(0, len(possible_root_nodes) - 1)
        root_node = possible_root_nodes[ran]
    elif root_node_alg == "MinLabelMaxDegree":
        for i in xrange(0, len(hist)):
            root_node_predicate_name = hist[i][0]  # choose the root node predicate with min label occurance
            if root_node_predicate_name == 'references':
                continue
            possible_root_nodes = [x for x in pattern.nodes() if
                                       pattern.node[x]['predicate'] == root_node_predicate_name and pattern.node[x][
                                       'valueinpattern'] == 0]
            if (len(possible_root_nodes) == 0):
                continue
            break
        max_degree = 0
        for r_node in possible_root_nodes:
            if pattern.degree(r_node) > max_degree:
                max_degree = pattern.degree(r_node)
                root_node = r_node
    elif root_node_alg == "Central":
        centers = get_center_nodes(pattern)
        ran = random.randint(0, len(centers) - 1)
        root_node = centers[ran]
    elif root_node_alg == "MinLabelCentral":
        for i in xrange(0, len(hist)):
            root_node_predicate_name = hist[i][0]  # choose the root node predicate with min label occurance
            if root_node_predicate_name == 'references':
                continue
            possible_root_nodes = [x for x in pattern.nodes() if
                                       pattern.node[x]['predicate'] == root_node_predicate_name and pattern.node[x][
                                       'valueinpattern'] == 0]
            if (len(possible_root_nodes) == 0):
                continue
            break
        dist_to_center = get_dist_to_center(pattern)
        for node in dist_to_center:
            if node[0] in possible_root_nodes:
                root_node = node[0]
                break
    #end hops code
    elif (root_node_predicate_name == None):
        for i in xrange(0, len(hist)):
            root_node_predicate_name = hist[i][0]  # choose the root node predicate
            if root_node_predicate_name == 'references':
                continue
            possible_root_nodes = [x for x in pattern.nodes() if
                                   pattern.node[x]['predicate'] == root_node_predicate_name and pattern.node[x][
                                       'valueinpattern'] == 0]
            if (len(possible_root_nodes) == 0):
                continue

            ran = random.randint(0, len(possible_root_nodes) - 1)
            root_node = possible_root_nodes[ran]
            if OBDsearch.get_heuristic4_OBD(pattern, startNode=root_node) == None:
                continue
            break
    else:
        possible_root_nodes = [x for x in pattern.nodes() if pattern.node[x]['predicate'] == root_node_predicate_name]
        ran = random.randint(0, len(possible_root_nodes) - 1)
        root_node = possible_root_nodes[ran]
    return root_node, pattern.node[root_node]['predicate']

def generate_monitoring_marks(time_interval_in_seconds, max_time_in_seconds):
    counter = 0
    marks = []
    while counter + time_interval_in_seconds <= max_time_in_seconds:
        marks.append(counter + time_interval_in_seconds)
        counter = counter + time_interval_in_seconds
    return marks

def string_to_pattern(gml_string):
    pattern = None
    with tempfile.NamedTemporaryFile() as f:
        f.write(gml_string)
        f.flush()
        pattern = nx.read_gml(f.name)
    return pattern


def get_all_obds(pattern, hist):
    possible_root_nodes = []
    obds = []
    print hist
    for i in xrange(0, len(hist)):
        root_node_predicate_name = hist[i][0]  # choose the root node predicate
        possible_root_nodes = [x for x in pattern.nodes() if
                               pattern.node[x]['predicate'] == root_node_predicate_name and pattern.node[x][
                                   'valueinpattern'] == 0]
        if root_node_predicate_name == 'references':
            continue
        if (len(possible_root_nodes) == 0):
            print "no possible root nodes for: ", root_node_predicate_name
            continue

        for root_node in possible_root_nodes:
            if OBDsearch.get_heuristic4_OBD(pattern, startNode=root_node) == None:
                print "no obd search for: ", root_node
            else:
                obds.append(OBDsearch.get_heuristic4_OBD(pattern, startNode=root_node))

    return obds

def string_to_pattern(gml_string):
    pattern=None
    with tempfile.NamedTemporaryFile() as f:
       f.write(gml_string)
       f.flush()
       pattern=nx.read_gml(f.name)
    return pattern

def get_all_obds(pattern,hist):
    possible_root_nodes=[]
    obds=[]
    for i in range(0,len(hist)):
            root_node_predicate_name=hist[i][0] #choose the root node predicate
            possible_root_nodes=[x for x in pattern.nodes() if pattern.node[x]['predicate']==root_node_predicate_name and pattern.node[x]['valueinpattern']==0]            
            if root_node_predicate_name=='references':
                continue
            if(len(possible_root_nodes)==0):
               continue
            for root_node in possible_root_nodes:
              if OBDsearch.get_heuristic4_OBD(pattern, startNode = root_node)==None:
                print("no obd search for: ",root_node)
              else:
                obds.append(OBDsearch.get_heuristic4_OBD(pattern, startNode = root_node))

    
    return obds


def get_valid_orderings(pattern,partial_ordering,res):
    neighbours=[]
    for n in partial_ordering:
        neighbours.extend(pattern.neighbors(n))
    set(neighbours)
    if len(partial_ordering)==len(pattern):
                  #print "FINAL!!!! partial ordering: ",partial_ordering
                  return partial_ordering
    
    for neighbour in neighbours:
        if not neighbour in partial_ordering:
            appended_list=[e for e in partial_ordering]
            appended_list.append(neighbour)
            result=get_valid_orderings(pattern,appended_list,res)
            if len(appended_list)==len(pattern):
              res.append(result)
            else:
              res=result
    return res
        
def permutations(head, tail=''):
    if len(head) == 0:
        print(tail)
    else:
        for i in range(len(head)):
            permutations(head[0:i] + head[i+1:], tail+head[i])    


def get_all_random_orderings(pattern,hist):
    obds=[]
    for i in range(0,len(hist)):
            root_node_predicate_name=hist[i][0] #choose the root node predicate
            possible_root_nodes=[x for x in pattern.nodes() if pattern.node[x]['predicate']==root_node_predicate_name and pattern.node[x]['valueinpattern']==0]
            if root_node_predicate_name=='references':
                continue
            if(len(possible_root_nodes)==0):
               continue
            for root_node in possible_root_nodes:
               obds.extend(get_valid_orderings(pattern, [root_node],[]))
    return obds
              

def get_observation_intervals_and_root_node_id(path_to_info_file):
    '''
    Get interval of limits on the number of observation. The input file has to be the output of the exhaustive algorithm
    and contain line: Total number of observations: Number
    :param path_to_info_file: path to exhaustive approach output file
    :returns list of intervals of length 15, root_node id determined from exhaustive approach
    '''
    nr_observations=0
    root_node_id=0
    nr_embeddings=0

    with open(path_to_info_file, 'r') as f:
       for line in f:
        if str('Number of embeddings:') in line:
            strings=line.split(':')
            nr_embeddings=int(strings[1].strip())
        if str('Total number of observations:') in line:
            strings=line.split(':')
            nr_observations=int(strings[1].strip())
        if str('root node id:') in line:
            strings=line.split(':')
            root_node_id=int(strings[1].strip())
            
    if(root_node_id==-1):
        raise Exception("root node not specified!!!")
            
    interval_length=int(math.ceil((nr_observations/15)))
    intervals=[1]
    for i in range(1,15):
        intervals.append(intervals[i-1]+interval_length+1)
    return intervals,root_node_id,nr_embeddings


def get_observation_intervals_and_root_node_id_max_obs(path_to_exhaustive_res,nr_observations_max):
    '''
    Get interval of limits on the number of observation. The input file has to be the output of the exhaustive algorithm
    and contain line: Total number of observations: Number
    :param path_to_info_file: path to exhaustive approach output file
    :returns list of intervals of length 15, root_node id determined from exhaustive approach
    '''
    nr_observations=nr_observations_max
    root_node_id=0

    with open(path_to_exhaustive_res, 'r') as f:
       for line in f:
        if str('root node id:') in line:
            strings=line.split(':')
            root_node_id=int(strings[1].strip())
            
    if(root_node_id==-1):
        raise Exception("root node not specified!!!")
            
    interval_length=int(math.ceil((nr_observations/15)))
    intervals=[1]
    for i in range(1,16):
        intervals.append(intervals[i-1]+interval_length+1)
    return intervals,root_node_id
