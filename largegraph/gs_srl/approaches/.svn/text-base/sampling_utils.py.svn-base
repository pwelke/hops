
# Some utilities for graph sampling scripts

import math
import networkx as nx
import experiments.globals

#def read_number_observations_exhaustive_approach_split_N_intervals(path_to_file,N_intervals):
#    '''
#    :param path_to_file: path to file consisting the number of observations of the exhaustive approach. The line should start with:
                         

def make_command_string(arguments):
    string=""
    for arg in arguments:
        string+=arg+" "
    return string

#check if pattern is invalid
def is_invalid(pattern):
    nr_targets=0
    nr_heads=0
    for nd in pattern.nodes():
        if 'head' in pattern.node[nd].keys():
            nr_heads+=1
        if pattern.node[nd]['target']==1:
            nr_targets+=1
    if nr_targets>=2:
        return False
    else:
        return True


def turn_graph_into_prolog_format(data_graph,output_path,constants,relation_predicates,properties_predicates):
    with open(output_path,'w') as file:
        for node in data_graph.nodes():
            if data_graph.node[node]['predicate']=='interaction':
                continue
            literal=None
            
            if data_graph.node[node]['predicate']=='constant':
              literal=data_graph.node[node]['predicate']+"("+data_graph.node[node]['name'].lower()+").\n"
    
            if data_graph.node[node]['predicate'] in relation_predicates:
                literal=data_graph.node[node]['predicate']+"("+data_graph.node[data_graph.neighbors(node)[0]]['name'].lower()+","+data_graph.node[data_graph.neighbors(node)[1]]['name'].lower()+").\n"
            
            if data_graph.node[node]['predicate'] in properties_predicates:
                literal=data_graph.node[node]['predicate']+"("+data_graph.node[data_graph.neighbors(node)[0]]['name'].lower()+","+data_graph.node[node]['value'].lower()+").\n"
            
            file.write(literal)
            
def turn_graph_into_prolog_format_dblp(data_graph,output_path,constants,relation_predicates,properties_predicates):
    with open(output_path,'w') as file:
        for node in data_graph.nodes():
            if data_graph.node[node]['predicate']=='interaction':
                continue
            literal=None
            
            if data_graph.node[node]['predicate']=='constant':
              literal="paper"+"(p_"+str(data_graph.node[node]['label'])+").\n"
             
    
            if data_graph.node[node]['predicate'] in relation_predicates:
                print "RELATION PREDICATE: ",data_graph.node[node]['predicate']
                print "NEIGHBOURS"
                node1=data_graph.node[data_graph.neighbors(node)[0]]
                print "NODE1",node1
                try:
                    node2=data_graph.node[data_graph.neighbors(node)[1]]
                except IndexError:
                    continue #PROBLEM HERE. ASK
                    
                node1_prefix=None
                node2_prefic=None
                if node1['predicate']=='constant':
                    node1_prefix="p_"
                if node2['predicate']=='constant':
                    node2_prefix="p_"
                if node1['predicate']=='dir':
                    node1_prefix="d_"
                if node2['predicate']=='dir':
                    node2_prefix="d_"
                if node1['predicate']=='references':
                    node1_prefix="r_"
                if node2['predicate']=='references':
                    node2_prefix="r_"
                
                print "NODE 2",node2
                literal=data_graph.node[node]['predicate']+"("+node1_prefix+str(data_graph.node[data_graph.neighbors(node)[0]]['label'])+","+node2_prefix+str(data_graph.node[data_graph.neighbors(node)[1]]['label'])+").\n"
            
            if data_graph.node[node]['predicate'] in properties_predicates:
                literal=data_graph.node[node]['predicate']+"(p_"+str(data_graph.node[data_graph.neighbors(node)[0]]['label'])+","+str(data_graph.node[node]['value'])+").\n"
            
            file.write(literal)
        
                


def kld(p, q):
    """
    Function that computes Kullback-Leibler divergence of two discrete probability distributions.
    The probability distributions 'p' and 'q' must be python lists.
    Log2 is used in this implementation, so the outcome is in bits. 
    """
    sum = 0
    #print p
    #print q
    for i in range(len(p)):
        if p[i]==0:
            sum+=0
        else:
            sum += p[i] * ( math.log(p[i],  2) - math.log(q[i],  2) )
    return sum

def kld_dict_old(p, q):
    """The same as 'kld()', but made to handle distributions given as python dictionaries."""
    p_list = []
    q_list=[]
    for k in p.keys():
        p_list.append(p[k])
        q_list.append(q[k])
    return kld(p_list,  q_list)


def kld_dict(p, q):
    """The same as 'kld()', but made to handle distributions given as python dictionaries."""
    p_list = []
    q_list=[]
    for k in p.keys():
        p_list.append(p[k])
        if k in q.keys():
            q_list.append(q[k])
        #else:
            #q_list.append(0.00000000001)
        #print p_list,q_list
    return kld(p_list,  q_list)


def hellinger(p, q):
    """
    Calculates the Hellinger distance (using Bhattacharyya coefficient) among discrete probability distributions 'p' and 'q', given as python lists.
    It is bounded to [0, 1], unlike the Bhattacharyya, which is unbounded.
    Often the Hellinger distance is wrongly reffered to as Bhattacharyya distance.
    """
    coef = 0
    for i in range(len(p)):
        coef = coef + math.sqrt(p[i] * q[i])
    argu = 1 - coef
    if argu <= 0:   # can happen to be 0, because of Python's rounding
        argu = 0.000000000000001
    return math.sqrt(argu)

def hellinger_dict(p,  q):
    """The same as 'hellinger()', but made to handle distributions given as python dictionaries"""
    p_list = []
    q_list=[]
    for k in p.keys():
        p_list.append(p[k])
        if k in q.keys():
            q_list.append(q[k])
##        else:
##            q_list.append(0.00000000001)
    return hellinger(p_list,  q_list)
    


def bhatta(p, q):
    """
    Calculates the Bhattacharyya distance among discrete probability distributions 'p' and 'q', given as python lists
    """
    coef = 0
    for i in range(len(p)):
        coef = coef + math.sqrt(p[i] * q[i])
    return -1 * math.log(coef)
    
def bhatta_dict(p,  q):
    """The same as 'bhatta()', but made to handle distributions given as python dictionaries"""
    p_list = []
    q_list=[]
    for k in p.keys():
        p_list.append(p[k])
        if k in q.keys():
            q_list.append(q[k])
##        else:
##            q_list.append(0.00000000001)
    return bhatta(p_list,  q_list)
    
    
def abs_d_diff(p, q):
    """
    Returns the absolute difference among discrete probability distributions 'p' and 'q', which are given as python dictionaries.
    A sum of absolute differences at each value.
    """
    diff = 0
    for k in p.keys():
        diff = diff + abs(p[k] - q[k])
    return diff


def cum_abs_d_diff(p_table,  q_table):
    """
    Returns a cumulative absolute difference among two discrete probability distribution tables - so, collections of distributions.
    Each table is represented as a dictionary
            - its keys are parent value tuples, e.g.: '('high', 'high')'
            - its values are distributions in form of python dictionaries, e.g.: '{'high': 0.4388059701492537, 'low': 0.34746268656716417, 'mid': 0.2137313432835821}'
    Absolute differences of all distributions are summed together and returned
    """
    err = 0
    for k in p_table.keys():
        ierr = abs_d_diff(p_table[k],  q_table[k])
        err = err + ierr
    return err


def avg_kld(p_table,  q_table):
    """
    Returns an average Kullback-Leibler divergence of two discrete probability distribution tables - that is. collections of distributions
    Each table is represented as a dictionary
            - its keys are parent value tuples, e.g.: '('high', 'high')'
            - its values are distributions in form of python dictionaries, e.g.: '{'high': 0.4388059701492537, 'low': 0.34746268656716417, 'mid': 0.2137313432835821}'
    """
    cum_kld = 0

    for k in p_table.keys():
        if k in q_table.keys():
          kld_i = kld_dict(p_table[k],  q_table[k])
        elif experiments.globals.default_key in q_table.keys():
          kld_i= kld_dict(p_table[k],  q_table[experiments.globals.default_key])
        elif 'empty' in q_table.keys():
          kld_i= kld_dict(p_table[k],  q_table['empty'])
        cum_kld = cum_kld + kld_i
    if experiments.globals.report=="furer":
        return float(cum_kld)/(len(p_table.keys()))
    else:
        return float(cum_kld)/(len(p_table.keys()))
  

def avg_hellinger(p_table,  q_table):
    """
    Returns an average Hellinger distance of two discrete probability distribution tables - that is. collections of distributions
    Each table is represented as a dictionary
            - its keys are parent value tuples, e.g.: '('high', 'high')'
            - its values are distributions in form of python dictionaries, e.g.: '{'high': 0.4388059701492537, 'low': 0.34746268656716417, 'mid': 0.2137313432835821}'
    """
    cum_hd = 0
    for k in p_table.keys():
        if k in q_table.keys():
          hd_i = hellinger_dict(p_table[k],  q_table[k])
        elif experiments.globals.default_key in q_table.keys():
          hd_i= hellinger_dict(p_table[k],  q_table[experiments.globals.default_key])
        elif 'empty' in q_table.keys():
          hd_i= hellinger_dict(p_table[k],  q_table['empty'])
            
        cum_hd = cum_hd + hd_i
    return float(cum_hd)/len(p_table.keys())


def generate_monitoring_marks(time_interval_in_seconds,max_time_in_seconds):
    counter=0
    marks=[]
    while counter+time_interval_in_seconds<=max_time_in_seconds:
        marks.append(counter+time_interval_in_seconds)
        counter=counter+time_interval_in_seconds
    return marks


def avg_bhatta(p_table,  q_table):
    """
    Returns an average Bhattacharyya distance of two discrete probability distribution tables - that is. collections of distributions
    Each table is represented as a dictionary
            - its keys are parent value tuples, e.g.: '('high', 'high')'
            - its values are distributions in form of python dictionaries, e.g.: '{'high': 0.4388059701492537, 'low': 0.34746268656716417, 'mid': 0.2137313432835821}'
    """
    cum_bd = 0
    for k in p_table.keys():
        if k in q_table.keys():
          bd_i = bhatta_dict(p_table[k],  q_table[k])
        elif experiments.globals.default_key in q_table.keys():
          bd_i= bhatta_dict(p_table[k],  q_table[experiments.globals.default_key])
        elif 'empty' in q_table.keys():
          bd_i= bhatta_dict(p_table[k],  q_table['empty'])
            
        cum_bd = cum_bd + bd_i
    return float(cum_bd)/len(p_table.keys())

if __name__ == '__main__':
    data_graph_path='/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/YEAST.gpickle'
    output_prolog_path='/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/YEAST_prolog.pl'
    data_graph=nx.read_gpickle(data_graph_path)
    turn_graph_into_prolog_format(data_graph, output_prolog_path,['constant'],['interaction'],['function','location','protein_class','enzyme','phenotype','complex'])
