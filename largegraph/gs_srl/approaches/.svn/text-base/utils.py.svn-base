'''
Created on May 13, 2015

@author: irma
'''
import math,os,random,tempfile
import OBDsearch
import networkx as nx

def choose_root_node(pattern,root_node_predicate_name,hist):
    possible_root_nodes=[]
    print hist
    if(root_node_predicate_name==None):
        for i in xrange(0,len(hist)):
            root_node_predicate_name=hist[i][0] #choose the root node predicate
            possible_root_nodes=[x for x in pattern.nodes() if pattern.node[x]['predicate']==root_node_predicate_name and pattern.node[x]['valueinpattern']==0]            
            if root_node_predicate_name=='references':
                continue
            if(len(possible_root_nodes)==0):
               print "no possible root nodes for: ",root_node_predicate_name
               continue
            
            ran=random.randint(0,len(possible_root_nodes)-1)
            root_node=possible_root_nodes[ran]
            if OBDsearch.get_heuristic4_OBD(pattern, startNode = root_node)==None:
                print "no obd search for: ",root_node
                continue
            
            root_node_predicate_name=pattern.node[root_node]['predicate']
            print "Root predicate name determined to be: ",pattern.node[root_node]['predicate']
            break

    else:
        print "root predicate name: ",root_node_predicate_name
        possible_root_nodes=[x for x in pattern.nodes() if pattern.node[x]['predicate']==root_node_predicate_name]
        print possible_root_nodes
        ran=random.randint(0,len(possible_root_nodes)-1)
        root_node=possible_root_nodes[ran]
    
    return root_node,pattern.node[root_node]['predicate']

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
    print hist
    for i in xrange(0,len(hist)):
            root_node_predicate_name=hist[i][0] #choose the root node predicate
            possible_root_nodes=[x for x in pattern.nodes() if pattern.node[x]['predicate']==root_node_predicate_name and pattern.node[x]['valueinpattern']==0]            
            if root_node_predicate_name=='references':
                continue
            if(len(possible_root_nodes)==0):
               print "no possible root nodes for: ",root_node_predicate_name
               continue
            
            for root_node in possible_root_nodes:
              if OBDsearch.get_heuristic4_OBD(pattern, startNode = root_node)==None:
                print "no obd search for: ",root_node
              else:
                obds.append(OBDsearch.get_heuristic4_OBD(pattern, startNode = root_node))

    
    return obds


def get_valid_orderings(pattern,partial_ordering,res):
    #res=[]
    final_node=partial_ordering[-1]
    neighbours=[]
    for n in partial_ordering:
        neighbours.extend(pattern.neighbors(n))
    result=None
    set(neighbours)
    #print "FINAL NODE: ",final_node
    #print "neighbours: ",neighbours
    
    if len(partial_ordering)==len(pattern):
                  #print "FINAL!!!! partial ordering: ",partial_ordering
                  return partial_ordering
    
    for neighbour in neighbours:
        part_ord_local=[e for e in partial_ordering]
        #print "Partial: ",part_ord_local,"RES: ",res
        #print neighbour,partial_ordering
        if not neighbour in partial_ordering:
            #print "Neighbour: ",neighbour
            appended_list=[e for e in partial_ordering]     
            appended_list.append(neighbour)
            #print "Appended list: ",appended_list
            result=get_valid_orderings(pattern,appended_list,res)
            #print "Final node:",final_node,"Appending",result,"to",res
            #print "Final node:",final_node,"RES: ",appended_list,partial_ordering,part_ord_local  
            #print "Return :",result,"to upper level" 
            if len(appended_list)==len(pattern):
              res.append(result)
              #print "Resulting into: ",res
            else:
              res=result
              #print "Not appended: ",res
                      
        

    
    return res
        
def permutations(head, tail=''):
    if len(head) == 0: print tail
    else:
        for i in range(len(head)):
            permutations(head[0:i] + head[i+1:], tail+head[i])    


# def get_all_random_orderings(pattern,hist):
#     possible_root_nodes=[]
#     obds=[]
#     print hist
#     for i in xrange(0,len(hist)):
#             root_node_predicate_name=hist[i][0] #choose the root node predicate
#             possible_root_nodes=[x for x in pattern.nodes() if pattern.node[x]['predicate']==root_node_predicate_name and pattern.node[x]['valueinpattern']==0]            
#             if root_node_predicate_name=='references':
#                 continue
#             if(len(possible_root_nodes)==0):
#                print "no possible root nodes for: ",root_node_predicate_name
#                continue
#             
#             for root_node in possible_root_nodes:
#               if get_valid_orderings(pattern, startNode = root_node)==None:
#                 print "no obd search for: ",root_node
#               else:
#                 obds.append(OBDsearch.get_heuristic4_OBD(pattern, startNode = root_node))
#     return obds

def get_all_random_orderings(pattern,hist):
    possible_root_nodes=[]
    obds=[]
    print hist
    for i in xrange(0,len(hist)):
            root_node_predicate_name=hist[i][0] #choose the root node predicate
            print "ROOT NODE: ",root_node_predicate_name
            possible_root_nodes=[x for x in pattern.nodes() if pattern.node[x]['predicate']==root_node_predicate_name and pattern.node[x]['valueinpattern']==0]            
            if root_node_predicate_name=='user':
                print "HALO:",possible_root_nodes
                for n in pattern.nodes():
                    print pattern.node[n]['predicate'],pattern.node[n]['valueinpattern']
            if root_node_predicate_name=='references':
                continue
            if(len(possible_root_nodes)==0):
               print "no possible root nodes for: ",root_node_predicate_name
               continue
             
            for root_node in possible_root_nodes:
               print root_node
               obds.extend(get_valid_orderings(pattern, [root_node],[]))
    return obds
              
if __name__ == '__main__':
    gml='''graph [
  name "/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_FACEBOOK//patterns_size_7/batch5/facebookpattern_22e189ecaa7443628b9be8fd2de9b507/facebookpattern_22e189ecaa7443628b9be8fd2de9b507.parent"
  node [
    id 0
    label "language"
    predicate "language"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 1
    label "user"
    predicate "user"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 2
    label "education_type"
    predicate "education_type"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 3
    label "user"
    predicate "user"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 4
    label "language"
    predicate "language"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 5
    label "education_degree"
    predicate "education_degree"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 6
    label "hometown"
    predicate "hometown"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 7
    label "gender = value_78"
    predicate "gender"
    target 0
    valueinpattern 1
    type "None"
    value "value_78"
  ]
  edge [
    source 0
    target 1
  ]
  edge [
    source 1
    target 2
  ]
  edge [
    source 1
    target 3
  ]
  edge [
    source 1
    target 5
  ]
  edge [
    source 3
    target 4
  ]
  edge [
    source 3
    target 6
  ]
  edge [
    source 3
    target 7
  ]
]'''
# 
    pattern=string_to_pattern(gml)
    
    results=get_valid_orderings(pattern, [0],[])
    for r in results:
        print r


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
    print "Number of observations for exhaustive: ",nr_observations
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
