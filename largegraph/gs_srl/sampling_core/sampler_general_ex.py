
import copy
import itertools
import os
import random
import time
import approaches.globals_sampling
import functools

globalist_randomnode = []
globalist_furer = []
cqi = 0     #index of nlimitlist - the current quota to check for
globaltimes_randomnode = []     # first element is actual start time, others are timings for each quota reached
globaltimes_furer = []
temp_result=[]
nodes_observed=[]
output_bug=None



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


def complete_combinations_1(fdict, D, P, Plist):
    """completes the combinations in fdict, so that it contains also all the zeros in combinations that were not even found in the graph (needed for correct and fair smoothing)
    - value_tuples_list is a list of lists: each list contains all the possible value values of one target variable : ORDER MUST BE like in Plist, since this is how fdict's tuples are made.
    one value tuple is (label, value), so this is how they must be prepared for input. """
    import itertools
    count = 0
    value_tuples_list = []
    choose_subset = False
    values_for_head = []
    target_predicates = []
    head_predicate = None
    all_possible_target_tuples = None
    values_for_target_predicates = {}
    counts_for_head_occurence = {}

    target = 0
    for i in range(len(Plist)):
        if P.node[Plist[i]]['target'] == 1:
            target += 1
            count += 1
            part1 = P.node[Plist[i]]['label']  # first part of the value tuple is the label
            predicate1 = P.node[Plist[i]]['predicate']
            if target == 1:
                head_predicate = predicate1

            target_predicates.append(predicate1)
            # then all possible values get collected from D
            s = set()  # set of all possible values found in D for such a node
            for n in D.nodes():
                if D.node[n]['predicate'] == predicate1:
                    value = D.node[n]['value']
                    if target == 1:
                        values_for_head.append((predicate1, value))
                        values_for_head.append((predicate1, "false"))
                        head_predicate = predicate1
                    s.add(value)
                    s.add("false")
            values_for_target_predicates[predicate1] = s
            value_tuples_list.append(list(itertools.product([part1], list(
                s))))  # returns a list of tuples that are combinations of the label, and all possible value from the set
    # here value_tuples_list should be a list of lists: each variable in a combination has a list of its value tuples
    nr_possible_values_target = get_number_of_possible_value_combinations(head_predicate, target_predicates,
                                                                          values_for_target_predicates)
    nr_possible_values_target_no_head = get_number_of_possible_value_combinations_excluding_head_predicate(
        head_predicate, target_predicates, values_for_target_predicates)
    approaches.globals_sampling.nr_target_nodes_no_head = nr_possible_values_target_no_head

    for value in values_for_target_predicates[head_predicate]:
        counts_for_head_occurence[(head_predicate, value)] = nr_possible_values_target
    # all_possible_target_tuples = list(itertools.product(*value_tuples_list))       # we get a list of all possible target tuples (* just unpacks values_list into individual list, since this is what itertools expect)
    # print len(all_possible_target_tuples)
    set_of_values_for_head = set(values_for_head)
    approaches.globals_sampling.nr_values_for_head = len(set_of_values_for_head)
    approaches.globals_sampling.all_possible_target_combinations = []
    approaches.globals_sampling.valueTuples = set(set_of_values_for_head)
    counter_not_found_targets = 0
    if len(fdict) == 0 or len(target_predicates) == 1 or nr_possible_values_target > len(fdict):
        default_key = []
        if (len(fdict.keys()) > 0):
            akey = fdict.keys()[0]
        else:
            akey = ['dummy']
        for j in range(len(akey)):
            default_key.append(('default', 'default'))
        default_key = tuple(default_key)
        fdict[default_key] = []
        fdict[default_key] = -1
        for tt in fdict.keys():
            new_key = tt
            if len(target_predicates):
                new_key = tt[0]
            if new_key in counts_for_head_occurence.keys():
                counts_for_head_occurence[(new_key[0], new_key[1])] = counts_for_head_occurence[
                                                                          (new_key[0], new_key[1])] - 1
                approaches.globals_sampling.count_of_combination_values_for_head = counts_for_head_occurence

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
                 key=k[1:]
                 if key!=():
                   fd[key]=[]
                 if not key in fd.keys():
                     fd[key]=[]
                 counter=0
                 for headValue in approaches.globals_sampling.count_of_combination_values_for_head.keys():
                    if key==():
                        if approaches.globals_sampling.count_of_combination_values_for_head[headValue]==0:
                            continue
                    fd[key].append([headValue, approaches.globals_sampling.count_of_combination_values_for_head[headValue]])
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
        for value_tuple in approaches.globals_sampling.valueTuples:
                if not value_in_tuple_list(value_tuple[1],headValuesAdded):
                  headValuesAdded.append(value_tuple)
                  if approaches.globals_sampling.report== "furer":
                      fd[k].append([value_tuple, 1 / float(approaches.globals_sampling.nr_iterations)])
                  else:    
                      fd[k].append([value_tuple,  1])
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
                 
                 for headValue in approaches.globals_sampling.count_of_combination_values_for_head.keys():
                    if key==():
                        if approaches.globals_sampling.count_of_combination_values_for_head[headValue]==0:
                            continue 
                    #if approaches.globals.current_time_snapshot==15:
                    #    print "Appending: ",[headValue,approaches.globals.count_of_combination_values_for_head[headValue]]
                    fd[key].append([headValue, approaches.globals_sampling.count_of_combination_values_for_head[headValue]])
        else:    
                if k[1:]==() and k[1:] in fd.keys():
                    fd[k[1:]].append([k[0],  fdict[k]+1])
                    continue
                if not k[1:] in fd.keys():  
                    fd[k[1:]] = [[k[0],  fdict[k]+1]]
                else:
                    fd[k[1:]].append([k[0],  fdict[k]+1])
    #Add other head values
    for k in fd.keys():   
        headValuesAdded=[]
        for i in fd[k]:
            headValuesAdded.append(i[0])
        for value_tuple in approaches.globals_sampling.valueTuples:
                if not value_in_tuple_list(value_tuple[1],headValuesAdded):
                  headValuesAdded.append(value_tuple)
                  fd[k].append([value_tuple, approaches.globals_sampling.nr_iterations])
    return fd

def make_fd_general_my_version_exhaustive_1(fdict):
    fd = {}
    for k in fdict.keys():
        if(fdict[k]==-1):
                 key=k[1:]
                 if key!=():
                   fd[key]=[]
                 else:
                    continue
                 for headValue in approaches.globals_sampling.count_of_combination_values_for_head.keys():
                    if key==():
                        if approaches.globals_sampling.count_of_combination_values_for_head[headValue]==0:
                            continue 
                    fd[key].append([headValue, approaches.globals_sampling.count_of_combination_values_for_head[headValue]])
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
        for value_tuple in approaches.globals_sampling.valueTuples:
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
        ksum = 0
        for el in fd[k]:    # the value of fd dict. - the list like : [[(u'satisfaction(m)', u'low'), 66], [(u'satisfaction(m)', u'mid'), 26], [(u'satisfaction(m)', u'high'), 66]]
            ksum = ksum + el[1]
        # now the normalization change
        for el in fd[k]:
            el[1] = el[1] / float(ksum)
    return [fd,  trash,  default_key]




def make_pd_general_kickout_default_my_version(fdict):
    """this one gathers in a default combination all rows/combinations that do not gather in frequencies more than 1% of all embeddings
    trash_factor gives the threshold for removal: default is 0.01, which means threshold of 1%"""
    num_embeddings = 0
    for k in fdict.keys():
        num_embeddings = num_embeddings + fdict[k]  # I remove +1 added by Laplace smoothing BEWARE: previous Laplace smoothing assumed
    if(approaches.globals_sampling.report== "furer"):
      fd = make_fd_general_my_version_exhaustive_1(fdict)
    else:
      fd = make_fd_general_my_version_exhaustive_1(fdict)
    trash = []
    # creation of the default key of the same size as other keys, but all values 'default'
    default_key = []
    akey = fd.keys()[0]
    for j in range(len(akey)):
        default_key.append(('default', 'default'))
    default_key = tuple(default_key)
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
    if approaches.globals_sampling.report== "furer":
       fd = make_fd_general_my_version(fdict)
    else:
       fd = make_fd_general_my_version(fdict)
    # now we normalize the remaining keys for each key - its list with values
    counter=0
    ksum_unconstrained=0
    for k in fd.keys():     # so, for each combination/row:   
        ksum = 0
        for el in fd[k]:    # the value of fd dict. - the list like : [[(u'satisfaction(m)', u'low'), 66], [(u'satisfaction(m)', u'mid'), 26], [(u'satisfaction(m)', u'high'), 66]]
            if approaches.globals_sampling.report== "furer":
              ksum_unconstrained+=el[1]
              if not el[1]==1:
                    ksum+=el[1]
                    #el[1]*=approaches.globals.nr_iterations
                    #ksum+=el[1]
                    counter+=1
            else:
              ksum = ksum + el[1]
        # now the normalization change
        if counter==1:
            ksum+=1
        for el in fd[k]:    
            if float(ksum)==0:
                ksum=len(fd[k])
                el[1]=el[1] / float(ksum)
            else:
                el[1] = el[1] / float(ksum)
    return fd

    
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
           approaches.globals_sampling.default_key=intertuple
        p_table_pde[intertuple] = valuedict
    return p_table_pde
    
def make_new_dict(pd_general):
     new_dict={}
     for k in pd_general.keys():
        new_dict[(('default', 'default'),)]=pd_general[k]
     return new_dict


#IrMA: changed it here that the function returns the total_freq_dict (needed it for time snapshots)
def handle_quota(D,  P,  Plist,  total_freq_dict,  mappings_list,thread_number):
    #global globalist_randomnode
    #global globaltimes_randomnode   
    #approaches.globals.globaltimes_randomnode[thread_number].append(time.time() - approaches.globals.globaltimes_randomnode[thread_number][0])
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
    #approaches.globals.globalist_randomnode[thread_number].append(total_freq_dict)
    approaches.globals_sampling.nlimit_nr_embeddings.append(nr_emb)
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
    if approaches.globals_sampling.abort:
         if len(matched_list) == len(Plist):
             temp_result=[matched_list]
             nodes_observed=nodes_observed_list
             with lock:
                approaches.globals_sampling.temporary_embeddings.append(matched_list)
             return [matched_list]
         else:
             nodes_observed=nodes_observed_list
             return None
    global temp_result
    global nodes_observed
    matching_subgraphs = []
    if i < len(Plist):       #border condition
        #print "Pred match: ", D.node[n], P.node[Plist[i]],matches(n, D,  Plist[i], P,  matched_list,  Plist)
        if matches(n, D,  Plist[i], P,  matched_list,  Plist):
            matched_list.append(D.node[n]['id'])
            candidates = []
            for matched in matched_list:
                for x in D.neighbors(matched):
                    if x not in matched_list:   # we do not want to check the already matched, besides: they should not appear again(?)
                        candidates.append(x)
            counter=1
            approaches.globals_sampling.candidates+=len(candidates)
            if len(candidates)==0:
                candidates=[n]
            for c in candidates:
                counter+=1
                nodes_observed_list[0] = nodes_observed_list[0] + 1
                approaches.globals_sampling.temporary_observed[0]= approaches.globals_sampling.temporary_observed[0] + 1
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
            if matched_list in approaches.globals_sampling.temporary_embeddings:
       	           return [matched_list]
            
            with lock:
                 approaches.globals_sampling.nr_embeddings_exhaustive+=1
                 approaches.globals_sampling.temporary_embeddings.append(matched_list)
                 if(nodes_observed==1):
                   raise Wrong_root_node('cannot use this one as a root node')
                 target_values = []
                 for i in range(len(Plist)):
                    if P.node[Plist[i]]['target'] == True:
                             value_tuple = (P.node[Plist[i]]['label'] , D.node[matched_list[i]]['value'])
                             target_values.append(value_tuple)
                 target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.            


                 if target_tuple in approaches.globals_sampling.freq_dict_exhaustive:
                            approaches.globals_sampling.freq_dict_exhaustive[target_tuple] += 1
                            approaches.globals_sampling.freq_dict_tuple_count[target_tuple] += 1
                 else:
                           approaches.globals_sampling.freq_dict_exhaustive[target_tuple] = 1
                           approaches.globals_sampling.freq_dict_tuple_count[target_tuple] = 1
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
    approaches.globals_sampling.globaltimes_furer.append(time.time() - approaches.globals_sampling.globaltimes_furer[0])
    approaches.globals_sampling.nlimit_iteration_counter.append(iteration_counter)
    freq_dict = {}
    nr_emb=0
    nr_emb1=0
    for k in total_Zlist_dict_copy.keys():
        freq_dict[k] = (total_Zlist_dict_copy[k])/float(iteration_counter)   # simply an average of a list
        nr_emb+=freq_dict[k]
        nr_emb1+=total_Zlist_dict_copy[k]
    approaches.globals_sampling.globalist_furer.append(freq_dict)
    approaches.globals_sampling.nlimit_nr_embeddings.append(nr_emb)
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

    if len(nlimitlist)<=approaches.globals_sampling.cqi[thread_number]:
        nlimitlist.append(sum(nlimitlist))
    if nodes_observed_list[0] > nlimitlist[approaches.globals_sampling.cqi[thread_number]]:
        approaches.globals_sampling.cqi[thread_number] = approaches.globals_sampling.cqi[thread_number] + 1    # we increase the index of position of quota to check upon
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
        
        
def find_embeddings_Furer(nodes, D,  P,  OBdecomp,   i,  matched_list,  nodes_observed_list, Zlist_dict, iteration_counter,  epsilon_from_above,thread_number):
    """
    nodes : a list of (candidate) nodes to fit in this step GIVEN IN THE SAME ORDER as appear in OBdecomp!
    OBdecomp : ordered bipartite decomposition on P, which is given. First element is root. # [ [2] , [1,3] , [4] , [5, 6] ]
    i : index of the currently analyzed decomposition element
    """
    X = 1
    if (i < len(OBdecomp)):       #border condition, limit condition
        #print "Back here"
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
                  if matches_Furer(c, D,  el, P,  matched_list,  OBd_matched_next):
                          good_el.append(c)
                good_collection.append(good_el)
            lists_intersection = set.intersection(*map(set,good_collection))
            
            if len(lists_intersection) > 0:
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
                        break
                    s_next_nodes=set(nodes_next)
                    if(len(s_next_nodes)!=len(OBdecomp[i+1])):
                          return [0, None]
                    # now only the recursive call
                    copyforcandidate = copy.deepcopy(matched_list)
                    result = find_embeddings_Furer(nodes_next,  D,  P,  OBdecomp,  i+1,  copyforcandidate,  nodes_observed_list,  Zlist_dict, iteration_counter,  epsilon,thread_number)
                    if result[1] != None:
                        matched_list = result[1]
                        X = X * result[0]                
            else:
                number_of_combinations = functools.reduce(lambda x, y: x*y, [len(x) for x in good_collection])        # counts the number of their combinations
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
                    result = find_embeddings_Furer(nodes_next,  D,  P,  OBdecomp,  i+1,  copyforcandidate,  nodes_observed_list,  Zlist_dict, iteration_counter,  epsilon,thread_number)
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
        


# predicate_match procedure is changed here, so that we also compare against values if they are part of the pattern
def predicate_match(x, y):
    if x['predicate'] == y['predicate']:
    #     if y['valueinpattern']==1:
    #         if 'value' in x.keys() and x['value'] == y['value']:
    #             return True
    #         else:
    #             return False
    #     else:
    #         return True
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
        neighbor_test = True
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
    #print "Matches?",D.node[n], P.node[m]
    if predicate_match(D.node[n],  P.node[m]):
        test_list = matched_list + [n]
        compare_list = OBmatched+[m]
        if len(test_list) !=len(OBmatched+[m]): #hence, they should be of equal size and ready to be compared
          if not(os.path.exists(os.path.join(output_bug,"unequal_size.warning"))):
                with open(os.path.join(output_bug,"unequal_size.warning"),'w') as f:
                    f.write("Unequal size warning.")
                    f.close()
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