
import os
import time
import re
import random
import math
import operator,sys
import copy
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import sched
import sampling_utils as su
import experiments.globals
import warnings


# global lists of fdicts; one for each quota reached
globalist_randomnode = []
globalist_furer = []
cqi = 0     #index of nlimitlist - the current quota to check for
globaltimes_randomnode = []     # first element is actual start time, others are timings for each quota reached
globaltimes_furer = []
temp_result=[]
nodes_observed=[]
output_bug=None

def random_from_distribution(dist_dict):
    """
    The function takes a distribution of the form {key1:p1, key2:p2, ...keyN:pN}
    where p1 + p2 + ... + pN =1
    and returns a random key, according to the probabilities given in the distribution.
    """
    # -- first a check if the probabilities sum to 1
    value_sum = 0
    for v in dist_dict.values():
        value_sum = value_sum + v
    if value_sum != 1:
        print "WARNING: distribution values not summing to 1. Random pick from distribution can give results 'None'."
    # -- just a warning is issued, as the process can usually continue without much damage, if mistakes are only slight.
    random_value = random.uniform(0,1)
    p_sum = 0
    for k in dist_dict.keys():
        if k == None: print "PROBLEM in dist_dict!"
        p_sum = p_sum + dist_dict[k]
        if random_value <= p_sum:
            return k

def select_least_expensive_combination(Plist,D,P):
    target_nodes=[]
    combs=[]
    comb_domain_best=float('inf')
    best_comb=None
    for i in range(len(Plist)):
        if P.node[Plist[i]]['target'] == True:
            target_nodes.append(Plist[i])
    print "Target nodes: ",target_nodes
    if len(target_nodes)==1:
        return target_nodes
    for i in xrange(2,len(target_nodes)+1):
        combs.append(list(itertools.combinations(target_nodes,i)))
    combs=[item for sublist in combs for item in sublist]
    print combs
    
    for comb in combs:
        comb_domain=1
        for i in range(len(comb)):
              if P.node[comb[i]]['target'] == True:
                part1 = P.node[comb[i]]['label']       # first part of the value tuple is the label
                predicate1 = P.node[comb[i]]['predicate']
                s = set()   # set of all possible values found in D for such a node
                for n in D.nodes():
                    if D.node[n]['predicate'] == predicate1:
                        value=D.node[n]['value']
                        s.add(value)
                comb_domain*=len(s)
        print "comb: ",comb," #combs: ",comb_domain
        if comb_domain<comb_domain_best:
            comb_domain_best=comb_domain
            best_comb=comb
    print "BEST COMBINATION: ",best_comb,"with domain size: ",comb_domain_best
    return best_comb
         

def complete_combinations(fdict, D,  P,  Plist):
    """completes the combinations in fdict, so that it contains also all the zeros in combinations that were not even found in the graph (needed for correct and fair smoothing)
    - value_tuples_list is a list of lists: each list contains all the possible value values of one target variable : ORDER MUST BE like in Plist, since this is how fdict's tuples are made.
    one value tuple is (label, value), so this is how they must be prepared for input. """
    import itertools
    count=0
    value_tuples_list = []
    choose_subset=False
    values_for_head=[]
    #if experiments.globals.experiment_name=="yeast":
    #   choose_subset=True
    #print "Choosing a subset of possible nodes?",choose_subset
    
    all_possible_target_tuples=None
    if choose_subset:
        least_expensive_combination=select_least_expensive_combination(Plist,D,P)
        with open(os.path.join(experiments.globals.output_path,"target_combination.info"),'w') as f:
            f.write(str(least_expensive_combination)); 
        for i in range(len(least_expensive_combination)):
            if P.node[least_expensive_combination[i]]['target'] == True:
                count+=1
                part1 = P.node[least_expensive_combination[i]]['label']       # first part of the value tuple is the label
                predicate1 = P.node[least_expensive_combination[i]]['predicate']
                s = set()   # set of all possible values found in D for such a node
                for n in D.nodes():
                    if D.node[n]['predicate'] == predicate1:
                        value=D.node[n]['value']
                        s.add(value)
                value_tuples_list.append(list(itertools.product([part1], list(s))))     # returns a list of tuples that are combinations of the label, and all possible value from the set
                print "For ",predicate1," comb: ",len(s)
        all_possible_target_tuples = list(itertools.product(*value_tuples_list)) 
        with open(os.path.join(experiments.globals.output_path,"nr_combinations.info"),'w') as f:
            f.write(str(all_possible_target_tuples));
        
    else:
        for i in range(len(Plist)):
            if P.node[Plist[i]]['target'] == True:
                count+=1
                part1 = P.node[Plist[i]]['label']       # first part of the value tuple is the label
                predicate1 = P.node[Plist[i]]['predicate']
                # then all possible values get collected from D
                s = set()   # set of all possible values found in D for such a node
                for n in D.nodes():
                    if D.node[n]['predicate'] == predicate1:
                        value=D.node[n]['value']
                        if i==0:
                           values_for_head.append(value)
                        s.add(value)
                value_tuples_list.append(list(itertools.product([part1], list(s))))     # returns a list of tuples that are combinations of the label, and all possible value from the set
    # here value_tuples_list should be a list of lists: each variable in a combination has a list of its value tuples
        all_possible_target_tuples = list(itertools.product(*value_tuples_list))       # we get a list of all possible target tuples (* just unpacks values_list into individual list, since this is what itertools expect)
    experiments.globals.nr_values_for_head=len(set(values_for_head))
    for tt in all_possible_target_tuples:
        if tt not in fdict:
          fdict[tt] = 0
    return len(all_possible_target_tuples)

def get_number_of_possible_value_combinations(head_predicate,predicates,map_of_values):
    nr_combinations=1
    if len(predicates)==1:
        return 1
    for k in predicates:
       # if(not k==head_predicate):
            nr_combinations*=len(map_of_values[k])
    return nr_combinations


def get_number_of_possible_value_combinations_excluding_head_predicate(head_predicate,predicates,map_of_values):
    nr_combinations=1
    if len(predicates)==1:
        return len(map_of_values[predicates[0]])
    for k in predicates:
        if (not k==head_predicate):
            nr_combinations*=len(map_of_values[k])
    return nr_combinations

def complete_combinations_1(fdict, D,  P,  Plist):
    """completes the combinations in fdict, so that it contains also all the zeros in combinations that were not even found in the graph (needed for correct and fair smoothing)
    - value_tuples_list is a list of lists: each list contains all the possible value values of one target variable : ORDER MUST BE like in Plist, since this is how fdict's tuples are made.
    one value tuple is (label, value), so this is how they must be prepared for input. """
    import itertools
    count=0
    value_tuples_list = []
    choose_subset=False
    values_for_head=[]
    target_predicates=[]
    head_predicate=None
    all_possible_target_tuples=None
    values_for_target_predicates={}
    counts_for_head_occurence={}
    
    for k in fdict.keys():
        head_predicate=k[0][0]
        break
    
    target=0
    for i in range(len(Plist)):
            if P.node[Plist[i]]['target'] == 1:
                target+=1
                count+=1
                part1 = P.node[Plist[i]]['label']       # first part of the value tuple is the label
                predicate1 = P.node[Plist[i]]['predicate']
                print "PRED: ",predicate1
                if target==1:
                    head_predicate=predicate1

                print "HEAD PREDICATE: ",head_predicate
                target_predicates.append(predicate1)
                # then all possible values get collected from D
                s = set()   # set of all possible values found in D for such a node
                for n in D.nodes():
                    if D.node[n]['predicate'] == predicate1:
                        value=D.node[n]['value']
                        if target==1:
                          values_for_head.append((predicate1,value))
                          values_for_head.append((predicate1,"false"))
                          head_predicate=predicate1
                        s.add(value)
                        s.add("false")
                values_for_target_predicates[predicate1]=s
                value_tuples_list.append(list(itertools.product([part1], list(s))))     # returns a list of tuples that are combinations of the label, and all possible value from the set
    # here value_tuples_list should be a list of lists: each variable in a combination has a list of its value tuples
    nr_possible_values_target= get_number_of_possible_value_combinations(head_predicate, target_predicates,values_for_target_predicates)
    nr_possible_values_target_no_head= get_number_of_possible_value_combinations_excluding_head_predicate(head_predicate, target_predicates,values_for_target_predicates)
    experiments.globals.nr_target_nodes_no_head=nr_possible_values_target_no_head
    print "Nr possible values target: ",nr_possible_values_target
    print "Nr possible values targets (no HEAD): ",nr_possible_values_target_no_head
    
    for value in values_for_target_predicates[head_predicate]:
        counts_for_head_occurence[(head_predicate,value)]=nr_possible_values_target
    #all_possible_target_tuples = list(itertools.product(*value_tuples_list))       # we get a list of all possible target tuples (* just unpacks values_list into individual list, since this is what itertools expect)
    #print len(all_possible_target_tuples)
    set_of_values_for_head=set(values_for_head)
    experiments.globals.nr_values_for_head=len(set_of_values_for_head)
    experiments.globals.all_possible_target_combinations=[]
    experiments.globals.valueTuples=set(set_of_values_for_head)
    counter_not_found_targets=0
    if len(fdict)==0 or len(target_predicates)==1 or nr_possible_values_target>len(fdict):
        default_key = []
        if(len(fdict.keys())>0):
           akey = fdict.keys()[0]
        else:
           akey=['dummy']
        for j in range(len(akey)):
            default_key.append(('default', 'default'))
        default_key = tuple(default_key)
        fdict[default_key]=[]
        fdict[default_key] = -1
        for tt in fdict.keys():
                 new_key=tt
                 if len(target_predicates):
                     new_key=tt[0]        
                 if new_key in counts_for_head_occurence.keys():
                   counts_for_head_occurence[(new_key[0],new_key[1])]=counts_for_head_occurence[(new_key[0],new_key[1])]-1
        experiments.globals.count_of_combination_values_for_head=counts_for_head_occurence
    
    return nr_possible_values_target
    



def make_fd(fd):
    """ takes crude frequency dictionary as input and creates frequency distributions dictionary as output """
    f_diki = {}
    for k in fd.keys():
        f_diki[(k[0], k[1])] = {'low':0, 'mid':0, 'high':0}         # initializing to 0 is better than to None, since some can stay 0. In those None is a problem in make_pd.
    # the structure is prepared now, what follows is filling it in
    for k in fd.keys():
        f_diki[(k[0], k[1])] [k[2]] = fd[k]
    return f_diki
    
def make_pd(fd):
    """takes a frequency distribution and returns its normalized version - a probability distribution"""
    pd = copy.deepcopy(fd)
    for k in pd.keys():
        dist_sum = 0
        for ik in pd[k]:
            dist_sum = dist_sum + pd[k][ik]
        if dist_sum == 0:       # can happen if sample is too smal to detect any object for this distribution, so frequency == 0 for all values
            for ik in pd[k]:
                pd[k][ik] = 1.0 / len(pd[k])
        else:
            for ik in pd[k]:
                pd[k][ik] = pd[k][ik] / float(dist_sum)
    return pd


def smooth(fd, fdtemplate):
    """Smoothes the fdict fd according to fdtemplate. All values in fd get an increase of 1. 
    The keys that do not exist in fd (but do in fdtemplate) get added to fd and get a value of 1.
    This is Laplace smoothing. The same as if all frequencies would be initialized to 1 at the start.
    WARNING: fd is changed by this function. If you also need the original make a deepcopy of it before the call."""
    for k in fdtemplate:
        if k in fd:
            fd[k] = fd[k] + 1
        else:
            fd[k] = 1

def make_fd_general(fdict):
    fd = {}
    for k in fdict.keys():
        if k[1:] not in fd.keys():
            fd[k[1:]] = [[k[0],  fdict[k] ]] # key is now the group of all target-value tuples but first, list of lists containting first tuple and its frequency is the value now
        else:   # we have something in place already for this key - just add to the list
            fd[k[1:]].append([k[0],  fdict[k]])
    return fd

def make_fd_general_my_version(fdict):
    fd = {}
    for k in fdict.keys():
        if(fdict[k]==-1):
                 print "default"
                 headValuesAdded=[]
                 key=k[1:]
                 if key!=():
                   fd[key]=[]
                 if not key in fd.keys():
                     fd[key]=[]
                 counter=0
                 for headValue in experiments.globals.count_of_combination_values_for_head.keys():
                    if key==():
                        if experiments.globals.count_of_combination_values_for_head[headValue]==0:
                            continue 
                    fd[key].append([headValue,experiments.globals.count_of_combination_values_for_head[headValue]])
        else:    
                if k[1:]==() and k[1:] in fd.keys():
                    fd[k[1:]].append([k[0],  fdict[k]+1 ])
                    continue
                if not k[1:] in fd.keys():  
                    fd[k[1:]] = [[k[0],  fdict[k]+1]]
                else:
                    fd[k[1:]].append([k[0],  fdict[k]+1 ])
    #Add other head values
    for k in fd.keys():   
        headValuesAdded=[]
        for i in fd[k]:
            headValuesAdded.append(i[0])
        for value_tuple in experiments.globals.valueTuples:
                if not value_in_tuple_list(value_tuple[1],headValuesAdded):
                  headValuesAdded.append(value_tuple)
                  if experiments.globals.report=="furer":
                      fd[k].append([value_tuple,  1/float(experiments.globals.nr_iterations)])
                  else:    
                      fd[k].append([value_tuple,  1])
    #print "NEW"
    #for k in fd.keys():
    #    for el in fd[k]:
    #        print el,el[1]
    return fd

def make_fd_general_my_version_exhaustive(fdict):
    fd = {}
    #for k in fdict.keys():
    #    print k,fdict[k]
    for k in fdict.keys():
        if(fdict[k]==-1):
                 headValuesAdded=[]
                 key=k[1:]
                 if key!=():
                   fd[key]=[]
                 else:
                    continue
                 counter=0
                 
                 for headValue in experiments.globals.count_of_combination_values_for_head.keys():
                    if key==():
                        if experiments.globals.count_of_combination_values_for_head[headValue]==0:
                            continue 
                    #if experiments.globals.current_time_snapshot==15:
                    #    print "Appending: ",[headValue,experiments.globals.count_of_combination_values_for_head[headValue]]
                    fd[key].append([headValue,experiments.globals.count_of_combination_values_for_head[headValue]])
        else:    
                if k[1:]==() and k[1:] in fd.keys():
                    fd[k[1:]].append([k[0],  fdict[k]+1])
                    continue
                if not k[1:] in fd.keys():  
                    fd[k[1:]] = [[k[0],  fdict[k]+1]]
                else:
                    fd[k[1:]].append([k[0],  fdict[k]+1])
    #if experiments.globals.current_time_snapshot==15:
    #print "New dict:"
    #for k in fd.keys():
    #  print k,fd[k]
    
    #Add other head values
    for k in fd.keys():   
        headValuesAdded=[]
        for i in fd[k]:
            headValuesAdded.append(i[0])
        for value_tuple in experiments.globals.valueTuples:
                if not value_in_tuple_list(value_tuple[1],headValuesAdded):
                  headValuesAdded.append(value_tuple)
                  fd[k].append([value_tuple,  experiments.globals.nr_iterations])
    #print "EXHAUSTIVE"
    #for k in fd.keys():
    #    print k,fd[k]
    return fd

def make_fd_general_my_version_exhaustive_1(fdict):
    fd = {}
    for k in fdict.keys():
        if(fdict[k]==-1):
                 headValuesAdded=[]
                 key=k[1:]
                 if key!=():
                   fd[key]=[]
                 else:
                    continue
                 counter=0
                 
                 for headValue in experiments.globals.count_of_combination_values_for_head.keys():
                    if key==():
                        if experiments.globals.count_of_combination_values_for_head[headValue]==0:
                            continue 
                    fd[key].append([headValue,experiments.globals.count_of_combination_values_for_head[headValue]])
        else:    
                if k[1:]==() and k[1:] in fd.keys():
                    fd[k[1:]].append([k[0],  fdict[k]])
                    continue
                if not k[1:] in fd.keys():  
                    fd[k[1:]] = [[k[0],  fdict[k]]]
                else:
                    fd[k[1:]].append([k[0],  fdict[k]]) 
    #Add other head values
    for k in fd.keys():   
        headValuesAdded=[]
        for i in fd[k]:
            headValuesAdded.append(i[0])
        for value_tuple in experiments.globals.valueTuples:
                if not value_in_tuple_list(value_tuple[1],headValuesAdded):
                  headValuesAdded.append(value_tuple)
                  fd[k].append([value_tuple,  0])
    return fd

def value_in_tuple_list(value,head_values):
    res=False
    for h in head_values:
        if h[1]==value:
            return True
    return res 


# def make_fd_general(fdict):
#     fd = {}
#     for k in fdict.keys():
#         key=None
#         if(len(k)==2): #Irma: added this. there were some problems slicing this when having only two elements
#             key=k[-1]
#         else:
#             key=k[1:]
#         if key not in fd.keys():
#             fd[key] = [[k[0],  fdict[k] ]] # key is now the group of all target-value tuples but first, list of lists containting first tuple and its frequency is the value now
#         else:   # we have something in place already for this key - just add to the list
#             fd[key].append([k[0],  fdict[k]])
#     return fd

def make_pd_general(fdict):
    fd = make_fd_general(fdict)
    # now we normalize for each key - its list with values
    for k in fd.keys():
        ksum = 0
        for el in fd[k]:    # the value of fd dict. - the list like : [[(u'satisfaction(m)', u'low'), 66], [(u'satisfaction(m)', u'mid'), 26], [(u'satisfaction(m)', u'high'), 66]]
            ksum = ksum + el[1]
        # now the normalization change
        for el in fd[k]:
            el[1] = el[1] / float(ksum)
    return fd


def make_pd_general_kickout(fdict,  trash_factor=0.01):
    """this one kicks out all rows/combinations that do not gather in frequencies more than 1% of all embeddings
    trash_factor gives the threshold for removal: default is 0.01, which means threshold of 1%"""
    num_embeddings = 0
    for k in fdict.keys():
        num_embeddings = num_embeddings + fdict[k] - 1  # I remove +1 added by Laplace smoothing BEWARE: previous Laplace smoothing assumed
    #print "Number of embeddings: %d" % sum    
    fd = make_fd_general(fdict)
    trash = []
    # now we normalize for each key - its list with values
    for k in fd.keys():     # so, for each combination/row:
        ksum = 0
        trashsum = 0
        for el in fd[k]:    # the value of fd dict. - the list like : [[(u'satisfaction(m)', u'low'), 66], [(u'satisfaction(m)', u'mid'), 26], [(u'satisfaction(m)', u'high'), 66]]
            ksum = ksum + el[1]
            trashsum = trashsum + el[1] - 1     # again, for trash threshold, Laplace is removed
        if trashsum < trash_factor * num_embeddings:    # if smaller than 1% of embeddings
            trash.append(k)
        # now the normalization change
        for el in fd[k]:
            el[1] = el[1] / float(ksum)
    for tk in trash:    # now we remove all trashy keys - this cannot be done while iterating over dict, so it is separate
        del fd[tk]
    return fd



def make_pd_general_kickout_default(fdict,  trash_factor=0.01):
    """this one gathers in a default combination all rows/combinations that do not gather in frequencies more than 1% of all embeddings
    trash_factor gives the threshold for removal: default is 0.01, which means threshold of 1%"""
    num_embeddings = 0
    for k in fdict.keys():        
        num_embeddings+= fdict[k] - 1  # I remove +1 added by Laplace smoothing BEWARE: previous Laplace smoothing assumed
    print "Number of embeddings: %d" % num_embeddings    
    fd = make_fd_general(fdict)

    trash = []
    # creation of the default key of the same size as other keys, but all values 'default'
    default_key = []
    akey = fd.keys()[0]
    for j in range(len(akey)):
        default_key.append(('default', 'default'))
    default_key = tuple(default_key)
    # now a separate walk over all keys is needed, before they get transformed into probabilities
    for k in fd.keys():     # so, for each combination/row:
        trashsum = 0
        for el in fd[k]:    # the value of fd dict. - the list like : [[(u'satisfaction(m)', u'low'), 66], [(u'satisfaction(m)', u'mid'), 26], [(u'satisfaction(m)', u'high'), 66]]
            trashsum = trashsum + el[1] - 1     # again, for trash threshold, Laplace is removed
        if trashsum < trash_factor * num_embeddings:    # if smaller than 1% of embeddings
            trash.append(k)
    if len(trash) >0:
        fd[default_key] = []
    default_element_tuples = []
    for tk in trash:
        for element in fd[tk]:        # element is like [('location', 'somewhere'), 1]  or  [('location', 'elsewhere'), 3] 
            if element[0] not in default_element_tuples:
                default_element_tuples.append(element[0])   # so that I know which elements are already in default distribution
                fd[default_key].append(element)
            else:
                for item in fd[default_key]:    # item has the same structure as element above
                    if item[0]==element[0]:
                        item[1] = item[1] + element[1]      # we add the frequency
    for tk in trash:    # now we remove all trashy keys - this cannot be done while iterating over dict, so it is separate
        del fd[tk]  

  
    # now we normalize the remaining keys for each key - its list with values
    for k in fd.keys():     # so, for each combination/row:
        print k

        ksum = 0
        for el in fd[k]:    # the value of fd dict. - the list like : [[(u'satisfaction(m)', u'low'), 66], [(u'satisfaction(m)', u'mid'), 26], [(u'satisfaction(m)', u'high'), 66]]
            ksum = ksum + el[1]
        # now the normalization change
        for el in fd[k]:
            el[1] = el[1] / float(ksum)
    print "SIZE OF DICT MARTIN: ",len(fd)
    with open('pdfAfterGeneralKickout_MARTIN.csv','w') as f:
        for k in fd.keys():
          f.write(str(k)+';'+str(fd[k])+'\n') 
    return [fd,  trash,  default_key]




def make_pd_general_kickout_default_my_version(fdict):
    """this one gathers in a default combination all rows/combinations that do not gather in frequencies more than 1% of all embeddings
    trash_factor gives the threshold for removal: default is 0.01, which means threshold of 1%"""
    num_embeddings = 0
    for k in fdict.keys():
        num_embeddings = num_embeddings + fdict[k]  # I remove +1 added by Laplace smoothing BEWARE: previous Laplace smoothing assumed
    print "Nr embeddingS:",num_embeddings
    nr_non_observed=experiments.globals.nr_non_observed_combinations
    print "Making general version dictionary"
    if(experiments.globals.report=="furer"):
      fd = make_fd_general_my_version_exhaustive_1(fdict)
    else:
      fd = make_fd_general_my_version_exhaustive_1(fdict)
    #for k in fd.keys():
    #    if k==((u'location', u'Location_id_705003'), (u'function', u'Func_id_40')):
    #        print "Exhaustive"
    #        print k,fd[k]
    #with open('fdictGENERAL_MINE.csv','w') as f:
    #    for k in fd.keys():
    #        print k,fd[k]
    #        f.write(str(k)+';')
    #        for el in fd[k]:
    #           f.write(str(el)+';')
    #        f.write('\n')
    print "Finished with general version"
    print "SizE: ",len(fd)
    counter=0
    all_comb=0
    trash = []
    # creation of the default key of the same size as other keys, but all values 'default'
    default_key = []
    akey = fd.keys()[0]
    for j in range(len(akey)):
        default_key.append(('default', 'default'))
    default_key = tuple(default_key)
#     # now a separate walk over all keys is needed, before they get transformed into probabilities
#     for k in fd.keys():     # so, for each combination/row:
#         trashsum = 0
#         for el in fd[k]:    # the value of fd dict. - the list like : [[(u'satisfaction(m)', u'low'), 66], [(u'satisfaction(m)', u'mid'), 26], [(u'satisfaction(m)', u'high'), 66]]
#             trashsum = trashsum + el[1] - 1     # again, for trash threshold, Laplace is removed
#         if trashsum < 0.01 * num_embeddings:    # if smaller than 1% of embeddings
#             if len(fd)==1 and () in fd.keys():
#                 continue
#             else:
#                trash.append(k)
#     print "Size of trash: ",len(trash)
#     for tk in trash:    # now we remove all trashy keys - this cannot be done while iterating over dict, so it is separate
#         del fd[tk] 
    for k in fd.keys():     # so, for each combination/row:
        ksum = 0
        for el in fd[k]:    # the value of fd dict. - the list like : [[(u'satisfaction(m)', u'low'), 66], [(u'satisfaction(m)', u'mid'), 26], [(u'satisfaction(m)', u'high'), 66]]
            ksum = ksum + el[1]
        for el in fd[k]:
            if ksum==0:
                el[1]=0
            else:
                el[1] = el[1] / float(ksum)
    return [fd,trash,default_key]


def make_pd_general_kickout_default_old(fdict,  trash_factor=0.01):
    """this one gathers in a default combination all rows/combinations that do not gather in frequencies more than 1% of all embeddings
    trash_factor gives the threshold for removal: default is 0.01, which means threshold of 1%"""
    num_embeddings = 0
    for k in fdict.keys():
        num_embeddings = num_embeddings + fdict[k] - 1  # I remove +1 added by Laplace smoothing BEWARE: previous Laplace smoothing assumed
    fd = make_fd_general(fdict)
   # with open('general_Martin.csv','w') as f:
   #     for k in fd.keys():
   #         print k,fd[k]
   #         f.write(str(k)+";")
   #         for e in k:
   #             f.write(str(e)+";")
    #        f.write("\n")    
    trash = []
    # creation of the default key of the same size as other keys, but all values 'default'
    default_key = []
    akey = fd.keys()[0]
    for j in range(len(akey)):
        default_key.append(('default', 'default'))
    default_key = tuple(default_key)
    # now a separate walk over all keys is needed, before they get transformed into probabilities
    for k in fd.keys():     # so, for each combination/row:
        trashsum = 0
        for el in fd[k]:    # the value of fd dict. - the list like : [[(u'satisfaction(m)', u'low'), 66], [(u'satisfaction(m)', u'mid'), 26], [(u'satisfaction(m)', u'high'), 66]]
            trashsum = trashsum + el[1] - 1     # again, for trash threshold, Laplace is removed
        if trashsum < trash_factor * num_embeddings:    # if smaller than 1% of embeddings
            trash.append(k)
    if len(trash) >0:
        fd[default_key] = []
    default_element_tuples = []
    for tk in trash:
        for element in fd[tk]:        # element is like [('location', 'somewhere'), 1]  or  [('location', 'elsewhere'), 3] 
            if element[0] not in default_element_tuples:
                default_element_tuples.append(element[0])   # so that I know which elements are already in default distribution
                fd[default_key].append(element)
            else:
                for item in fd[default_key]:    # item has the same structure as element above
                    if item[0]==element[0]:
                        item[1] = item[1] + element[1]      # we add the frequency
    for tk in trash:    # now we remove all trashy keys - this cannot be done while iterating over dict, so it is separate
        del fd[tk]    
    # now we normalize the remaining keys for each key - its list with values
    counter=0
    for k in fd.keys():     # so, for each combination/row:
        counter+=1
        ksum = 0 
        for el in fd[k]:    # the value of fd dict. - the list like : [[(u'satisfaction(m)', u'low'), 66], [(u'satisfaction(m)', u'mid'), 26], [(u'satisfaction(m)', u'high'), 66]]
            ksum = ksum + el[1]
        # now the normalization change
        for el in fd[k]:
            el[1] = el[1] / float(ksum)
    return [fd,  trash,  default_key]


def make_pd_general_kickout_default_limited(fdict,  trash,  default_key):
    """to handle also sampling fdicts according to what was defaulted in the exhaustive"""
    fd = make_fd_general(fdict)
    if len(trash)>0:
        fd[default_key] = []
    default_element_tuples = []
    
    #print "TRASH: ",len(trash)
    for tk in trash:
        if not(tk in fd.keys()):
            continue
        for element in fd[tk]:        # element is like [('location', 'somewhere'), 1]  or  [('location', 'elsewhere'), 3] 
            if element[0] not in default_element_tuples:
                default_element_tuples.append(element[0])   # so that I know which elements are already in default distribution
                fd[default_key].append(element)
            else:
                for item in fd[default_key]:    # item has the same structure as element above
                    if item[0]==element[0]:
                        item[1] = item[1] + element[1]      # we add the frequency
    
    for tk in trash:    # now we remove all trashy keys - this cannot be done while iterating over dict, so it is separate
        del fd[tk]    
    # now we normalize the remaining keys for each key - its list with values
    counter=0
    for k in fd.keys():     # so, for each combination/row:
        ksum = 0
        for el in fd[k]:    # the value of fd dict. - the list like : [[(u'satisfaction(m)', u'low'), 66], [(u'satisfaction(m)', u'mid'), 26], [(u'satisfaction(m)', u'high'), 66]]
            ksum = ksum + el[1]
        # now the normalization change
        for el in fd[k]:
            el[1] = el[1] / float(ksum)
    return [fd,  trash,  default_key]

def make_pd_general_kickout_default_limited_my_version(fdict):
    """to handle also sampling fdicts according to what was defaulted in the exhaustive"""
    if experiments.globals.report=="furer":
       fd = make_fd_general_my_version(fdict)
    else:
       fd = make_fd_general_my_version(fdict)

#     with open('generalDict.csv','w') as f:
#                 for k in fd.keys():
#                    f.write(str(k)+";")
#                    for e in fd[k]:
#                        f.write(str(e)+";")
#                    f.write("\n")
    default_element_tuples = []
    # now we normalize the remaining keys for each key - its list with values
    counter=0
    ksum_unconstrained=0
    for k in fd.keys():     # so, for each combination/row:   
        ksum = 0
        for el in fd[k]:    # the value of fd dict. - the list like : [[(u'satisfaction(m)', u'low'), 66], [(u'satisfaction(m)', u'mid'), 26], [(u'satisfaction(m)', u'high'), 66]]
            if experiments.globals.report=="furer":
              ksum_unconstrained+=el[1]
              if not el[1]==1:
                    ksum+=el[1]
                    #el[1]*=experiments.globals.nr_iterations
                    #ksum+=el[1]
                    counter+=1
            else:
              #print "NORMALIZED!"
              ksum = ksum + el[1]
        # now the normalization change
        if counter==1:
            ksum+=1
        for el in fd[k]:    
            #print el[1],ksum,el[1]/ksum
            if float(ksum)==0:
                ksum=len(fd[k])
                el[1]=el[1] / float(ksum)
            else:
                el[1] = el[1] / float(ksum)
    return fd


def make_pd_general_kickout_default_limited_old(fdict,  trash,  default_key):
    """to handle also sampling fdicts according to what was defaulted in the exhaustive"""
    fd = make_fd_general(fdict)
    if len(trash)>0:
        fd[default_key] = []
    default_element_tuples = []
    for tk in trash:
        if not(tk in fd.keys()):
            continue
        for element in fd[tk]:        # element is like [('location', 'somewhere'), 1]  or  [('location', 'elsewhere'), 3] 
            if element[0] not in default_element_tuples:
                default_element_tuples.append(element[0])   # so that I know which elements are already in default distribution
                fd[default_key].append(element)
            else:
                for item in fd[default_key]:    # item has the same structure as element above
                    if item[0]==element[0]:
                        item[1] = item[1] + element[1]      # we add the frequency
    for tk in trash:    # now we remove all trashy keys - this cannot be done while iterating over dict, so it is separate
        del fd[tk]    
    # now we normalize the remaining keys for each key - its list with values
    for k in fd.keys():     # so, for each combination/row:
        ksum = 0 
        for el in fd[k]:    # the value of fd dict. - the list like : [[(u'satisfaction(m)', u'low'), 66], [(u'satisfaction(m)', u'mid'), 26], [(u'satisfaction(m)', u'high'), 66]]
            ksum = ksum + el[1]
        for el in fd[k]:
            el[1] = el[1] / float(ksum)
    return [fd,  trash,  default_key]
    
    
def transform_to_ptable(pd_general):
    """ Transformation into format, which is accepted in the "sampling_utils.py" for calculation of distribution distance measures. """
    p_table_pde = {}
    for k in pd_general:
        values=None
        if len(k)==0:
            values=pd_general[k]
            
        else:
            values=k
        interlist = []
        valuedict = {}
        for i in range(len(values)):
            interlist.append(values[i][1])
            intertuple = tuple(interlist)
        # intertuple is current key for p_table now
        value = pd_general[k]
        for i in range(len(value)):
            valuedict[value[i][0][1]] = value[i][1]
        if len(k)==0:
            intertuple='empty'
        if 'default' in intertuple:
           experiments.globals.default_key=intertuple
        p_table_pde[intertuple] = valuedict
    return p_table_pde
    
def make_new_dict(pd_general):
     new_dict={}
     for k in pd_general.keys():
        new_dict[(('default', 'default'),)]=pd_general[k]
     return new_dict

def give_me_friends_graph(number_of_men,  number_of_women,  num_friends_list):
    G=nx.MultiGraph()       # do we need MultiGraph - to allow for multiple edges among two nodes ?
    ##male_names_list = ["john",  "mike",  "bob",  "peter",  "jack",  "bill",  "jeremy",  "abraham",  "luke",  "mick",  "michael",  "leroy"]
    male_names_list = ['m'+str(i) for i in range(number_of_men)]
    ##female_names_list = ["wanda",  "linda",  "sarah",  "jessica",  "ann",  "mary",  "beth",  "lindsay",  "vanessa",  "serena",  "venus",  "lily",  "monica"]
    female_names_list = ['f'+str(i) for i in range(number_of_women)]
    # first we create all persons:
    idcounter = 1
    for p in (male_names_list + female_names_list):
        if p in male_names_list:
            person_string = "man("+p+")"
            G.add_node(person_string,  id=idcounter,  predicate='man')
        else:
            person_string = "woman("+p+")"
            G.add_node(person_string,  id=idcounter,  predicate='woman')
        idcounter = idcounter + 1
        random_value = random.uniform(0,1)
        if random_value > 0.1:      # 10% of people are unemployed, have no salary
            salary_string = "salary("+p+")"
            G.add_node(salary_string,  id=idcounter,  predicate='salary')
            idcounter = idcounter + 1
            G.node[salary_string]['value']=random_from_distribution({'low':0.40,  'mid':0.20,  'high':0.40})
            G.add_edge(person_string,  salary_string)
            satisfaction_string = "satisfaction("+p+")"
            satisfaction_value = random_from_distribution({'low':0.40,  'mid':0.20,  'high':0.40})
            G.add_node(satisfaction_string,  id=idcounter,  value=satisfaction_value,  predicate='satisfaction')
            idcounter = idcounter + 1
            G.add_edge(person_string,  satisfaction_string)
    # second step is to get some of them married
    for p in male_names_list:
        if random.uniform(0,1) > 0.2:      # 80% of people are married
            person_string = "man("+p+")"
            for w in female_names_list:
                woman_string = "woman("+w+")"
                if ('married' in G.node[woman_string].keys()) and (G.node[woman_string]['married']=='yes'):
                    pass
                else:
                    married_string = 'married('+p+','+w+')'
                    G.add_node(married_string,  id=idcounter,  predicate='married')
                    G.add_edge(married_string,  person_string)
                    G.add_edge(married_string,  woman_string)
                    G.node[woman_string]['married']='yes'
                    idcounter = idcounter + 1
                    break
    # now we also add some friendships
    # a bit more care has to be taken here not to duplicate friendship nodes
    friends_list = []       # this list will contain tuples of friends
    for p in (male_names_list + female_names_list):
        number_of_friends = random.choice(num_friends_list)    # every person has 1,2 or 3 friends or [10, 20, 30] or...
        if p in male_names_list:
            person_string = "man("+p+")"
        else:
            person_string = "woman("+p+")"
        for i in range(number_of_friends):
            friend = random.choice(male_names_list + female_names_list)
            if (friend!=p) and ((friend, p) not in friends_list) and ((p,  friend) not in friends_list):
                if friend in male_names_list:
                    friend_string = "man("+friend+")"
                else:
                    friend_string = "woman("+friend+")"
                friends_list.append((p,  friend))
                friends_string = 'friends(' + p + ','+friend+')'
                G.add_node(friends_string,  id = idcounter,  predicate='friends')
                idcounter = idcounter + 1
                G.add_edge(friends_string,  person_string)
                G.add_edge(friends_string,  friend_string)
    return G


def give_me_friends_graph2(number_of_men,  number_of_women,  num_friends_list):
    """similar to original, but no string labels, only IDs."""
    G=nx.MultiGraph()       # do we need MultiGraph - to allow for multiple edges among two nodes ?
    ##male_names_list = ["john",  "mike",  "bob",  "peter",  "jack",  "bill",  "jeremy",  "abraham",  "luke",  "mick",  "michael",  "leroy"]
    male_names_list = ['m'+str(i) for i in range(number_of_men)]
    ##female_names_list = ["wanda",  "linda",  "sarah",  "jessica",  "ann",  "mary",  "beth",  "lindsay",  "vanessa",  "serena",  "venus",  "lily",  "monica"]
    female_names_list = ['f'+str(i) for i in range(number_of_women)]
    # first we create all persons:
    idcounter = 1
    male_ids = []
    female_ids = []
    for p in (male_names_list + female_names_list):
        if p in male_names_list:
            person_id = idcounter
            G.add_node(person_id,  id=idcounter,  predicate='man')
            male_ids.append(person_id)
        else:
            person_id = idcounter
            G.add_node(person_id,  id=idcounter,  predicate='woman')
            female_ids.append(person_id)
        idcounter = idcounter + 1
        random_value = random.uniform(0,1)
        if random_value > 0.1:      # 10% of people are unemployed, have no salary
            salary_id = idcounter
            G.add_node(salary_id,  id=idcounter,  predicate='salary')
            idcounter = idcounter + 1
            G.node[salary_id]['value']=random_from_distribution({'low':0.40,  'mid':0.20,  'high':0.40})
            G.add_edge(person_id,  salary_id)
            satisfaction_id = idcounter
            satisfaction_value = random_from_distribution({'low':0.40,  'mid':0.20,  'high':0.40})
            G.add_node(satisfaction_id,  id=idcounter,  value=satisfaction_value,  predicate='satisfaction')
            idcounter = idcounter + 1
            G.add_edge(person_id,  satisfaction_id)
    # second step is to get some of them married
    for mid in male_ids:
        if random.uniform(0,1) > 0.2:      # 80% of people are married
            for fid in female_ids:
                if ('married' in G.node[fid].keys()) and (G.node[fid]['married']=='yes'):
                    pass
                else:
                    married_id = idcounter
                    G.add_node(married_id,  id=idcounter,  predicate='married')
                    G.add_edge(married_id,  mid)
                    G.add_edge(married_id,  fid)
                    G.node[fid]['married']='yes'
                    idcounter = idcounter + 1
                    break
    # now we also add some friendships
    # a bit more care has to be taken here not to duplicate friendship nodes
    friends_list = []       # this list will contain tuples of friends
    for pid in (male_ids + female_ids):
        number_of_friends = random.choice(num_friends_list)    # every person has 1,2 or 3 friends or [10, 20, 30] or...
##        if pid in male_ids:
##            person_id = "man"
##        else:
##            person_string = "woman("+p+")"
        for i in range(number_of_friends):
            friend_id = random.choice(male_ids + female_ids)
            if (friend_id!=pid) and ((friend_id, pid) not in friends_list) and ((pid,  friend_id) not in friends_list):
##                if friend in male_names_list:
##                    friend_string = "man("+friend+")"
##                else:
##                    friend_string = "woman("+friend+")"
                friends_list.append((pid,  friend_id))
                friends_ID = idcounter
                G.add_node(friends_ID,  id = idcounter,  predicate='friends')
                idcounter = idcounter + 1
                G.add_edge(friends_ID,  pid)
                G.add_edge(friends_ID,  friend_id)
    return G



def give_me_friends_graph2_NUM(number_of_men,  number_of_women,  num_friends_list):
    """similar to original, but no string labels, only IDs. And all predicates are integers."""
    G=nx.MultiGraph()       # do we need MultiGraph - to allow for multiple edges among two nodes ?
    ##male_names_list = ["john",  "mike",  "bob",  "peter",  "jack",  "bill",  "jeremy",  "abraham",  "luke",  "mick",  "michael",  "leroy"]
    male_names_list = ['m'+str(i) for i in range(number_of_men)]
    ##female_names_list = ["wanda",  "linda",  "sarah",  "jessica",  "ann",  "mary",  "beth",  "lindsay",  "vanessa",  "serena",  "venus",  "lily",  "monica"]
    female_names_list = ['f'+str(i) for i in range(number_of_women)]
    # first we create all persons:
    idcounter = 1
    male_ids = []
    female_ids = []
    for p in (male_names_list + female_names_list):
        if p in male_names_list:
            person_id = idcounter
            G.add_node(person_id,  id=idcounter,  predicate=3)
            male_ids.append(person_id)
        else:
            person_id = idcounter
            G.add_node(person_id,  id=idcounter,  predicate=5)
            female_ids.append(person_id)
        idcounter = idcounter + 1
        random_value = random.uniform(0,1)
        if random_value > 0.1:      # 10% of people are unemployed, have no salary
            salary_id = idcounter
            G.add_node(salary_id,  id=idcounter,  predicate=2)
            idcounter = idcounter + 1
            G.node[salary_id]['value']=random_from_distribution({'low':0.40,  'mid':0.20,  'high':0.40})
            G.add_edge(person_id,  salary_id)
            satisfaction_id = idcounter
            satisfaction_value = random_from_distribution({'low':0.40,  'mid':0.20,  'high':0.40})
            G.add_node(satisfaction_id,  id=idcounter,  value=satisfaction_value,  predicate=1)
            idcounter = idcounter + 1
            G.add_edge(person_id,  satisfaction_id)
    # second step is to get some of them married
    for mid in male_ids:
        if random.uniform(0,1) > 0.2:      # 80% of people are married
            for fid in female_ids:
                if ('married' in G.node[fid].keys()) and (G.node[fid]['married']=='yes'):
                    pass
                else:
                    married_id = idcounter
                    G.add_node(married_id,  id=idcounter,  predicate=4)
                    G.add_edge(married_id,  mid)
                    G.add_edge(married_id,  fid)
                    G.node[fid]['married']='yes'
                    idcounter = idcounter + 1
                    break
    # now we also add some friendships
    # a bit more care has to be taken here not to duplicate friendship nodes
    friends_list = []       # this list will contain tuples of friends
    for pid in (male_ids + female_ids):
        number_of_friends = random.choice(num_friends_list)    # every person has 1,2 or 3 friends or [10, 20, 30] or...
##        if pid in male_ids:
##            person_id = "man"
##        else:
##            person_string = "woman("+p+")"
        for i in range(number_of_friends):
            friend_id = random.choice(male_ids + female_ids)
            if (friend_id!=pid) and ((friend_id, pid) not in friends_list) and ((pid,  friend_id) not in friends_list):
##                if friend in male_names_list:
##                    friend_string = "man("+friend+")"
##                else:
##                    friend_string = "woman("+friend+")"
                friends_list.append((pid,  friend_id))
                friends_ID = idcounter
                G.add_node(friends_ID,  id = idcounter,  predicate=6)
                idcounter = idcounter + 1
                G.add_edge(friends_ID,  pid)
                G.add_edge(friends_ID,  friend_id)
    return G


def subsampling_random(D, sample_size):
    """Subsampling procedure: out of a full dataset graph D takes RANDOMLY a sample of nodes and returns a subsample graph
    sample_size tells how many nodes are taken from D
    """
    nodes_list = []
    if sample_size <= len(D.nodes()):
        while len(nodes_list) < sample_size:
            n = random.choice(D.nodes())
            if n not in nodes_list:
                nodes_list.append(n)
        # now lets make a subgraph out of those nodes, containing edges from D
        S= nx.Graph(D.subgraph(nodes_list))
        # NOTE: this is a relatively safe call, which makes a separate copy of attributes(instead just referencing to D), but takes some more space
        # even a deepcopy could be made, if some attributes are containers.
        #A reference version, or even an in-place version  could be made, if space is a problem. (see NetworkX documentation on this)
    else:
        S = None    # in case sample size is larger than dataset graph size, the sampling is not possible and the loop would not finish.
    return S
    

def subsampling_walker(D, sample_size):
    """Subsampling procedure: out of a full dataset graph D takes a sample of nodes by a RANDOM WALK and returns a subsample graph
    sample_size tells how many nodes are taken from D
    """
    n = random.choice(D.nodes())
    nodes_list = [n]
    if sample_size <= len(D.nodes()):
        while len(nodes_list) < sample_size:
            neighbors = D.neighbors(n)
            n = random.choice(neighbors)
            if n not in nodes_list:
                nodes_list.append(n)
        # now lets make a subgraph out of those nodes, containing edges from D
        S= nx.Graph(D.subgraph(nodes_list))
        # NOTE: this is a relatively safe call, which makes a separate copy of attributes(instead just referencing to D), but takes some more space
        # even a deepcopy could be made, if some attributes are containers.
        #A reference version, or even an in-place version  could be made, if space is a problem. (see NetworkX documentation on this)
    else:
        S = None    # in case sample size is larger than dataset graph size, the sampling is not possible and the loop would not finish.
    return S



def subsampling_selfavoiding_walker(D, sample_size):
    """Subsampling procedure: out of a full dataset graph D takes a sample of nodes by a SELF-AVOIDING RANDOM WALK and returns a subsample graph
    sample_size tells how many nodes are taken from D
    """
    nodes_list = []
    if sample_size <= len(D.nodes()):
        while len(nodes_list) < sample_size:
            print "v zunanji zanki"
            unvisited_root = False
            while unvisited_root == False:
                n = random.choice(D.nodes())
                if n not in nodes_list:
                    nodes_list.append(n)
                    unvisited_root = True
            while len(nodes_list) < sample_size:
                print "v notranji zanki"
                neighbors = D.neighbors(n)
                unvisited = [x for x in neighbors if x not in nodes_list]
                if unvisited == []:
                    print "BREAK"
                    break
                else:
                    n = random.choice(unvisited)
                    nodes_list.append(n)
            # now lets make a subgraph out of those nodes, containing edges from D
        S= nx.Graph(D.subgraph(nodes_list))
        # NOTE: this is a relatively safe call, which makes a separate copy of attributes(instead just referencing to D), but takes some more space
        # even a deepcopy could be made, if some attributes are containers.
        #A reference version, or even an in-place version  could be made, if space is a problem. (see NetworkX documentation on this)
    else:
        S = None    # in case sample size is larger than dataset graph size, the sampling is not possible and the loop would not finish.
    return S







def subsampling_forestfire(D, sample_size, pf,  sampleList):
    """Subsampling procedure: out of a full dataset graph D takes a sample of nodes by a FOREST FIRE algorithm and returns a subsample graph
    sample_size tells how many nodes are taken from D
    pf is forward burning probability
    sampleList is empty at first
    """
    if sampleList == []:        # initial call
        n = random.choice(D.nodes())        # we first choose a node uniformly at random
        sampleList = [n]                                
    if sample_size <= len(D.nodes()):   # if sample_size is larger than the size of D we return None 
        if len(sampleList) < sample_size:
            neighbors = D.neighbors(n)
            # we have to select x (p/(1-p) geometric mean) -not-yet-visited- neighbors
            unvisited = [x for x in neighbors if x not in sampleList]
            # now x of them at random
            
            
            for neigh in selection:
                sampleList.append(neigh)
                if len(sampleList) >= sample_size:
                    return nx.Graph(D.subgraph(sampleList))
            
            
            n = random.choice(neighbors)
            if n not in nodes_list:
                nodes_list.append(n)
        # now lets make a subgraph out of those nodes, containing edges from D
        # NOTE: this is a relatively safe call, which makes a separate copy of attributes(instead just referencing to D), but takes some more space
        # even a deepcopy could be made, if some attributes are containers.
        #A reference version, or even an in-place version  could be made, if space is a problem. (see NetworkX documentation on this)
    else:
        return None    # in case sample size is larger than dataset graph size, the sampling is not possible and the loop would not finish.
    return nx.Graph(D.subgraph(nodes_list))




def sampling_exhaustive_general2(D,  P,  Plist,  root_nodes,  returnEmb = False):       ## returnEmb added May2013
    """A procedure that is GENERAL and can sample general graphs for patterns
    D : domain graph (networkx graph with 'predicate' and 'value' attributes)
    P : pattern graph (networkx graph with 'predicate' and 'value' attributes, and 'target' boolean value)
    Plist : ordered list of P nodes
    root_nodes: list of nodes of D that match the root node of P, given in advance, not considered part of sampling procedure
    """
    freq_dict={}    # dictionary with tuples of values as keys and frequency as value: (my_salary_value, his_salary_value, my_satisfaction)
    number_of_targets = 0
    for node in P.nodes():
        if P.node[node]['target'] == True:
            number_of_targets += 1
    # number_of_targets holds the number of target nodes that we are after
    allEmbeddings = []                                              ## added May2013
    iters = 0
    for n in root_nodes:
        iters = iters + 1
##        print " "
##        print "Here goes node " + str(iters) + " out of " + str(len(root_nodes))
        mappings_list = rec_fit2(n, D,  P,  Plist,  0,  [])
        for mapping in mappings_list:
            if returnEmb:                                               ## added May2013
                allEmbeddings.append(mapping)           ## added May2013
            # we'll get the target indices accoding to Plist and collect the values
            target_values = []
            for i in range(len(Plist)):
                if P.node[Plist[i]]['target'] == True:
                    value_tuple = (P.node[Plist[i]]['label'] , D.node[mapping[i]]['value'])
                    target_values.append(value_tuple)
            # now target_values contains all combinations of target nodes' label-value as tuples
            target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.
            if target_tuple in freq_dict:
                freq_dict[target_tuple] += 1
            else:
                freq_dict[target_tuple] = 1
    if returnEmb:                                               ## added May2013
        return (freq_dict, allEmbeddings)           ## added May2013
    else:                                                              ## added May2013
        return freq_dict



def sampling_exhaustive_general_inf(D,  P,  Plist,  root_nodes,short_graph_file_name,output_path):
    """A procedure that is GENERAL and can sample general graphs for patterns
    D : domain graph (networkx graph with 'predicate' and 'value' attributes)
    P : pattern graph (networkx graph with 'predicate' and 'value' attributes, and 'target' boolean value)
    Plist : ordered list of P nodes
    root_nodes: list of nodes of D that match the root node of P, given in advance, not considered part of sampling procedure
    """
    print "exhaustive approach"
    second_interval=0
    freq_dict={}    # dictionary with tuples of values as keys and frequency as value: (my_salary_value, his_salary_value, my_satisfaction)
    number_of_targets = 0
    for node in P.nodes():
        if P.node[node]['target'] == True:
            number_of_targets += 1
    # number_of_targets holds the number of target nodes that we are after
    nodes_observed = 0
    counter=0
    for n in root_nodes:
        nodes_observed = nodes_observed + 1
        counter+=1
        print "Seen: ",counter,"out of: ",len(root_nodes)
        list_for_spent = []
        list_for_spent.append(nodes_observed)
        infinity = float("inf")
        mappings_list = rec_fit_limited(n, D,  P,  Plist,  0,  [],  [infinity],  list_for_spent, freq_dict)
        nodes_observed = list_for_spent[0]
        if(nodes_observed==1):
            raise Wrong_root_node('cannot use this one as a root node')
        #print "nodes observed: ",nodes_observed
        #print "mappings list: ",mappings_list
        for mapping in mappings_list:
            #print mapping
            # we'll get the target indices accoding to Plist and collect the values
            target_values = []
            for i in range(len(Plist)):
                if P.node[Plist[i]]['target'] == True:
                    #print "cannot get: ",D.node[mapping[i]]
                    value_tuple = (P.node[Plist[i]]['label'] , D.node[mapping[i]]['value'])
                    target_values.append(value_tuple)
            # now target_values contains all combinations of target nodes' label-value as tuples
            target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.
            if target_tuple in freq_dict:
                freq_dict[target_tuple] += 1
            else:
                freq_dict[target_tuple] = 1
    print (freq_dict, nodes_observed) 
    return (freq_dict, nodes_observed)

class Wrong_root_node(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)



def sampling_randomnode_general(D,  P,  Plist,  root_nodes,  nlimitlist):
    """
    This is based on a procedure "sampling_exhaustive_general2()", but is limited by a number of nodes it can observe in domain graph D: nlimit
    A procedure that is GENERAL and can sample general graphs for patterns
    D : domain graph (networkx graph with 'predicate' and 'value' attributes)
    P : pattern graph (networkx graph with 'predicate' and 'value' attributes, and 'target' boolean value)
    Plist : ordered list of P nodes
    root_nodes: list of nodes of D that match the root node of P, given in advance, not considered part of sampling procedure
    """
    global globalist_randomnode
    global globaltimes_randomnode
    globalist_randomnode = []
    globaltimes_randomnode = [time.time()]
    freq_dict={}    # dictionary with tuples of values as keys and frequency as value: (my_salary_value, his_salary_value, my_satisfaction)
    number_of_targets = 0
    for node in P.nodes():
        if P.node[node]['target'] == True:
            number_of_targets += 1
    # number_of_targets holds the number of target nodes that we are after
    nodes_observed = 0
    while nodes_observed <= max(nlimitlist):
        #print nlimitlist
        if nodes_observed in nlimitlist:
            total_freq_dict_copy = copy.deepcopy(freq_dict)
            handle_quota(D,  P,  Plist, total_freq_dict_copy,  None)
            ## print "Call to quota handling (main routine) for quota %d" % nodes_observed
        n = root_nodes[random.randrange(len(root_nodes))]
        nodes_observed = nodes_observed + 1
        
        # we have to quota-handle also this one!, otherwise it is not handled anywhere
        if nodes_observed in nlimitlist:
            total_freq_dict_copy = copy.deepcopy(freq_dict)
            handle_quota(D,  P,  Plist, total_freq_dict_copy,  None)
        
        # tukaj bom rabil drugacen rec_fit2 - tak, ki bo spremljal nlimit in vracal tudi nobserved
        # ------ vse ostalo spodaj namrec sploh ne ogleduje node-ov...je samo se uporaba rezultatov...
        list_for_spent = []
        list_for_spent.append(nodes_observed)
        mappings_list = rec_fit_limited(n, D,  P,  Plist,  0,  [],  nlimitlist,  list_for_spent,  freq_dict)
        # list_for_spent gets passed by reference and number gets increased
        nodes_observed = list_for_spent[0]
        if mappings_list != None:       # it can be None if limit is reached inside a call
            for mapping in mappings_list:
                # we'll get the target indices accoding to Plist and collect the values
                target_values = []
                for i in range(len(Plist)):
                    if P.node[Plist[i]]['target'] == True:
                        value_tuple = (P.node[Plist[i]]['label'] , D.node[mapping[i]]['value'])
                        target_values.append(value_tuple)
                # now target_values contains all combinations of target nodes' label-value as tuples
                target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.
                if target_tuple in freq_dict:
                    freq_dict[target_tuple] += 1
                else:
                    freq_dict[target_tuple] = 1
    # now with quota handlers, we just return the global list of freqdicts:
    return [globalist_randomnode,  globaltimes_randomnode]



def rec_fit2(n, D,  P,  Plist,  i,  matched_list):
    ##print "rec_fit2 je prisel v node %s z i=%s" % (str(n),  str(i)) 
    matching_subgraphs = []
    if i < len(Plist):       #border condition
        ##print "in vzorca se ni konec, ker i=%s" % str(i)
        ##print "primerjal bom n=%s in m=%s" % (str(n),  str(Plist[i])) 
        if matches(n, D,  Plist[i], P,  matched_list,  Plist):
            ##print "in tale se ujema"
            matched_list.append(D.node[n]['id'])
            candidates = []
            for matched in matched_list:
                for x in D.neighbors(matched):
                    if x not in matched_list:   # we do not want to check the already matched, besides: they should not appear again(?)
                        candidates.append(x)
            ##print "in kandidati iz [ %s ] za naprej so %s" % (str(n),  str(candidates))
            for c in candidates:
                copyforcandidate = copy.deepcopy(matched_list)
                result = rec_fit2(c,  D,  P,  Plist,  i+1,  copyforcandidate)
                if result != None:
                    for list in result:                        
                        if list not in matching_subgraphs:
                            matching_subgraphs.append(list)
        else:
            return None
        ##print "nazaj [node=%s, i=%s] sporocim: %s" % (str(n),  str(i),  str(matching_subgraphs))
        return matching_subgraphs
    else:
        ##print "VZORCA JE KONEC"
        # search is over - report back
        #if we have full pattern report back a full matching list, otherwise an empty list
        if len(matched_list) == len(Plist):
            ##print "NAZAJ [node=%s, i=%s] SPOROCIM: %s" % (str(n),  str(i),  str(matched_list))
            return [matched_list]
        else:
            ##print "NAZAJ SPOROCIM None"
            return None



#IrMA: changed it here that the function returns the total_freq_dict (needed it for time snapshots)
def handle_quota(D,  P,  Plist,  total_freq_dict,  mappings_list,thread_number):
    #global globalist_randomnode
    #global globaltimes_randomnode   
    #experiments.globals.globaltimes_randomnode[thread_number].append(time.time() - experiments.globals.globaltimes_randomnode[thread_number][0])
    # we will be adding to total_freq_dict:
    if mappings_list != None:       # it can be None if limit is reached inside a call
        for mapping in mappings_list:
            # we'll get the target indices accoding to Plist and collect the values
            target_values = []
            for i in range(len(Plist)):
                if P.node[Plist[i]]['target'] == True:
                    value_tuple = (P.node[Plist[i]]['label'] , D.node[mapping[i]]['value'])
                    target_values.append(value_tuple)
            # now target_values contains all combinations of target nodes' label-value as tuples
            target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.
            if target_tuple in total_freq_dict:
                total_freq_dict[target_tuple] += 1
            else:
                total_freq_dict[target_tuple] = 1
    # otherwise there is nothing to add - just report the total_freq_dict that you were called with
    #get nr embeddings
    nr_emb=0
    for key in total_freq_dict.keys():
        nr_emb+=total_freq_dict[key]
    #experiments.globals.globalist_randomnode[thread_number].append(total_freq_dict)
    experiments.globals.nlimit_nr_embeddings.append(nr_emb)  
    return total_freq_dict

def rec_fit_limited(n, D,  P,  Plist,  i,  matched_list,  nlimitlist,  nodes_observed_list,  total_freq_dict,thread_number,q,q1):
    matching_subgraphs = []
    if i < len(Plist):       #border condition
        if matches(n, D,  Plist[i], P,  matched_list,  Plist):
            matched_list.append(D.node[n]['id'])
            candidates = []
            for matched in matched_list:
                for x in D.neighbors(matched):
                    if x not in matched_list:   # we do not want to check the already matched, besides: they should not appear again(?)
                        candidates.append(x)
            counter=1
            for c in candidates:
                counter+=1
                nodes_observed_list[0] = nodes_observed_list[0] + 1
                if nodes_observed_list[0] in nlimitlist:    #intermediate or final quota: make copies and call procedure to handle them
                    total_freq_dict_copy = copy.deepcopy(total_freq_dict)
                    matching_subgraphs_copy = copy.deepcopy(matching_subgraphs)
                    handle_quota(D,  P,  Plist, total_freq_dict_copy,  matching_subgraphs_copy,thread_number)
                if nodes_observed_list[0] <= max(nlimitlist):
                    copyforcandidate = copy.deepcopy(matched_list)
                    result = rec_fit_limited(c,  D,  P,  Plist,  i+1,  copyforcandidate,  nlimitlist,  nodes_observed_list,  total_freq_dict,thread_number,q,q1)
                    if result != None:
                        for list in result:                        
                            if list not in matching_subgraphs:
                                matching_subgraphs.append(list)
                else:
                    return None
        else:
            return None
        q.put(matching_subgraphs)
        q1.put(nodes_observed_list)
        return matching_subgraphs
    else:
        # search is over - report back
        #if we have full pattern report back a full matching list, otherwise an empty list
        if len(matched_list) == len(Plist):
            q.put([matched_list])
            q1.put(nodes_observed_list)
            return [matched_list]
        else:
            return None
        
def rec_fit_limited_original(n, D,  P,  Plist,  i,  matched_list,  nlimitlist,  nodes_observed_list,  total_freq_dict,thread_number):
    matching_subgraphs = []
    if i < len(Plist):       #border condition
        if matches(n, D,  Plist[i], P,  matched_list,  Plist):
            matched_list.append(D.node[n]['id'])
            candidates = []
            for matched in matched_list:
                for x in D.neighbors(matched):
                    if x not in matched_list:   # we do not want to check the already matched, besides: they should not appear again(?)
                        candidates.append(x)
            counter=1
            for c in candidates:
                counter+=1
                nodes_observed_list[0] = nodes_observed_list[0] + 1
                if nodes_observed_list[0] in nlimitlist:    #intermediate or final quota: make copies and call procedure to handle them
                    total_freq_dict_copy = copy.deepcopy(total_freq_dict)
                    matching_subgraphs_copy = copy.deepcopy(matching_subgraphs)
                    handle_quota(D,  P,  Plist, total_freq_dict_copy,  matching_subgraphs_copy,thread_number)
                if nodes_observed_list[0] <= max(nlimitlist):
                    copyforcandidate = copy.deepcopy(matched_list)
                    result = rec_fit_limited_original(c,  D,  P,  Plist,  i+1,  copyforcandidate,  nlimitlist,  nodes_observed_list,  total_freq_dict,thread_number)
                    if result != None:
                        for list in result:                        
                            if list not in matching_subgraphs:
                                matching_subgraphs.append(list)
                else:
                    return None
        else:
            return None
        return matching_subgraphs
    else:
        # search is over - report back
        #if we have full pattern report back a full matching list, otherwise an empty list
        if len(matched_list) == len(Plist):
            return [matched_list]
        else:
            return None
               
                             
               
def rec_fit_limited_global(n, D,  P,  Plist,  i,  matched_list,  nlimitlist,  nodes_observed_list,  total_freq_dict,thread_number,lock,experiment_name,root_nodes):    
    if experiments.globals.abort:
         if len(matched_list) == len(Plist):
             temp_result=[matched_list]
             nodes_observed=nodes_observed_list
             with lock:
                experiments.globals.temporary_embeddings.append(matched_list)
             return [matched_list]
         else:
             nodes_observed=nodes_observed_list
             return None
    matching_subgraphs = []
    global temp_result
    global nodes_observed
    if i < len(Plist):       #border condition
        if matches(n, D,  Plist[i], P,  matched_list,  Plist):
            matched_list.append(D.node[n]['id'])
            candidates = []
            for matched in matched_list:
                for x in D.neighbors(matched):
                    if x not in matched_list:   # we do not want to check the already matched, besides: they should not appear again(?)
                        candidates.append(x)
            counter=1
            experiments.globals.candidates+=len(candidates)
            #DODALA OVDJE!
            if len(candidates)==0:
                candidates=[n]
            for c in candidates:  
                counter+=1
                nodes_observed_list[0] = nodes_observed_list[0] + 1
                experiments.globals.temporary_observed[0]=experiments.globals.temporary_observed[0]+1
                if True:
                    copyforcandidate = copy.deepcopy(matched_list)
                    result = rec_fit_limited_global(c,  D,  P,  Plist,  i+1,  copyforcandidate,  nlimitlist,  nodes_observed_list,  total_freq_dict,thread_number,lock,experiment_name,root_nodes)
                    if result != None:
                        for list in result:  
                            if list not in matching_subgraphs:
                                matching_subgraphs.append(list)                        
        else:
            nodes_observed=nodes_observed_list
            return None
        temp_result=matching_subgraphs
        return matching_subgraphs
    else:
        if len(matched_list) == len(Plist):
            if matched_list in experiments.globals.temporary_embeddings:
       	           return [matched_list]
            
            with lock:
                 experiments.globals.nr_embeddings_exhaustive+=1
                 experiments.globals.temporary_embeddings.append(matched_list)
                 if(nodes_observed==1):
                   raise Wrong_root_node('cannot use this one as a root node')
                 target_values = []
                 for i in range(len(Plist)):
                    if P.node[Plist[i]]['target'] == True:
                             value_tuple = (P.node[Plist[i]]['label'] , D.node[matched_list[i]]['value'])
                             target_values.append(value_tuple)
                 target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.            
                 if target_tuple in experiments.globals.freq_dict_exhaustive:
                            experiments.globals.freq_dict_exhaustive[target_tuple] += 1
                            experiments.globals.freq_dict_tuple_count[target_tuple] += 1
                 else:
                           experiments.globals.freq_dict_exhaustive[target_tuple] = 1
                           experiments.globals.freq_dict_tuple_count[target_tuple] = 1
                 temp_result=[matched_list]
                 nodes_observed=nodes_observed_list                     
            return [matched_list]
        else:
         nodes_observed=nodes_observed_list
         return None
     
def get_nr_embeddings(freq_dict,iterations):
    nr_emb=0
    for k in freq_dict.keys():
        nr_emb+=freq_dict[k]
    return nr_emb

def rec_fit_limited_basic(n, D,  P,  Plist,  i,  matched_list,  nlimitlist,  nodes_observed_list,  total_freq_dict,thread_number):
    #print "BASIC RANDOM"
    matching_subgraphs = []
    if i < len(Plist):       #border condition
        if matches(n, D,  Plist[i], P,  matched_list,  Plist):
            matched_list.append(D.node[n]['id'])
            candidates = []
            for matched in matched_list:
                for x in D.neighbors(matched):
                    if x not in matched_list:   # we do not want to check the already matched, besides: they should not appear again(?)
                        candidates.append(x)
            counter=1
            for c in candidates:
                counter+=1
                nodes_observed_list[0] = nodes_observed_list[0] + 1
                if nodes_observed_list[0] in nlimitlist:    #intermediate or final quota: make copies and call procedure to handle them
                    total_freq_dict_copy = copy.deepcopy(total_freq_dict)
                    matching_subgraphs_copy = copy.deepcopy(matching_subgraphs)
                    handle_quota(D,  P,  Plist, total_freq_dict_copy,  matching_subgraphs_copy,thread_number)
                if nodes_observed_list[0] <= max(nlimitlist):
                    copyforcandidate = copy.deepcopy(matched_list)
                    result = rec_fit_limited_basic(c,  D,  P,  Plist,  i+1,  copyforcandidate,  nlimitlist,  nodes_observed_list,  total_freq_dict,thread_number)
                    if result != None:
                        for list in result:                        
                            if list not in matching_subgraphs:
                                matching_subgraphs.append(list)
                else:
                    return None
        else:
            return None
        return matching_subgraphs
    else:
        # search is over - report back
        #if we have full pattern report back a full matching list, otherwise an empty list
        if len(matched_list) == len(Plist):
            return [matched_list]
        else:
            return None


def handle_quota_Furer(D,  P, total_Zlist_dict_copy, result_to_give, iteration_counter,thread_number):
    experiments.globals.globaltimes_furer[thread_number].append(time.time() -  experiments.globals.globaltimes_furer[thread_number][0])
    experiments.globals.nlimit_iteration_counter.append(iteration_counter)
    freq_dict = {}
    if result_to_give[1] != None:   # to bi bilo verjetno cudno, ce bi se zgodilo - zadnji node iz kvote bi dopolnil pattern
        print "Ce to izpisujem, potem bo zdej crknilo, ker nisi v rekurzijo poslal se root_nodes in OBdecomp, ki se jih tu nuca."
        actualX = result_to_give[0] * len(root_nodes)
        mapping = result_to_give[1]     # this is mapping for OBdecomp FLAT.
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        target_values = []
        for i in range(len(OBd_flat)):
            if P.node[OBd_flat[i]]['target'] == True:
                value_tuple = (P.node[OBd_flat[i]]['label'] , D.node[mapping[i]]['value'])
                target_values.append(value_tuple)
        # now target_values contains all combinations of target nodes' label-value as tuples
        target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.
        if target_tuple in Zlist_dict:   # this checks for KEYS in Zlist_dict
            Zlist_dict[target_tuple] = Zlist_dict[target_tuple] + actualX
        else:
            Zlist_dict[target_tuple] = 0
            Zlist_dict[target_tuple] = Zlist_dict[target_tuple] + actualX
        # now also give zeros to all others...this is the correction of the "relaxed" version
        # this step not needed any more since we do not have lists anymore out of debug
    nr_emb=0
    nr_emb1=0
    
    for k in total_Zlist_dict_copy.keys():
        freq_dict[k] = (total_Zlist_dict_copy[k])/float(iteration_counter)   # simply an average of a list
        nr_emb+=freq_dict[k]
        nr_emb1+=total_Zlist_dict_copy[k]
    experiments.globals.globalist_furer[thread_number].append(freq_dict)
    experiments.globals.nlimit_nr_embeddings.append(nr_emb)
    return freq_dict

def rec_fit_Furer(nodes, D,  P,  OBdecomp,   i,  matched_list,  nlimitlist,  nodes_observed_list, Zlist_dict, iteration_counter,  epsilon_from_above,thread_number):
    """
    nodes : a list of (candidate) nodes to fit in this step GIVEN IN THE SAME ORDER as appear in OBdecomp!
    OBdecomp : ordered bipartite decomposition on P, which is given. First element is root. # [ [2] , [1,3] , [4] , [5, 6] ]
    i : index of the currently analyzed decomposition element
    """
    X = 1
    Z = 0
    #print "Candidate nodes: "
    #for n in nodes:
    #    print D.node[n]
    #    time.sleep(5)
    if len(nlimitlist)<=experiments.globals.cqi[thread_number]:
        nlimitlist.append(sum(nlimitlist))
    if nodes_observed_list[0] > nlimitlist[experiments.globals.cqi[thread_number]]:
        experiments.globals.cqi[thread_number] = experiments.globals.cqi[thread_number] +1    # we increase the index of position of quota to check upon
        total_Zlist_dict_copy = copy.deepcopy(Zlist_dict)
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            matched_list_copy = copy.deepcopy(matched_list)
            result_to_give = [X, matched_list_copy]
        else:
            result_to_give = [0, None]        
        handle_quota_Furer(D,  P, total_Zlist_dict_copy, result_to_give, iteration_counter,thread_number)
    
    if (i < len(OBdecomp)) and (nodes_observed_list[0] <= max(nlimitlist)):       #border condition, limit condition
        matched_list = matched_list + nodes
        candidates = []
        for matched in matched_list:
            
            for x in D.neighbors(matched):
                if x not in matched_list:   # we do not want to check the already matched, besides: they should not appear again(?)
                    candidates.append(x)
        
        
        nodes_observed_list[0] = nodes_observed_list[0] + len(candidates)
        epsilon = len(candidates) # epsilon for quota checking
        if i+1 < len(OBdecomp):     # so, only, if there is any following decomposition step
            good_collection = []
            OBd_matched_next = [item for sublist in OBdecomp[:i+1] for item in sublist]
            for el in OBdecomp[i+1]:
                good_el = []
                for c in candidates:
                  #print "Candidate: ",c,"for: ",matched_list
                  if matches_Furer(c, D,  el, P,  matched_list,  OBd_matched_next):
                          #print "Candidate ",c,"approved"
                          good_el.append(c)
                good_collection.append(good_el)
            allcombinations = list(itertools.product(*good_collection))     # but here are all, also such that use one node in many roles -><-
            allgoodcombinations = []
            for combi in allcombinations:
                if len(list(combi)) == len(set(combi)):
                    allgoodcombinations.append(list(combi))
            if(len(allgoodcombinations))==0:
                return [0, None]
            if True:
                skt = list(set(tuple(i) for i in allgoodcombinations))
                allgoodcombinations=[list(elem) for elem in skt]
                number_of_combinations = len(skt)        # counts the number of their combinations
                X = X * number_of_combinations
                if number_of_combinations > 0:
                    nodes_next = random.choice(allgoodcombinations)
                    ##print "all good combs: ",allgoodcombinations
                    #print "nodes next: ",nodes_next
                    copyforcandidate = copy.deepcopy(matched_list)
                    #time.sleep(30)
                    result = rec_fit_Furer(nodes_next,  D,  P,  OBdecomp,  i+1,  copyforcandidate,  nlimitlist,  nodes_observed_list,  Zlist_dict, iteration_counter,  epsilon,thread_number)
                    if result[1] != None:
                        matched_list = result[1]
                        X = X * result[0]
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            return [X, matched_list]
        else:
            return [0, None]        
    else:   # because of border condition we never get here, it is all pretested..
        # search is over - report back
        #if we have full pattern report back a full matching list, otherwise an empty list
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            return [X, matched_list]
        else:
            return [0, None]
        
        
def rec_fit_Furer_bug_fix(nodes, D,  P,  OBdecomp,   i,  matched_list,  nlimitlist,  nodes_observed_list, Zlist_dict, iteration_counter,  epsilon_from_above,thread_number):
    """
    nodes : a list of (candidate) nodes to fit in this step GIVEN IN THE SAME ORDER as appear in OBdecomp!
    OBdecomp : ordered bipartite decomposition on P, which is given. First element is root. # [ [2] , [1,3] , [4] , [5, 6] ]
    i : index of the currently analyzed decomposition element
    """
    X = 1
    Z = 0
    if len(nlimitlist)<=experiments.globals.cqi[thread_number]:
        nlimitlist.append(sum(nlimitlist))
    if nodes_observed_list[0] > nlimitlist[experiments.globals.cqi[thread_number]]:
        experiments.globals.cqi[thread_number] = experiments.globals.cqi[thread_number] +1    # we increase the index of position of quota to check upon
        total_Zlist_dict_copy = copy.deepcopy(Zlist_dict)
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            matched_list_copy = copy.deepcopy(matched_list)
            result_to_give = [X, matched_list_copy]
        else:
            result_to_give = [0, None]        
        handle_quota_Furer(D,  P, total_Zlist_dict_copy, result_to_give, iteration_counter,thread_number)
    
    if (i < len(OBdecomp)) and (nodes_observed_list[0] <= max(nlimitlist)):       #border condition, limit condition
        matched_list = matched_list + nodes
        candidates = []
        for matched in matched_list:
            for x in D.neighbors(matched):
                if x not in matched_list:   # we do not want to check the already matched, besides: they should not appear again(?)
                    candidates.append(x)
        print "CANDIDATES: "
        nodes_observed_list[0] = nodes_observed_list[0] + len(candidates)
        epsilon = len(candidates) # epsilon for quota checking
        if i+1 < len(OBdecomp):     # so, only, if there is any following decomposition step
            good_collection = []
            OBd_matched_next = [item for sublist in OBdecomp[:i+1] for item in sublist]
            for el in OBdecomp[i+1]:
                good_el = []
                for c in candidates:
                  #if D.node[c]['predicate'] == P.node[el]['predicate']:                             #    the change to IZO-MATCH test the candidates
                  if matches_Furer(c, D,  el, P,  matched_list,  OBd_matched_next):
                        #if not c in good_el: #IRMA ADDED TO SEE IF BUG FIXED!!!
                          good_el.append(c)
                #if not good_el in good_collection:#IRMA ADDED TO SEE IF BUG FIXED!!!
                good_collection.append(good_el)
             # now we have this good collection:  [ [gfor4, gfor4, gfor4] , [gfor5], [gfor6, gfor6 , gfor6] ]
            ########### DEBUG 2015 change ########################################################################
            lists_intersection = set.intersection(*map(set,good_collection))
            
            
            if len(lists_intersection) > 0:
                #print "WARNING - candidate node in multiple possible roles...slower combination sampler will be used."
                allcombinations = list(itertools.product(*good_collection))     # but here are all, also such that use one node in many roles -><-
                allgoodcombinations = []
                for combi in allcombinations:
                    if len(list(combi)) == len(set(combi)):
                        allgoodcombinations.append(list(combi))
                number_of_combinations = len(allgoodcombinations)
                X = X * number_of_combinations
                if(len(allgoodcombinations))==0:
                     return [0, None]
                # now we have to pick a random one - a random item from each list is taken
                if number_of_combinations > 0:
                    nodes_next = []
                    for elist in allgoodcombinations:
                        item = random.choice(elist)
                        nodes_next.append(item)
                    s_next_nodes=set(nodes_next)
                    if(len(s_next_nodes)!=len(OBdecomp[i+1])):
                          return [0, None]
                    # now only the recursive call
                    copyforcandidate = copy.deepcopy(matched_list)
                    result = rec_fit_Furer_bug_fix(nodes_next,  D,  P,  OBdecomp,  i+1,  copyforcandidate,  nlimitlist,  nodes_observed_list,  Zlist_dict, iteration_counter,  epsilon,thread_number)
                    # result is of this kind: [X, num_visited, matched_list]
                    # -----------------ZDAJ PA uredi se vracanje rezultatov in stetje X-ov..., pa stestiraj.
                    if result[1] != None:
                        matched_list = result[1]
                        X = X * result[0]                
            else:
                number_of_combinations = reduce(lambda x, y: x*y, [len(x) for x in good_collection])        # counts the number of their combinations
                X = X * number_of_combinations
                # now we have to pick a random one - a random item from each list is taken
                if number_of_combinations > 0:
                    nodes_next = []
                    for elist in good_collection:
                        item = random.choice(elist)
                        nodes_next.append(item)
                    s_next_nodes=set(nodes_next)
                    if(len(s_next_nodes)!=len(OBdecomp[i+1])):
                          return [0, None]
                    # now only the recursive call
                    copyforcandidate = copy.deepcopy(matched_list)
                    result = rec_fit_Furer_bug_fix(nodes_next,  D,  P,  OBdecomp,  i+1,  copyforcandidate,  nlimitlist,  nodes_observed_list,  Zlist_dict, iteration_counter,  epsilon,thread_number)
                    # result is of this kind: [X, num_visited, matched_list]
                    # -----------------ZDAJ PA uredi se vracanje rezultatov in stetje X-ov..., pa stestiraj.
                    if result[1] != None:
                        matched_list = result[1]
                        X = X * result[0]
            ########### DEBUG 2015 change ########################################################################
        # and in any case return what you have received
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            return [X, matched_list]
        else:
            return [0, None]        
    else:   # because of border condition we never get here, it is all pretested..
        # search is over - report back
        #if we have full pattern report back a full matching list, otherwise an empty list
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            return [X, matched_list]
        else:
            return [0, None]
        
        
def rec_fit_False_Furer(nodes, D,  P,  OBdecomp,   i,  matched_list,  nlimitlist,  nodes_observed_list, Zlist_dict, iteration_counter,  epsilon_from_above,thread_number):
    """
    nodes : a list of (candidate) nodes to fit in this step GIVEN IN THE SAME ORDER as appear in OBdecomp!
    OBdecomp : ordered bipartite decomposition on P, which is given. First element is root. # [ [2] , [1,3] , [4] , [5, 6] ]
    i : index of the currently analyzed decomposition element
    """
    X = 1
    Z = 0
    
    if nodes_observed_list[0] > nlimitlist[cqi]:
        experiments.globals.cqi[thread_number] = experiments.globals.cqi[thread_number] +1    # we increase the index of position of quota to check upon
        total_Zlist_dict_copy = copy.deepcopy(Zlist_dict)
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            matched_list_copy = copy.deepcopy(matched_list)
            result_to_give = [X, matched_list_copy]
        else:
            result_to_give = [0, None]        
        handle_quota_Furer(D,  P, total_Zlist_dict_copy, result_to_give, iteration_counter,thread_number)
        ##print "Call to Furer quota handling at quota %d" % nlimitlist[cqi-1]
    
    if (i < len(OBdecomp)) and (nodes_observed_list[0] <= max(nlimitlist)):       #border condition, limit condition
        matched_list = matched_list + nodes
        candidates = []
        for matched in matched_list:
            for x in D.neighbors(matched):
                if x not in matched_list:   # we do not want to check the already matched, besides: they should not appear again(?)
                    candidates.append(x)
        nodes_observed_list[0] = nodes_observed_list[0] + len(candidates)
        epsilon = len(candidates) # epsilon for quota checking
        # now we have all candidates
        # --- verify their fit with the next decomposition step (predicate only for starting...)
        # --- count the appropriate ones, * X, pick one random
        # --- and then make the next recursive call on that picked one
        if i+1 < len(OBdecomp):     # so, only, if there is any following decomposition step
            # OBdecomp[i+1] can be composed of many nodes: [4, 5, 6]
            # we'll make a list of lists for good candidates: [ [gfor4, gfor4, gfor4] , [gfor5], [gfor6, gfor6 , gfor6] ]
            # counting number of combinations and picking one random one will then be easy
            good_collection = []
            OBd_matched_next = [item for sublist in OBdecomp[:i+1] for item in sublist]
    # 3 old comment lines from the start of recursion...namesto samo enega "matches", moramo to preveriti za vse node, ki naj bi se prilegali v tej dekompoziciji
    # all OBdecomp matched so far must be collected for matching function - so, all nodes in lists up to (excluding) i-th list
    # OBdecomp[:i] are decompositions so far (up to i, excluding i), the rest is just list comprehension to flatten the list of lists into one list of items (fastest way to do it)                
            for el in OBdecomp[i+1]:
                good_el = []
                for c in candidates:
##                        if D.node[c]['predicate'] == P.node[el]['predicate']:                             #    the change to IZO-MATCH test the candidates
                    if matches_Furer(c, D,  el, P,  matched_list,  OBd_matched_next):
                        good_el.append(c)
                good_collection.append(good_el)
            number_of_combinations = reduce(lambda x, y: x*y, [len(x) for x in good_collection])        # counts the number of their combinations
            X = X * number_of_combinations
            if number_of_combinations > 0:
                nodes_next = []
                for list in good_collection:
                    item = random.choice(list)
                    nodes_next.append(item)
                # now only the recursive call
                copyforcandidate = copy.deepcopy(matched_list)
                result = rec_fit_False_Furer(nodes_next,  D,  P,  OBdecomp,  i+1,  copyforcandidate,  nlimitlist,  nodes_observed_list,  Zlist_dict, iteration_counter,  epsilon,thread_number)
                # result is of this kind: [X, num_visited, matched_list]
                # -----------------ZDAJ PA uredi se vracanje rezultatov in stetje X-ov..., pa stestiraj.
                if result[1] != None:
                    matched_list = result[1]
                    X = X * result[0]
        # and in any case return what you have received
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            #print "Match found"
            return [X, matched_list]
        else:
            return [0, None]        
    else:   # because of border condition we never get here, it is all pretested..
        # search is over - report back
        #if we have full pattern report back a full matching list, otherwise an empty list
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            #print "Match found"
            return [X, matched_list]
        else:
            return [0, None]


def rec_fit_False_Furer_global(nodes, D,  P,  OBdecomp,   i,  matched_list,  nlimitlist,  nodes_observed_list, Zlist_dict, iteration_counter,  epsilon_from_above,thread_number):
    """
    nodes : a list of (candidate) nodes to fit in this step GIVEN IN THE SAME ORDER as appear in OBdecomp!
    OBdecomp : ordered bipartite decomposition on P, which is given. First element is root. # [ [2] , [1,3] , [4] , [5, 6] ]
    i : index of the currently analyzed decomposition element
    """
    X = 1
    Z = 0
    global temp_result

    if nodes_observed_list[0] > nlimitlist[cqi]:
        experiments.globals.cqi[thread_number] = experiments.globals.cqi[thread_number] +1    # we increase the index of position of quota to check upon
        total_Zlist_dict_copy = copy.deepcopy(Zlist_dict)
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            matched_list_copy = copy.deepcopy(matched_list)
            result_to_give = [X, matched_list_copy]
        else:
            result_to_give = [0, None]        
        handle_quota_Furer(D,  P, total_Zlist_dict_copy, result_to_give, iteration_counter,thread_number)
        ##print "Call to Furer quota handling at quota %d" % nlimitlist[cqi-1]
    
    if (i < len(OBdecomp)) and (nodes_observed_list[0] <= max(nlimitlist)):       #border condition, limit condition
        matched_list = matched_list + nodes
        candidates = []
        for matched in matched_list:
            for x in D.neighbors(matched):
                if x not in matched_list:   # we do not want to check the already matched, besides: they should not appear again(?)
                    candidates.append(x)
        nodes_observed_list[0] = nodes_observed_list[0] + len(candidates)
        epsilon = len(candidates) # epsilon for quota checking
        # now we have all candidates
        # --- verify their fit with the next decomposition step (predicate only for starting...)
        # --- count the appropriate ones, * X, pick one random
        # --- and then make the next recursive call on that picked one
        if i+1 < len(OBdecomp):     # so, only, if there is any following decomposition step
            # OBdecomp[i+1] can be composed of many nodes: [4, 5, 6]
            # we'll make a list of lists for good candidates: [ [gfor4, gfor4, gfor4] , [gfor5], [gfor6, gfor6 , gfor6] ]
            # counting number of combinations and picking one random one will then be easy
            good_collection = []
            OBd_matched_next = [item for sublist in OBdecomp[:i+1] for item in sublist]
    # 3 old comment lines from the start of recursion...namesto samo enega "matches", moramo to preveriti za vse node, ki naj bi se prilegali v tej dekompoziciji
    # all OBdecomp matched so far must be collected for matching function - so, all nodes in lists up to (excluding) i-th list
    # OBdecomp[:i] are decompositions so far (up to i, excluding i), the rest is just list comprehension to flatten the list of lists into one list of items (fastest way to do it)                
            for el in OBdecomp[i+1]:
                good_el = []
                for c in candidates:
##                        if D.node[c]['predicate'] == P.node[el]['predicate']:                             #    the change to IZO-MATCH test the candidates
                    if matches_Furer(c, D,  el, P,  matched_list,  OBd_matched_next):
                        good_el.append(c)
                good_collection.append(good_el)
            # now we have this good collection:  [ [gfor4, gfor4, gfor4] , [gfor5], [gfor6, gfor6 , gfor6] ]
            number_of_combinations = reduce(lambda x, y: x*y, [len(x) for x in good_collection])        # counts the number of their combinations
            X = X * number_of_combinations
            # now we have to pick a random one - a random item from each list is taken
            if number_of_combinations > 0:
                nodes_next = []
                for list in good_collection:
                    item = random.choice(list)
                    nodes_next.append(item)
                # now only the recursive call
                copyforcandidate = copy.deepcopy(matched_list)
                temp_result = rec_fit_False_Furer(nodes_next,  D,  P,  OBdecomp,  i+1,  copyforcandidate,  nlimitlist,  nodes_observed_list,  Zlist_dict, iteration_counter,  epsilon,thread_number)
                # result is of this kind: [X, num_visited, matched_list]
                # -----------------ZDAJ PA uredi se vracanje rezultatov in stetje X-ov..., pa stestiraj.
                if temp_result[1] != None:
                    matched_list = temp_result[1]
                    X = X * temp_result[0]
        # and in any case return what you have received
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            temp_result= [X, matched_list]
            return [X, matched_list]
        else:
            temp_result=[0, None] 
            return [0, None]        
    else:   # because of border condition we never get here, it is all pretested..
        # search is over - report back
        #if we have full pattern report back a full matching list, otherwise an empty list
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            temp_result=[X, matched_list]
            return [X, matched_list]
        else:
            temp_result=[0, None]
            return [0, None]



def rec_fit_Furer_global(nodes, D,  P,  OBdecomp,  i,  matched_list,  nlimitlist,  nodes_observed_list, Zlist_dict, iteration_counter,  epsilon_from_above,thread_number):
    """
    nodes : a list of (candidate) nodes to fit in this step GIVEN IN THE SAME ORDER as appear in OBdecomp!
    OBdecomp : ordered bipartite decomposition on P, which is given. First element is root. # [ [2] , [1,3] , [4] , [5, 6] ]
    i : index of the currently analyzed decomposition element
    """
    X = 1
    Z = 0
    global temp_result
    if len(nlimitlist)<=experiments.globals.cqi[thread_number]:
        nlimitlist.append(sum(nlimitlist))
    printing=False
    if printing:
        print "------------ Iznovaaaa --------------------"
        print "Nodes: "
        for n in nodes:
           print D.node[n]
        print "i " ,i
    if nodes_observed_list[0] > nlimitlist[experiments.globals.cqi[thread_number]]:
        experiments.globals.cqi[thread_number] = experiments.globals.cqi[thread_number] +1    # we increase the index of position of quota to check upon
        total_Zlist_dict_copy = copy.deepcopy(Zlist_dict)
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            matched_list_copy = copy.deepcopy(matched_list)
            result_to_give = [X, matched_list_copy]
        else:
            result_to_give = [0, None]        
        handle_quota_Furer(D,  P, total_Zlist_dict_copy, result_to_give, iteration_counter,thread_number)
    if (i < len(OBdecomp)) and (nodes_observed_list[0] <= max(nlimitlist)):       #border condition, limit condition
        matched_list = matched_list + nodes
        if printing:
            print "Matched list:"
            for m in matched_list:
                print D.node[m]
        candidates = []
        for matched in matched_list:
            for x in D.neighbors(matched):
                if x not in matched_list:   # we do not want to check the already matched, besides: they should not appear again(?)
                    candidates.append(x)
        if printing:
         print "i ",i
         print "Candidates:"
         for c in candidates:
            print D.node[c]
        nodes_observed_list[0] = nodes_observed_list[0] + len(candidates)
        epsilon = len(candidates) # epsilon for quota checking
        # now we have all candidates
        # --- verify their fit with the next decomposition step (predicate only for starting...)
        # --- count the appropriate ones, * X, pick one random
        # --- and then make the next recursive call on that picked one
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
                
        if i+1 < len(OBdecomp):     # so, only, if there is any following decomposition step
            # OBdecomp[i+1] can be composed of many nodes: [4, 5, 6]
            # we'll make a list of lists for good candidates: [ [gfor4, gfor4, gfor4] , [gfor5], [gfor6, gfor6 , gfor6] ]
            # counting number of combinations and picking one random one will then be easy
            good_collection = []
            OBd_matched_next = [item for sublist in OBdecomp[:i+1] for item in sublist]
    # 3 old comment lines from the start of recursion...namesto samo enega "matches", moramo to preveriti za vse node, ki naj bi se prilegali v tej dekompoziciji
    # all OBdecomp matched so far must be collected for matching function - so, all nodes in lists up to (excluding) i-th list
    # OBdecomp[:i] are decompositions so far (up to i, excluding i), the rest is just list comprehension to flatten the list of lists into one list of items (fastest way to do it)                
            if printing:
                print "Finding candidates: ",OBdecomp[i+1]
            for el in OBdecomp[i+1]:
                good_el = []
                for c in candidates:
                  if matches_Furer(c, D,  el, P,  matched_list,  OBd_matched_next):
                          good_el.append(c)
                good_collection.append(good_el)
            if printing:
                print "good collection: ",good_collection
             # now we have this good collection:  [ [gfor4, gfor4, gfor4] , [gfor5], [gfor6, gfor6 , gfor6] ]
            ########### DEBUG 2015 change ########################################################################
            lists_intersection = set.intersection(*map(set,good_collection))
            if printing:
              print "Intersections:", lists_intersection 
            if len(lists_intersection) > 0:
                #print "WARNING - candidate node in multiple possible roles...slower combination sampler will be used."
                allcombinations = list(itertools.product(*good_collection))     # but here are all, also such that use one node in many roles -><-
                if printing:
                   print "all  combinations:",allcombinations
                allgoodcombinations = []
                for combi in allcombinations:
                    if len(list(combi)) == len(set(combi)):
                        allgoodcombinations.append(list(combi))
                number_of_combinations = len(allgoodcombinations)  
                #print "Number of combinations: ",number_of_combinations
                X = X * number_of_combinations
                # now we have to pick a random one - a random item from each list is taken
                #print "All good combinations: ",allgoodcombinations
                #print number_of_combinations            
                if number_of_combinations > 0:
                    nodes_next = []
                    for elist in allgoodcombinations:
                        item = random.choice(elist)
                        nodes_next.append(item)
                        #if len(nodes_next)==len(OBdecomp[i+1]): #IRMA ADDED: Willl it help - test with succeeded patterns!
                        #    break
                    # now only the recursive call
                    copyforcandidate = copy.deepcopy(matched_list)
                    if printing:
                        print "nodes next: ",nodes_next
                    temp_result = rec_fit_Furer_global(nodes_next,  D,  P,  OBdecomp, i+1,  copyforcandidate,  nlimitlist,  nodes_observed_list,  Zlist_dict, iteration_counter,  epsilon,thread_number)
                    # result is of this kind: [X, num_visited, matched_list]
                    # -----------------ZDAJ PA uredi se vracanje rezultatov in stetje X-ov..., pa stestiraj.
                    if temp_result[1] != None:
                        matched_list = temp_result[1]
                        X = X * temp_result[0]                                   
            else:
                number_of_combinations = reduce(lambda x, y: x*y, [len(x) for x in good_collection])        # counts the number of their combinations
                X = X * number_of_combinations
                # now we have to pick a random one - a random item from each list is taken
                #print "Number of combinations: ",number_of_combinations
                if number_of_combinations > 0:
                    nodes_next = []
                    for elist in good_collection:
                        item = random.choice(elist)
                        nodes_next.append(item)
                    if printing:
                        print "OBD: ",OBdecomp
                        print "nodes next: ",nodes_next
                    copyforcandidate = copy.deepcopy(matched_list)
                    result = rec_fit_Furer_global(nodes_next,  D,  P,  OBdecomp,  i+1,  copyforcandidate,  nlimitlist,  nodes_observed_list,  Zlist_dict, iteration_counter,  epsilon,thread_number)
                    if result[1] != None:
                        matched_list = result[1]
                        X = X * result[0]
            ########### DEBUG 2015 change ########################################################################
        # and in any case return what you have received
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            temp_result=[X, matched_list]
            return [X, matched_list]
        else:
            if printing:
                print "No matching found"
            temp_result=[0,None]
            return [0, None]        
    else:   # because of border condition we never get here, it is all pretested..
        # search is over - report back
        #if we have full pattern report back a full matching list, otherwise an empty list
        OBd_flat = [item for sublist in OBdecomp for item in sublist]
        if len(matched_list) == len(OBd_flat):
            temp_result=[X, matched_list]
            return [X, matched_list]
        else:
            temp_result=[0,None]
            return [0, None]


def Furer_run_general(D,  P,  OBdecomp,  root_nodes,  nlimitlist):
    """
    OBdecomp : ordered bipartite decomposition on P, which is given. First element is list with a root node. # [ [2] , [1,3] , [4] , [5, 6] ]
    """
    global cqi
    global globalist_furer
    global globaltimes_furer
    globaltimes_furer = [time.time()]
    cqi = 0
    globalist_furer = []
    freq_dict={}    # dictionary with tuples of values as keys and frequency as value
    Zlist_dict = {}     # Furer will result in a list of estimations for each tuple -> average of this list must be taken as frequency
    # out of debug we do not use a list actually: an integer is kept for every tuple, and divided by number of iterations at the end
    number_of_targets = 0
    for node in P.nodes():
        if P.node[node]['target'] == True:
            number_of_targets += 1
    # number_of_targets holds the number of target nodes that we are after
    nodes_observed = 0
    iteration_counter = 0
    while nodes_observed <= max(nlimitlist):
        if nodes_observed > nlimitlist[cqi]:
            cqi = cqi +1    # we increase the index of position of quota to check upon
            total_Zlist_dict_copy = copy.deepcopy(Zlist_dict)
            handle_quota_Furer(D,  P, total_Zlist_dict_copy,  [0,None], iteration_counter)
            ##print "Call to Furer quota handling (main routine) at quota %d" % nlimitlist[cqi-1]
        iteration_counter = iteration_counter +1
        n = root_nodes[random.randrange(len(root_nodes))]
        nodes_observed = nodes_observed + 1
        list_for_spent = []
        list_for_spent.append(nodes_observed)
        result = rec_fit_Furer([n], D,  P,  OBdecomp,  0,  [],  nlimitlist,  list_for_spent,  Zlist_dict,  iteration_counter,  0)
        # list_for_spent gets passed by reference and number gets increased in recursions
        nodes_observed = list_for_spent[0]
        if result[1] != None:
            actualX = result[0] * len(root_nodes)
            mapping = result[1]     # this is mapping for OBdecomp FLAT.
            OBd_flat = [item for sublist in OBdecomp for item in sublist]
            target_values = []
            for i in range(len(OBd_flat)):
                if P.node[OBd_flat[i]]['target'] == True:
                    value_tuple = (P.node[OBd_flat[i]]['label'] , D.node[mapping[i]]['value'])
                    target_values.append(value_tuple)
            # now target_values contains all combinations of target nodes' label-value as tuples
            target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.
            if target_tuple in Zlist_dict:   # this checks for KEYS in Zlist_dict
                Zlist_dict[target_tuple] = Zlist_dict[target_tuple] + actualX
            else:
                Zlist_dict[target_tuple] = 0
                Zlist_dict[target_tuple] = Zlist_dict[target_tuple] + actualX
            # now also give zeros to all others...this is the correction of the "relaxed" version
            # this step not needed any more since we do not have lists anymore out of debug
    if (cqi < len(nlimitlist)) and (nodes_observed >= nlimitlist[cqi]):
        cqi = cqi +1    # we increase the index of position of quota to check upon
        total_Zlist_dict_copy = copy.deepcopy(Zlist_dict)
        handle_quota_Furer(D,  P, total_Zlist_dict_copy,  [0,None], iteration_counter)
        ##print "Call to Furer quota handling (main routine down) at quota %d" % nlimitlist[cqi-1]

    for k in Zlist_dict.keys():
        freq_dict[k] = (Zlist_dict[k])/float(iteration_counter)   # simply an average of a list
    # now with quota handler we just return global lists of freqdicts
    return [globalist_furer,  globaltimes_furer]




# predicate_match procedure is changed here, so that we also compare against values if they are part of the pattern
def predicate_match(x, y):
    if x['predicate'] == y['predicate']:
        if y['valueinpattern']==1:
            if not 'value' in x.keys():
                return False
            if x['value'] == y['value']:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def matches(n, D,  m,  P,  matched_list,  Plist):
    """
    n - node from dataset graph D to match with node m from pattern P
    matched_list - already matched nodes from D
    Plist - list of node IDs from P, which gives the ordering of finding the pattern
    """
    if predicate_match(D.node[n],  P.node[m]):
        test_list = matched_list + [n]
#        sgD = D.subgraph(test_list)
#        sgP = P.subgraph(Plist[:len(test_list)])    # we take as much from Plist as there is in test list
        neighbor_test = True
#        for m_neigh in sgP.neighbors(m):
        for m_neigh in P.neighbors(m):
            index_in_Plist = Plist.index(m_neigh)
            if index_in_Plist < len(test_list):
                image = test_list[index_in_Plist]   # this is m_neigh's corresponding image in D
                if image not in D.neighbors(n):
                    neighbor_test = False
        return neighbor_test
    else:
        return False 


def matches_Furer(n, D,  m,  P,  matched_list,  OBmatched):    
    global output_bug
    if predicate_match(D.node[n],  P.node[m]):
        #print "YES"  
        
        test_list = matched_list + [n]
        #print "--------------- TEST LIST: ------------------ "
        #for n in test_list:
        #  print D.node[n]
        #print "--------------- MATCHED LIST: ---------------- "
        #for k in matched_list:
        #      print D.node[k]
        compare_list = OBmatched+[m]
        #print "Compare list: ",OBmatched
        #print m
        
        if len(test_list) !=len(OBmatched+[m]): #hence, they should be of equal size and ready to be compared
          if not(os.path.exists(os.path.join(output_bug,"unequal_size.warning"))):
                with open(os.path.join(output_bug,"unequal_size.warning"),'w') as f:
                    f.write("Unequal size warning.")
                    f.close()
          
          
          #if not os.path.exists(os.path.join(experiments.globals.output_path,'warning_non_equal.info')):
                #with open(os.path.join(experiments.globals.output_path,'warning_non_equal.info'),'w') as f:
                # f.write("WARNING: you are comparing graphs of non-equal size in matches_Furer() !")
            
        neighbor_test = True
        for m_neigh in P.neighbors(m):
            if m_neigh in compare_list:
                index_in_Plist = compare_list.index(m_neigh)
                image = test_list[index_in_Plist]   # this is m_neigh's corresponding image in D
                if image not in D.neighbors(n):
                    neighbor_test = False
        return neighbor_test
    else:
        return False


    

def sampling_breadthsample_general(D,  P,  Plist,  root_nodes,  nlimit):
    """
    Takes a breadt-first sample of size nlimit from a random node in D and calls exhaustive on such a sample
    """
    n = root_nodes[random.randrange(len(root_nodes))]   # we start from a random root node
    # collect
    # make a nx.Graph out of them
    # call exhaustive on this smaller graph
    #BUT this is not comparable : sample != number of observations





def sampling_exhaustive_salsat(G,  satisfaction_nodes,  debug_mode='no'):
    """Function that exhaustively samples for 'salary satisfaction" in 'wife-friend' example (non-general function).
    We get a list of all 'satisfaction' nodes in a graph given. this is where we collect the value and then try to search for a pattern.
    If search for a pattern is successful, we update CPD, otherwise (in case of woman satisfaction, the procedure ends, and the satisfaction value gets discarded).
    More successful patterns on a single 'satisfaction' node are treated as separate examples."""
    freq_dict={}    # dictionary with tuples of values as keys and frequency as value: (my_salary_value, his_salary_value, my_satisfaction)
    good_roots = []
    for n in satisfaction_nodes:
        my_satisfaction_value = G.node[n]['value']
        num_man_neighbors = len([x for x in G.neighbors(n) if G.node[x]['predicate']=='man'])
        if num_man_neighbors<1:
            pass    # there are no 'man' nodes attached to this satisfaction, so, it is a woman's satisfaction - mismatch
        elif num_man_neighbors > 1:
            print "WARNING: more than one 'man' node attached to single 'satisfaction' node!"
        else:   # situation we aim for
            me = [x for x in G.neighbors(n) if G.node[x]['predicate']=='man'][0]    # initial 'man' node
            if debug_mode == 'yes': print "(debug): analysing man node " + str(me)
            # --- now, there also has to be a salary to continue the pattern...
            num_my_salary_neighbors = len([x for x in G.neighbors(me) if G.node[x]['predicate']=='salary'])
            if num_my_salary_neighbors < 1:
                pass    # I have no salary, so no comparison is possible, pattern mismatch
            elif num_my_salary_neighbors > 1:
                print "WARNING: 'man' node with many salaries - situation not considered!"
            else:   # pattern goes on
                if debug_mode == 'yes': print "(debug): " + str(me) + " has a salary, so we continue."
                my_salary_value = G.node[[x for x in G.neighbors(me) if G.node[x]['predicate']=='salary'][0]] ['value']
                # now there has to be marriage to continue the pattern...
                num_my_marriages = len([x for x in G.neighbors(me) if G.node[x]['predicate']=='married'])
                if num_my_marriages < 1:
                    pass    # not married, pattern mismatch
                elif num_my_marriages > 1:
                    print "WARNING: person married many times - situation not considered!"
                else:   #pattern goes on
                    if debug_mode == 'yes': print "(debug): " + str(me) + " is married, so we continue."
                    my_marriage = [x for x in G.neighbors(me) if G.node[x]['predicate']=='married'][0]
                    my_wife = [x for x in G.neighbors(my_marriage) if G.node[x]['predicate']=='woman'][0]
                    # now seek in all of her friends for patterns...
                    my_wifes_friendships = [x for x in G.neighbors(my_wife) if G.node[x]['predicate']=='friends']
                    my_wifes_friends = []
                    for wf in my_wifes_friendships:
                        friend = [x for x in G.neighbors(wf) if x != my_wife] [0]  # the friend argument that is not my wife - is her friend obviously
                        my_wifes_friends.append(friend)
                    my_wifes_girlfriends = [x for x in my_wifes_friends if G.node[x]['predicate']=='woman']
                    for wgf in my_wifes_girlfriends:     # pattern matching continues in all wife's girlfriends directions
                        if debug_mode == 'yes': print "(debug): analysing wgf " + str(wgf)
                        num_wgf_marriages = len([x for x in G.neighbors(wgf) if G.node[x]['predicate']=='married'])
                        if num_wgf_marriages < 1:
                            pass    # wife's girlfriend not married, pattern mismatch
                        elif num_wgf_marriages > 1:
                            print "WARNING: wgf maried many times - situation not considered!"
                        else:   # pattern goes on
                            if debug_mode == 'yes': print "(debug): " +str(wgf) + " is married so we continue."
                            wgf_marriage = [x for x in G.neighbors(wgf) if G.node[x]['predicate']=='married'][0]
                            wgf_husband = [x for x in G.neighbors(wgf_marriage) if G.node[x]['predicate']=='man'][0]
                            if debug_mode == 'yes': print "(debug): husband found " + str(wgf_husband)
                            num_wgf_husband_salaries = len([x for x in G.neighbors(wgf_husband) if G.node[x]['predicate']=='salary'])
                            if num_wgf_husband_salaries < 1:
                                pass    # no salary to compare (BTW: should we treat this as LOW??????????????????????)
                            elif num_wgf_husband_salaries > 1:
                                print "WARNING: he has many salaries - situation not considered!"
                            else:   # we are done
                                good_roots.append(n)
                                if debug_mode == 'yes': print "(debug): AND HE HAS A SALARY - PATTERN MATCH !"
                                his_salary = [x for x in G.neighbors(wgf_husband) if G.node[x]['predicate']=='salary'][0]
                                his_salary_value = G.node[his_salary]['value']
                                if (my_salary_value,  his_salary_value,  my_satisfaction_value) in freq_dict:
                                    freq_dict[(my_salary_value,  his_salary_value,  my_satisfaction_value)] += 1
                                else:
                                    freq_dict[(my_salary_value,  his_salary_value,  my_satisfaction_value)] = 1
    ##print "good roots were : %s" % str(good_roots)
    return freq_dict
    


def sampling_random_indexed_salsat(G,  satisfaction_nodes,  nsamples,  debug_mode='no'):
    """Function that exhaustively samples for 'salary satisfaction" in 'wife-friend' example (non-general function).
    We get a list of all 'satisfaction' nodes in a graph given. this is where we collect the value and then try to search for a pattern.
    If search for a pattern is successful, we update CPD, otherwise (in case of woman satisfaction, the procedure ends, and the satisfaction value gets discarded).
    More successful patterns on a single 'satisfaction' node are treated as separate examples."""
    freq_dict={}    # dictionary with tuples of values as keys and frequency as value: (my_salary_value, his_salary_value, my_satisfaction)
    nodes_sampled = 0
    while nodes_sampled <= nsamples:
        n = satisfaction_nodes[random.randrange(len(satisfaction_nodes))]
        nodes_sampled = nodes_sampled + 1
        my_satisfaction_value = G.node[n]['value']
        num_man_neighbors = len([x for x in G.neighbors(n) if G.node[x]['predicate']=='man'])
        nodes_sampled = nodes_sampled + len(G.neighbors(n))
        if num_man_neighbors<1:
            pass    # there are no 'man' nodes attached to this satisfaction, so, it is a woman's satisfaction - mismatch
        elif num_man_neighbors > 1:
            print "WARNING: more than one 'man' node attached to single 'satisfaction' node!"
        else:   # situation we aim for
            me = [x for x in G.neighbors(n) if G.node[x]['predicate']=='man'][0]    # initial 'man' node
            if debug_mode == 'yes': print "(debug): analysing man node " + str(me)
            # --- now, there also has to be a salary to continue the pattern...
            num_my_salary_neighbors = len([x for x in G.neighbors(me) if G.node[x]['predicate']=='salary'])
            nodes_sampled = nodes_sampled + len(G.neighbors(me))
            if num_my_salary_neighbors < 1:
                pass    # I have no salary, so no comparison is possible, pattern mismatch
            elif num_my_salary_neighbors > 1:
                print "WARNING: 'man' node with many salaries - situation not considered!"
            else:   # pattern goes on
                if debug_mode == 'yes': print "(debug): " + str(me) + " has a salary, so we continue."
                my_salary_value = G.node[[x for x in G.neighbors(me) if G.node[x]['predicate']=='salary'][0]] ['value']
                # now there has to be marriage to continue the pattern...
                num_my_marriages = len([x for x in G.neighbors(me) if G.node[x]['predicate']=='married'])
                if num_my_marriages < 1:
                    pass    # not married, pattern mismatch
                elif num_my_marriages > 1:
                    print "WARNING: person married many times - situation not considered!"
                else:   #pattern goes on
                    if debug_mode == 'yes': print "(debug): " + str(me) + " is married, so we continue."
                    my_marriage = [x for x in G.neighbors(me) if G.node[x]['predicate']=='married'][0]
                    my_wife = [x for x in G.neighbors(my_marriage) if G.node[x]['predicate']=='woman'][0]
                    nodes_sampled = nodes_sampled + 1
                    # now seek in all of her friends for patterns...
                    my_wifes_friendships = [x for x in G.neighbors(my_wife) if G.node[x]['predicate']=='friends']
                    nodes_sampled = nodes_sampled + len(G.neighbors(my_wife))
                    my_wifes_friends = []
                    for wf in my_wifes_friendships:
                        friend = [x for x in G.neighbors(wf) if x != my_wife] [0]  # the friend argument that is not my wife - is her friend obviously
                        nodes_sampled = nodes_sampled + 1
                        my_wifes_friends.append(friend)
                    my_wifes_girlfriends = [x for x in my_wifes_friends if G.node[x]['predicate']=='woman']
                    for wgf in my_wifes_girlfriends:     # pattern matching continues in all wife's girlfriends directions
                        if debug_mode == 'yes': print "(debug): analysing wgf " + str(wgf)
                        num_wgf_marriages = len([x for x in G.neighbors(wgf) if G.node[x]['predicate']=='married'])
                        nodes_sampled = nodes_sampled + len(G.neighbors(wgf))
                        if num_wgf_marriages < 1:
                            pass    # wife's girlfriend not married, pattern mismatch
                        elif num_wgf_marriages > 1:
                            print "WARNING: wgf maried many times - situation not considered!"
                        else:   # pattern goes on
                            if debug_mode == 'yes': print "(debug): " +str(wgf) + " is married so we continue."
                            wgf_marriage = [x for x in G.neighbors(wgf) if G.node[x]['predicate']=='married'][0]
                            wgf_husband = [x for x in G.neighbors(wgf_marriage) if G.node[x]['predicate']=='man'][0]
                            nodes_sampled = nodes_sampled + 1
                            if debug_mode == 'yes': print "(debug): husband found " + str(wgf_husband)
                            num_wgf_husband_salaries = len([x for x in G.neighbors(wgf_husband) if G.node[x]['predicate']=='salary'])
                            nodes_sampled = nodes_sampled + len(G.neighbors(wgf_husband))
                            if num_wgf_husband_salaries < 1:
                                pass    # no salary to compare (BTW: should we treat this as LOW??????????????????????)
                            elif num_wgf_husband_salaries > 1:
                                print "WARNING: he has many salaries - situation not considered!"
                            else:   # we are done
                                if debug_mode == 'yes': print "(debug): AND HE HAS A SALARY - PATTERN MATCH !"
                                his_salary = [x for x in G.neighbors(wgf_husband) if G.node[x]['predicate']=='salary'][0]
                                his_salary_value = G.node[his_salary]['value']
                                if (my_salary_value,  his_salary_value,  my_satisfaction_value) in freq_dict:
                                    freq_dict[(my_salary_value,  his_salary_value,  my_satisfaction_value)] += 1
                                else:
                                    freq_dict[(my_salary_value,  his_salary_value,  my_satisfaction_value)] = 1
    return freq_dict






def Furer_once(G,  rand_grade,  rand_intel,  rand_dif):
    X = 1       # initialization like in the paper, although a mock-up one here
    Z = None
    # a loop over decomposition should follow, but we only have 2 items for our case
    # first step is on the whole graph:
    right_grade_nodes = []
    for n in G.nodes():
        if (G.node[n]['predicate'] =='grade') and (G.node[n]['value'] == rand_grade):
            right_grade_nodes.append(n)
    X = X * len(right_grade_nodes)
    random_GH = random.choice(right_grade_nodes)
    # second step - embed the second decomposition part
    # in our case, just check whether it is the correct parents or not
    for pred in G.predecessors(random_GH):      # we collect its predeccessors (intelligence and difficulty)
        if 'intelligence(' in pred:
            intelligence_node_value = G.node[pred]['value']
        elif 'difficulty(' in pred:
            difficulty_node_value = G.node[pred]['value']
        else:
            print "ERROR : node GRADE has strange predecessors!!!"
    if ((intelligence_node_value == rand_intel) and (difficulty_node_value == rand_dif)):
        X = X * 1   # the only embedding there can be
        Z = X
    else:
        Z = 0
    return Z
    
    
def Furer_run(G,  nsamples):
    """Furer algorithm for sampling 'grade'. """
    freq_dict = {}      # dictionary with tuples of values as keys and frequency as value
    Zlist_dict = {}     # Furer will result in a list of estimations for each tuple -> average of this list must be taken as frequency
    num_nodes_visited = 0
    # TAKOLE bom naredu: v vsaki iteraciji bom izbral nakljucni triplet vrednosti, zalaufal na njem Furerja in pobral od njega frekvenco v freq_dict
    # Furer si bo sicer vsakic sproti zgradil indeks, ki ga rabi, kar je totalno neucinkovito, ampak dokler ne merimo casa je OK
    for i in range(nsamples):
        rand_grade = random.choice(['low',  'mid', 'high'])
        rand_intel = random.choice(['low', 'high'])
        rand_dif = random.choice(['low',  'mid', 'high'])
        if (rand_intel,  rand_dif,  rand_grade) in Zlist_dict:
            Zlist_dict[(rand_intel,  rand_dif,  rand_grade)].append(Furer_once(G,  rand_grade,  rand_intel,  rand_dif))
        else:
            Zlist_dict[(rand_intel,  rand_dif,  rand_grade)] = []
            Zlist_dict[(rand_intel,  rand_dif,  rand_grade)].append(Furer_once(G,  rand_grade,  rand_intel,  rand_dif))
    # ZDAJLE pa JE TREBA iz Zlist_dict pridelati freq_dict, da ga lahko vrnemo
    for k in Zlist_dict.keys():
        freq_dict[k] = sum(Zlist_dict[k])/float(len(Zlist_dict[k]))   # simply an average of a list
    return freq_dict
    
    
    
    
def Furer_try(G,  grade_value,  error=0.1):
    """Test function to try Furer for a specific grade value"""
    print "-----Furer try-test function-----"
    repetitions = int(math.pow(error,  -2))
    Z_list = []
    Z_sum = 0
    for i in range(repetitions):
        Zi = Furer_once(G,  grade_value)
        Z_list.append(Zi)
        Z_sum = Z_sum + Zi
    print "Z_list :" + str(Z_list)
    print "Embeddings estimation for grade_value /" + str(grade_value) + "/ :" + str(Z_sum/repetitions)


    
def Furer_once_satisfaction(G,  satisfaction_nodes_list,  rand_satisfaction,  rand_mysalary,  rand_hissalary):
    X = 1       # initialization like in the paper
    Z = 0
    number_nodes_visited = 0    # we keep a count of those and report them for each iteration
    # a loop over decomposition follows - but here I just make 9 iterative steps for specific decomposition (make it general sometime...)
    # first step is on the whole graph - or like here, on the whole list of satisfaction nodes (even values could be indexed...so we do not count these into nodes visited)
    right_satisfaction_nodes = []
    for n in satisfaction_nodes_list:
        if (G.node[n]['value'] == rand_satisfaction):
            right_satisfaction_nodes.append(n)
    X = X * len(right_satisfaction_nodes)
    random_SN = random.choice(right_satisfaction_nodes)
    number_nodes_visited = number_nodes_visited + 1
    # second step - try to embed the second decomposition part: the _me_ 'man' node
    man_neighbors = [x for x in G.neighbors(random_SN) if G.node[x]['predicate']=='man']
    number_nodes_visited = number_nodes_visited + len(G.neighbors(random_SN))
    if len(man_neighbors) < 1:  # if there is no such neighbor - therefore no such an embedding
        Z = 0
    else:   # in case there is an embedding or more of them
        random_MN = random.choice(man_neighbors)
        X = X * len(man_neighbors)
        # third step - try to embed third decomposition part: 'salary' and 'married' out of 'man'
        # Since 'salary' it is a value-holding node, we check also for value embedding
        my_right_salary_neighbors = [x for x in G.neighbors(random_MN) if ((G.node[x]['predicate']=='salary') and (G.node[x]['value']==rand_mysalary))]
        number_nodes_visited = number_nodes_visited + len(G.neighbors(random_MN))
        my_married_neighbors = [x for x in G.neighbors(random_MN) if G.node[x]['predicate']=='married']
        if len(my_right_salary_neighbors) < 1: # no embedding, either no salary, or wrong value of it
            Z = 0
        elif len(my_married_neighbors) < 1: # no embedding
            Z = 0
        else:
            # we pick one of each of them
            random_MRSN = random.choice(my_right_salary_neighbors)  # redundant here, as we do not continue in that branch, but for generality...
            random_MMN = random.choice(my_married_neighbors)
            X = X * len(my_right_salary_neighbors) * len(my_married_neighbors)  # all possible combinations of the two count in general, although here we know there is only one, as not multiple salaries or marriages exist.
            # fourth step - try to embed fourth decomposition part: 'woman' node that follows 'married'
            my_wife_neighbors = [x for x in G.neighbors(random_MMN) if G.node[x]['predicate']=='woman']
            number_nodes_visited = number_nodes_visited + len(G.neighbors(random_MMN))
            if len(my_wife_neighbors) < 1:  #no woman attached to married, no embedding
                Z = 0
            else:
                # we pick random woman of the married ones (currently can only be one)
                random_WN = random.choice(my_wife_neighbors)
                X = X * len(my_wife_neighbors)
                # fifth step - try to embed fifth decomposition part: 'friends' node that follows 'woman'
                wifes_friends_neighbors = [x for x in G.neighbors(random_WN) if G.node[x]['predicate']=='friends']
                number_nodes_visited = number_nodes_visited + len(G.neighbors(random_WN))
                if len(wifes_friends_neighbors) < 1:    #no friends of hers, no embedding
                    Z = 0
                else:
                    # we pick a random friend (might also be a man-friend, we cannot know)
                    random_FN = random.choice(wifes_friends_neighbors)
                    X = X * len(wifes_friends_neighbors)    # here it really is multiplying by something greater than 1 usually
                    # sixth step - try to embed sixth decomposition part: 'woman' on the other side of the 'friends' node
                    # (BEWARE: here we must not allow to get woman to be a friend of herself! From 'friends' we must ensure not to return back to first 'woman' node)
                    woman_friends = [x for x in G.neighbors(random_FN) if ((G.node[x]['predicate']=='woman') and (x != random_WN))]
                    number_nodes_visited = number_nodes_visited + len(G.neighbors(random_FN))
                    if len(woman_friends) < 1:  # not a female friend, no embedding
                        Z = 0
                    else:
                        # we pick a random woman (GirlFriend) and continue
                        random_GFN = random.choice(woman_friends)
                        X = X * len(woman_friends)
                        # seventh step - try to embed seventh decomposition part: 'married' continuation of the GF
                        girlfriends_married_neighbors = [x for x in G.neighbors(random_GFN) if G.node[x]['predicate']=='married']
                        number_nodes_visited = number_nodes_visited + len(G.neighbors(random_GFN))
                        if len(girlfriends_married_neighbors) < 1:  #girlfriend not married, no embedding
                            Z = 0
                        else:
                            # we pick a random one
                            random_GFMN = random.choice(girlfriends_married_neighbors)
                            X = X * len(girlfriends_married_neighbors)
                            # eight step - try to embed eighth decomposition step: 'man' node , so the husband
                            husband_neighbors = [x for x in G.neighbors(random_GFMN) if G.node[x]['predicate']=='man']
                            number_nodes_visited = number_nodes_visited + len(G.neighbors(random_GFMN))
                            if len(husband_neighbors) < 1:  # no husband, no embedding
                                Z = 0
                            else:
                                # we pick a random husband
                                random_HN = random.choice(husband_neighbors)
                                X = X * len(husband_neighbors)
                                # ninth step - try to embed 'salary', and also we check for its value at the same time
                                husband_right_salary_neighbors = [x for x in G.neighbors(random_HN) if ((G.node[x]['predicate']=='salary') and (G.node[x]['value']==rand_hissalary))]
                                number_nodes_visited = number_nodes_visited + len(G.neighbors(random_HN))
                                if len(husband_right_salary_neighbors) < 1: # no salary or not the right value
                                    Z = 0
                                else:
                                    # no random pick any more as we are finished
                                    X = X * len(husband_right_salary_neighbors)
                                    Z = X
    return [Z,  number_nodes_visited]





def Furer_run_satisfaction(G,  satisfaction_nodes_list,  nsamples):
    """Furer algorithm for sampling 'satisfaction'. """
    freq_dict = {}      # dictionary with tuples of values as keys and frequency as value
    Zlist_dict = {}     # Furer will result in a list of estimations for each tuple -> average of this list must be taken as frequency
    num_nodes_visited = 0
    # TAKOLE bom naredu: v vsaki iteraciji bom izbral nakljucni triplet vrednosti, zalaufal na njem Furerja in pobral od njega frekvenco v freq_dict
    # Furer si bo sicer vsakic sproti zgradil indeks, ki ga rabi, kar je totalno neucinkovito, ampak dokler ne merimo casa je OK
    while (num_nodes_visited < nsamples):
        rand_satisfaction = random.choice(['low',  'mid', 'high'])
        rand_mysalary = random.choice(['low',  'mid', 'high'])
        rand_hissalary = random.choice(['low',  'mid', 'high'])
        Furer_result = Furer_once_satisfaction(G,  satisfaction_nodes_list,  rand_satisfaction,  rand_mysalary,  rand_hissalary)    # a list: [Z, num_nodes_visited]
        if (rand_mysalary,  rand_hissalary,  rand_satisfaction) in Zlist_dict:
            Zlist_dict[(rand_mysalary,  rand_hissalary,  rand_satisfaction)].append(Furer_result[0])
        else:
            Zlist_dict[(rand_mysalary,  rand_hissalary,  rand_satisfaction)] = []
            Zlist_dict[(rand_mysalary,  rand_hissalary,  rand_satisfaction)].append(Furer_result[0])
        num_nodes_visited = num_nodes_visited + Furer_result[1]
    # ZDAJLE pa JE TREBA iz Zlist_dict pridelati freq_dict, da ga lahko vrnemo
    for k in Zlist_dict.keys():
        freq_dict[k] = sum(Zlist_dict[k])/float(len(Zlist_dict[k]))   # simply an average of a list
    return freq_dict
    



def Furer_once_satisfaction_relaxed(G,  satisfaction_nodes_list):
    """similar, but this checks for any comination of values in a matching pattern of nodes
    - so no random triplets are needed as input and are also not checked for correctness
    - and additional output item is added: the combination of values that succeeded, otherwise None"""
    freq_dict={}    # the relaxed version seeks for a pattern with any combination of values - like the random node approach
    matched_combination = None
    X = 1       # initialization like in the paper
    Z = 0
    number_nodes_visited = 0    # we keep a count of those and report them for each iteration
    # a loop over decomposition follows - but here I just make 9 iterative steps for specific decomposition (make it general sometime...)
    # first step is on the whole graph - or like here, on the whole list of satisfaction nodes (even values could be indexed...so we do not count these into nodes visited)
    X = X * len(satisfaction_nodes_list)
    random_SN = random.choice(satisfaction_nodes_list)
    number_nodes_visited = number_nodes_visited + 1
    my_satisfaction = G.node[random_SN]['value']
    # second step - try to embed the second decomposition part: the _me_ 'man' node
    man_neighbors = [x for x in G.neighbors(random_SN) if G.node[x]['predicate']=='man']
    number_nodes_visited = number_nodes_visited + len(G.neighbors(random_SN))
    if len(man_neighbors) < 1:  # if there is no such neighbor - therefore no such an embedding
        Z = 0
    else:   # in case there is an embedding or more of them
        random_MN = random.choice(man_neighbors)
        X = X * len(man_neighbors)
        # third step - try to embed third decomposition part: 'salary' and 'married' out of 'man'
        # Since 'salary' it is a value-holding node, we check also for value embedding
        my_right_salary_neighbors = [x for x in G.neighbors(random_MN) if (G.node[x]['predicate']=='salary')]
        number_nodes_visited = number_nodes_visited + len(G.neighbors(random_MN))
        my_married_neighbors = [x for x in G.neighbors(random_MN) if G.node[x]['predicate']=='married']
        if len(my_right_salary_neighbors) < 1: # no embedding, either no salary, or wrong value of it
            Z = 0
        elif len(my_married_neighbors) < 1: # no embedding
            Z = 0
        else:
            my_salary = G.node[my_right_salary_neighbors[0]]['value']
            # we pick one of each of them
            random_MRSN = random.choice(my_right_salary_neighbors)  # redundant here, as we do not continue in that branch, but for generality...
            random_MMN = random.choice(my_married_neighbors)
            X = X * len(my_right_salary_neighbors) * len(my_married_neighbors)  # all possible combinations of the two count in general, although here we know there is only one, as not multiple salaries or marriages exist.
            # fourth step - try to embed fourth decomposition part: 'woman' node that follows 'married'
            my_wife_neighbors = [x for x in G.neighbors(random_MMN) if G.node[x]['predicate']=='woman']
            number_nodes_visited = number_nodes_visited + len(G.neighbors(random_MMN))
            if len(my_wife_neighbors) < 1:  #no woman attached to married, no embedding
                Z = 0
            else:
                # we pick random woman of the married ones (currently can only be one)
                random_WN = random.choice(my_wife_neighbors)
                X = X * len(my_wife_neighbors)
                # fifth step - try to embed fifth decomposition part: 'friends' node that follows 'woman'
                wifes_friends_neighbors = [x for x in G.neighbors(random_WN) if G.node[x]['predicate']=='friends']
                number_nodes_visited = number_nodes_visited + len(G.neighbors(random_WN))
                if len(wifes_friends_neighbors) < 1:    #no friends of hers, no embedding
                    Z = 0
                else:
                    # we pick a random friend (might also be a man-friend, we cannot know)
                    random_FN = random.choice(wifes_friends_neighbors)
                    X = X * len(wifes_friends_neighbors)    # here it really is multiplying by something greater than 1 usually
                    # sixth step - try to embed sixth decomposition part: 'woman' on the other side of the 'friends' node
                    # (BEWARE: here we must not allow to get woman to be a friend of herself! From 'friends' we must ensure not to return back to first 'woman' node)
                    woman_friends = [x for x in G.neighbors(random_FN) if ((G.node[x]['predicate']=='woman') and (x != random_WN))]
                    number_nodes_visited = number_nodes_visited + len(G.neighbors(random_FN))
                    if len(woman_friends) < 1:  # not a female friend, no embedding
                        Z = 0
                    else:
                        # we pick a random woman (GirlFriend) and continue
                        random_GFN = random.choice(woman_friends)
                        X = X * len(woman_friends)
                        # seventh step - try to embed seventh decomposition part: 'married' continuation of the GF
                        girlfriends_married_neighbors = [x for x in G.neighbors(random_GFN) if G.node[x]['predicate']=='married']
                        number_nodes_visited = number_nodes_visited + len(G.neighbors(random_GFN))
                        if len(girlfriends_married_neighbors) < 1:  #girlfriend not married, no embedding
                            Z = 0
                        else:
                            # we pick a random one
                            random_GFMN = random.choice(girlfriends_married_neighbors)
                            X = X * len(girlfriends_married_neighbors)
                            # eight step - try to embed eighth decomposition step: 'man' node , so the husband
                            husband_neighbors = [x for x in G.neighbors(random_GFMN) if G.node[x]['predicate']=='man']
                            number_nodes_visited = number_nodes_visited + len(G.neighbors(random_GFMN))
                            if len(husband_neighbors) < 1:  # no husband, no embedding
                                Z = 0
                            else:
                                # we pick a random husband
                                random_HN = random.choice(husband_neighbors)
                                X = X * len(husband_neighbors)
                                # ninth step - try to embed 'salary', and also we check for its value at the same time
                                husband_right_salary_neighbors = [x for x in G.neighbors(random_HN) if (G.node[x]['predicate']=='salary')]
                                number_nodes_visited = number_nodes_visited + len(G.neighbors(random_HN))
                                if len(husband_right_salary_neighbors) < 1: # no salary or not the right value
                                    Z = 0
                                else:
                                    his_salary = G.node[husband_right_salary_neighbors[0]]['value']
                                    # no random pick any more as we are finished
                                    X = X * len(husband_right_salary_neighbors)
                                    Z = X
                                    matched_combination = (my_salary,  his_salary, my_satisfaction)
    return [Z,  number_nodes_visited,  matched_combination]





def Furer_run_satisfaction_relaxed(G,  satisfaction_nodes_list,  nsamples):
    """Furer algorithm for sampling 'satisfaction'. """
    freq_dict = {}      # dictionary with tuples of values as keys and frequency as value
    Zlist_dict = {}     # Furer will result in a list of estimations for each tuple -> average of this list must be taken as frequency
    num_nodes_visited = 0
    while (num_nodes_visited < nsamples):
        Furer_result = Furer_once_satisfaction_relaxed(G,  satisfaction_nodes_list)    # a list: [Z, num_nodes_visited, matched_combination]
        if Furer_result[2] != None:
            if Furer_result[2] in Zlist_dict:   # this checks for KEYS in Zlist_dict
                Zlist_dict[Furer_result[2]].append(Furer_result[0])
            else:
                Zlist_dict[Furer_result[2]] = []
                Zlist_dict[Furer_result[2]].append(Furer_result[0])
            # now also give zeros to all others...this is the correction of the "relaxed" version
            for key in Zlist_dict:
                if key != Furer_result[2]:
                    Zlist_dict[key].append(0)
        else:
            # in this case give zeros to all...this is the correction of the "relaxed" version
            for key in Zlist_dict:
                    Zlist_dict[key].append(0)
        num_nodes_visited = num_nodes_visited + Furer_result[1]     # number of nodes increases regardless whether there was success or not of course
    # ZDAJLE pa JE TREBA iz Zlist_dict pridelati freq_dict, da ga lahko vrnemo
    for k in Zlist_dict.keys():
        freq_dict[k] = sum(Zlist_dict[k])/float(len(Zlist_dict[k]))   # simply an average of a list
    return freq_dict






##-------MAIN part of the script---------
"""
#D = nx.read_gml("satisfaction_toy_example2.gml")
start = time.time()            # wall-clock time in seconds
D = nx.read_gml("satisfaction_100k_highM.gml")
stop = time.time()            # wall-clock time in seconds
print "Reading satisfaction_100k_highM.gml took " + str(stop-start) + " seconds."
P = nx.read_gml("satisfaction_pattern.gml")
Plist = [2, 3,1,4,5,6,7,8,9,10,11]
OBdecomp = [ [2], [3] , [1, 4], [5], [6], [7], [8], [9], [10] ]
root_nodes = [x for x in D.nodes() if D.node[x]['predicate']=='satisfaction']

start_time = time.time()            # wall-clock time in seconds
fdict_exhaustive = sampling_exhaustive_general2(D,  P,  Plist,  root_nodes)
mean_time0 = time.time()
report_time0 = mean_time0 - start_time

NLIMIT = 100000

print str(fdict_exhaustive)
print "-----true is:-----"
print str(sampling_exhaustive_salsat(D,  root_nodes))
print "-----node limited is:-----"
start_time = time.time()            # wall-clock time in seconds
fdict_limited = sampling_randomnode_general(D,  P,  Plist,  root_nodes,  NLIMIT)
mean_time1 = time.time()
report_time1 = mean_time1 - start_time
print str(fdict_limited)
##rec_fit2(101, D, P, Plist, 0, [])
##print "and now one FURER, just to try:"
##print str(rec_fit_Furer([101], D, P, OBdecomp, 0, [], 1000, [0]))

print "now the whole Furer..."
start_time = time.time()            # wall-clock time in seconds
fdict_Furer = Furer_run_general(D, P , OBdecomp, root_nodes, NLIMIT)
mean_time2 = time.time()
report_time2 = mean_time2 - start_time
print str(fdict_Furer)

print "######## now the distributions #########"
pde = make_pd_general(fdict_exhaustive)
pdl = make_pd_general(fdict_limited)
pdf = make_pd_general(fdict_Furer)

for k in pde.keys():
    print str(k) + " : " + str(pde[k])
    print str(k) + " : " + str(pdl[k])
    print str(k) + " : " + str(pdf[k])
    print "--------------next triplet--------------"

print "Exhaustive approach took %s seconds." % str(report_time0)
print "With %s nodes observation limit, the random node approach took %s seconds and Furer took %s seconds." % (str(NLIMIT),  str(report_time1),  str(report_time2))

print "Average Hellinger of random node is: %s" % (str(su.avg_hellinger(transform_to_ptable(pde), transform_to_ptable(pdl))))
print "Average Hellinger of Furer algo. is: %s" % (str(su.avg_hellinger(transform_to_ptable(pde), transform_to_ptable(pdf))))


"""


#start_time = time.time()            # wall-clock time in seconds
#G = give_me_friends_graph(100000,  100000)
#satisfaction_nodes = [x for x in G.nodes() if G.node[x]['predicate']=='satisfaction']
#stop_time = time.time()
#print "graph construction took " + str(stop_time-start_time) + " seconds."
#print " "
#print "#--------report started"
#print "Graph contains " +str(len(G.nodes())) + " nodes."
#
#start_time = time.time()            # wall-clock time in seconds
#freq = sampling_exhaustive_salsat(G,  satisfaction_nodes)
#mean_time1 = time.time()
#report_time1 = mean_time1 - start_time
#
#prob_dist = make_pd(make_fd(freq))
#
#NSAMPLES = 200000
#mean_time1 = time.time()    # to reset mean_time1 
#freq2 = sampling_random_indexed_salsat(G,  satisfaction_nodes,  NSAMPLES)
#mean_time2 = time.time()
#report_time2 = mean_time2 - mean_time1
#prob_dist2 = make_pd(make_fd(freq2))
#
#mean_time2 = time.time()    # to reset mean_time2 
#freq3 = Furer_run_satisfaction(G,  satisfaction_nodes,  NSAMPLES)
#mean_time3 = time.time()
#report_time3 = mean_time3 - mean_time2
#prob_dist3 = make_pd(make_fd(freq3))
#
#
#mean_time3 = time.time()    # to reset mean_time2 
#freq4 = Furer_run_satisfaction_relaxed(G,  satisfaction_nodes,  NSAMPLES)
#mean_time4 = time.time()
#report_time4 = mean_time4 - mean_time3
#prob_dist4 = make_pd(make_fd(freq4))
#
#
#print "Exhaustive approach took "+ str(report_time1) + " seconds and achieved average Hellinger of: " + str(su.avg_hellinger(prob_dist,  prob_dist))
#print "Random indexed on " + str(NSAMPLES)+ " nodes took "+ str(report_time2) + " seconds and achieved average Hellinger of: " + str(su.avg_hellinger(prob_dist,  prob_dist2))
#print "Strict indexed Furer on " + str(NSAMPLES)+ " nodes took "+ str(report_time3) + " seconds and achieved average Hellinger of: " + str(su.avg_hellinger(prob_dist,  prob_dist3))
#print "Relaxed indexed Furer on " + str(NSAMPLES)+ " nodes took "+ str(report_time4) + " seconds and achieved average Hellinger of: " + str(su.avg_hellinger(prob_dist,  prob_dist4))
#print " "
#print "Probability distribution by exhaustive approach (correct):"
#print prob_dist
#print "Probability distribution by random indexed (NSAMPLES=" +str(NSAMPLES)+"):"
#print prob_dist2
#print "Probability distribution by strict Furer (NSAMPLES=" +str(NSAMPLES)+"):"
#print prob_dist3
#print "#--------report finished."
#print " "
#
###start_time = time.time()
####-------OUTPUT to the GML format---------
###gmlfile = open('gml_sal_sat_temp.gml',  'w')
###gmlfile.write('graph [ directed 0 \n')
###
###for n in G.nodes():
###    if 'value' in G.node[n].keys():
###        stringtowrite = 'node [ id ' + str(G.node[n]['id']) + ' label "' + str(n) + '=' + str(G.node[n]['value']) + '" ]\n'
###    else:
###        stringtowrite = 'node [ id ' + str(G.node[n]['id']) + ' label "' + str(n)  + '" ]\n'
###    gmlfile.write(stringtowrite)
###
#####edge [ source 1 target 2 ]
###for e in G.edges():
###    sourcename = e[0]
###    targetname = e[1]
###    stringtowrite = 'edge [ source ' + str(G.node[sourcename]['id']) + ' target ' + str(G.node[targetname]['id']) + ' ]\n'
###    gmlfile.write(stringtowrite)
###
###gmlfile.write(']')
###gmlfile.close()
###
###stop_time = time.time()
###print "outputting the graph into GML format took " + str(stop_time-start_time) + " seconds."
