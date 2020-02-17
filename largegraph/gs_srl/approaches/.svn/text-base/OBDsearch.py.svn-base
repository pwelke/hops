

# Procedures for automatic COBD calculation.
# The useful ones are:
# - get_heuristic4_OBD()  as a heuristic one [the only heuristic one here that does not miss-out solutions]
# - getOBD2plus4() as the fastest exhaustive one [uses two filtering techniques for early detection of graphs without an OBD]

import itertools
import time
import pickle
import numpy
import networkx as nx
import matplotlib.pyplot as plt


def insertOBDlabels(P,  obd):
    allOK = True
    for n in P.nodes():
        label = None
        for i in range(len(obd)):       # obd is a list of elements (lists), if n is in i-th element, then i is its label
            if n in obd[i]:
                label = i
        if label == None:
            allOK = False
            print "Warning: not all nodes are in the provided OBD."
            break
        P.node[n]['OBDlabel'] = label
    return allOK


def OBDnodeCondition(n,  P):
    """assumes that nodes have ['OBDlabel'] set already (this is why  insertOBDlabels() must be called beforehand) """
    condition = True
    higherNeighborLabel = None
    for neigh in P.neighbors(n):
        if P.node[neigh]['OBDlabel'] == P.node[n]['OBDlabel']:
            condition = False
            break
        elif P.node[neigh]['OBDlabel'] > P.node[n]['OBDlabel']:
            if higherNeighborLabel == None:
                higherNeighborLabel = P.node[neigh]['OBDlabel']
            else:
                if P.node[neigh]['OBDlabel'] != higherNeighborLabel:
                    condition = False
                    break
    return condition
    

def OBDcorrect(P,  obd):
    correct = True
    ans = insertOBDlabels(P,  obd)    # adds 'OBDlabel' to each node in P, according to decomposition obd
    if ans == False:
        correct = False
    else:
        for n in P.nodes():
            if not OBDnodeCondition(n,  P):      #do all the neighbors have different labels, and all with higher label have the same one?
                correct = False
                break
    return correct

def connectedOBD(P,  obd):
    '''test whether the obd is such, that each node with higher level is connected to some node with lower level (needed in our depth-first kind of algorithm)'''
    connected = True
    seen = []
    if len(obd[0]) > 1:
        connected = False
        ##print "Warning: more than one root element in obd."
    else:
        seen.append(obd[0][0])
    for i in range(len(obd)):
        if i == 0:
            pass
        else:
            for el in obd[i]:
                test = False
                neighbors = P.neighbors(el)
                for neigh in neighbors:
                    if neigh in seen:
                        test = True
                if test == False:
                    connected = False
                else:
                    seen.append(el)
    return connected



# create all possible permutations of elements (IDs) - and on each permutation then try all possible splits....first with len(P) parts (optimal) and then lower.
def split_list(data, n):
#""" splits a list into n parts in all possible ways
#>>> list(split_list([1, 2, 3, 4], 2))
#[[[1], [2, 3, 4]], [[1, 2], [3, 4]], [[1, 2, 3], [4]]]
#>>> list(split_list([1, 2, 3, 4], 3))
#[[[1], [2], [3, 4]], [[1], [2, 3], [4]], [[1, 2], [3], [4]]]"""
    from itertools import combinations, chain
    for splits in combinations(range(1, len(data)), n-1):
        result = []
        prev = None
        for split in chain(splits, [None]):
            result.append(data[prev:split])
            prev = split
        yield result


def getOBD(P):
    result = None
    found = False
    IDs = []
    for n in P.nodes():
        IDs.append(P.node[n]['id'])
    # we will try with largest possible decomposition size and then go lower, if nothing is found
    decomp_size = len(IDs)
    while decomp_size > 0:
        # now we go over all possible permutations of IDs
        permutations = itertools.permutations(IDs)      # this has to be recreated each time we go over it again
        for perm in permutations:
            splits = split_list(list(perm),  decomp_size)
            for s in splits:
                # now this is our candidate OBD
                if ( OBDcorrect(P, s) and connectedOBD(P,  s) ):        # connectedOBD is additional condition because of our depth-first approach
                    result = s
                    found = True
                if found == True: break;
            if found == True: break;
        if found == True: break;
        decomp_size = decomp_size -1
    if found == False:
        ##print "OBD was not found for this pattern."
        result = None
    return result

#------------------------------HEURISTIC 1--------------------------------

def heuristic1_label_OBD(n,  P,  current_label):
    P.node[n]['OBDlabel'] = current_label
    current_label = current_label + 1
    neighbors = P.neighbors(n)
    for neigh in neighbors:
        if 'OBDlabel' in P.node[neigh].keys():
            if P.node[neigh]['OBDlabel'] > current_label:
                current_label = P.node[neigh]['OBDlabel']
    # we got maximum of current label or any node that neighbors have - now we label them all with that
    for neigh in neighbors:
        if 'OBDlabel' in P.node[neigh].keys():
            if P.node[neigh]['OBDlabel'] >= P.node[n]['OBDlabel']:
                heuristic1_label_OBD(neigh,  P,  current_label)
            else:   # if set and smaller than mine, leave them alone
                pass
        else:   # if not set, then not lower and not labelled
            heuristic1_label_OBD(neigh,  P,  current_label)

def produceOBDlist(P):
    """expects pattern P which has OBDlabel set for all the nodes. OBDlist is created accoring to labels (some might be skipped! so this is taken into account)"""
    # first we'll get all OBD labels, so that we can see how many different ones are there...
    output = []
    OBDlabels = set() # set, so that we do not collect duplicate labels
    for n in P.nodes():
        OBDlabels.add(P.node[n]['OBDlabel'])
    OBDlabels = list(OBDlabels)     # now we have a list of labels without duplicates
    OBDlabels.sort()    # in-place sorting (OBDlabels is changed)
    for el in OBDlabels:
        innerlist = []
        for n in P.nodes():
            if P.node[n]['OBDlabel'] == el:
                innerlist.append(n)
        output.append(innerlist)
    return output


def get_heuristic1_OBD(P):
    heuristic1_label_OBD(P.nodes()[0],  P,  1)
    obd = produceOBDlist(P)
    if ( OBDcorrect(P, obd) and connectedOBD(P,  obd) ): 
        return obd
    else:
        return None
    # result will be put into ['OBDlabel'] of nodes in P, so you have to create then the proper format...


#------------------------------HEURISTIC 2--------------------------------

def heuristic2_label_OBD(n,  P,  label, critical=None):
    """heuristic approach with backtracking"""
    print "trying to label " + str(n) + " with " + str(label)
    nodes_labeled = []
    if ('critical' in P.node[n].keys()) and (P.node[n]['critical']==True) and (P.node[n]['OBDlabel'] != label) :
        print "FAIL on critical and not the same label."
        return (False,  [])         # being critical, we could avoid failure only if the label to set would be the same (it happens)
    else:
        P.node[n]['OBDlabel'] = label
        nodes_labeled.append(n)                 # this is a list that gets passed through recursions
        if critical == True:
            P.node[n]['critical'] = True
    # labeling part done
    flag_critical = False   # if I will label more than one neighbor from now on, then the labels will be critical (not to be changed by others)
    new_label = label + 1
    neighbors = P.neighbors(n)
    for neigh in neighbors:
        if 'OBDlabel' in P.node[neigh].keys():
            if P.node[neigh]['OBDlabel'] > new_label:
                new_label = P.node[neigh]['OBDlabel']
    # we got maximum of current label or any node that neighbors have - now we label them all with that
    neighbors_to_label = []
    for neigh in neighbors:
        if 'OBDlabel' in P.node[neigh].keys():
            if (P.node[neigh]['OBDlabel'] >= P.node[n]['OBDlabel']) or (P.node[neigh]['OBDlabel']  == None):    # now they can have it, but set to None (because of removal in failers)
                neighbors_to_label.append(neigh)
            else:   # if set and smaller than mine, leave them alone
                pass
        else:   # if not set, then not lower and not labelled
            neighbors_to_label.append(neigh)
    # now we have all the neighbors that need to be labeled
    if len(neighbors_to_label) > 1:
        flag_critical = True
    # and now the recursive step - labeling all these nodes
    permutations = itertools.permutations(neighbors_to_label)      # iterator : gets exhausted as we access elements
    for perm in permutations:
        print "trying perm: " + str(perm)
        this_run_success = True
        this_run_labeled = []
        for el in perm:
            (s,  nl) = heuristic2_label_OBD(el,  P,  new_label, flag_critical)
            this_run_labeled = this_run_labeled + nl
            if s == False:
                this_run_success = False
                break
        if this_run_success == False:
            # then unlabel all that were labelled up to now
            for nn in this_run_labeled:
                print "removing label of " + str(nn)
                P.node[nn]['OBDlabel']  = None
                P.node[nn]['critical']  = False
        else:   # obviously success is True, we managed to label all others...
            nodes_labeled = nodes_labeled + this_run_labeled
            print "Win in labeling neighbors of " + str(n)
            return (True,  nodes_labeled)
            break
    # if no permutation is successful, we end up returning the last line
    return (False,  nodes_labeled)
    print "FAIL of all permutations from " + str(n)




def get_heuristic2_OBD(P):
    heuristic2_label_OBD(P.nodes()[0],  P,  1)


#------------------------------HEURISTIC 2B--------------------------------

def heuristic2B_label_OBD(n,  P,  label, critical=None):
    """heuristic approach with backtracking"""
    nodes_labeled = []

    flag_critical = False   # if I will label more than one neighbor from now on, then the labels will be critical (not to be changed by others)
    new_label = label + 1
    
    neighbors = P.neighbors(n)
    for neigh in neighbors:
        if 'OBDlabel' in P.node[neigh].keys():      # if it has a label
            if P.node[neigh]['OBDlabel'] > new_label:   # and it is higher than what I would use for labeling
                new_label = P.node[neigh]['OBDlabel']
    # we got maximum of current label or any node that neighbors have - now we label them all with that
    
    neighbors_to_label = []
    for neigh in neighbors:
        if 'OBDlabel' in P.node[neigh].keys():
            if (P.node[neigh]['OBDlabel'] >= P.node[n]['OBDlabel']) or (P.node[neigh]['OBDlabel']  == None):    # now they can have it, but set to None (because of removal in failers)
                neighbors_to_label.append(neigh)
            else:   # if set and smaller than mine, leave them alone
                pass
        else:   # if not set, then not lower and not labelled
            neighbors_to_label.append(neigh)
    # now we have all the neighbors that need to be labeled
    
    if len(neighbors_to_label) > 1:
        flag_critical = True
    # and now labeling all these nodes
    
    for neigh in neighbors_to_label:
        if ('critical' in P.node[neigh].keys()) and (P.node[neigh]['critical']==True) and (P.node[neigh]['OBDlabel'] != new_label) :
            return (False,  nodes_labeled)         # being critical, we could avoid failure only if the label to set would be the same (it happens)
        else:
            P.node[neigh]['OBDlabel'] = new_label
            nodes_labeled.append(neigh)                 # this is a list that gets passed through recursions
            if flag_critical == True:
                P.node[neigh]['critical'] = True
        # labeling part done
        
    # and now recursive step - going into each neighbor to continue, in any order if necessary
    permutations = itertools.permutations(neighbors_to_label)      # iterator : gets exhausted as we access elements
    for perm in permutations:
        this_run_success = True
        this_run_labeled = []
        for el in perm:
            (s,  nl) = heuristic2B_label_OBD(el,  P,  new_label, flag_critical)
            this_run_labeled = this_run_labeled + nl
            if s == False:
                this_run_success = False
        if this_run_success == False:
            # then unlabel all that were labelled up to now
            for nn in this_run_labeled:
                P.node[nn]['OBDlabel']  = None
                P.node[nn]['critical']  = False
        else:   # obviously success is True, we managed to label all others...
            nodes_labeled = nodes_labeled + this_run_labeled
            return (True,  nodes_labeled)
            break
    # if no permutation is successful, we end up returning the last line
    return (False,  nodes_labeled)


def get_heuristic2B_OBD(P):
    # in this version we label the root before recursion
    for n in P.nodes():
        root = n
        P.node[root]['OBDlabel'] = 1
        (success, result) = heuristic2B_label_OBD(root,  P,  1)
        if success:
            obd = produceOBDlist(P)
            if ( OBDcorrect(P, obd) and connectedOBD(P,  obd) ): 
                return obd
            else:
                for no in P.nodes():
                    P.node[no]['OBDlabel']  = None
                    P.node[no]['critical']  = False
        else:   # in case of failure of all attempts with this node as a root - we have to clean up all flags and labels before the new root is tried
            for nn in P.nodes():
                P.node[nn]['OBDlabel']  = None
                P.node[nn]['critical']  = False
    # if we did not return any solution before, then None was found
    return None



#----------------------------------------------------------------------------------
#------------------------------exhaustive 2--------------------------------

def any_neighbors(nodelist,  G):
    """If any two nodes in the nodelist are neighbors in graph G, it outputs TRUE, otherwise FALSE."""
    outcome = False
    #neighbors = P.neighbors(n)
    for i in range(len(nodelist)):
        for j in range(i+1, len(nodelist)):
            if G.has_edge(nodelist[i], nodelist[j]) or G.has_edge(nodelist[j], nodelist[i]):
            ##if nodelist[j] in G.neighbors(nodelist[i]):
                outcome = True
                return outcome
    return outcome



def getOBD2(P):
    result = None
    found = False
    IDs = []
    for n in P.nodes():
        IDs.append(P.node[n]['id'])
    # we will try with largest possible decomposition size and then go lower, if nothing is found
    decomp_size = len(IDs)
    while decomp_size > 0:
        # now we go over all possible permutations of IDs
        permutations = itertools.permutations(IDs)      # this has to be recreated each time we go over it again
        for perm in permutations:
            splits = split_list(list(perm),  decomp_size)
            for s in splits:
                # now this is our candidate OBD
                # -------speedup A: checking for neighbors in elements of split
                noneighbors = True
                for nodelist in s:
                    if len(nodelist)>1:
                        if any_neighbors(nodelist,  P):
                            noneighbors = False
                # -------
                if noneighbors and OBDcorrect(P, s) and connectedOBD(P,  s):        # connectedOBD is additional condition because of our depth-first approach
                    result = s
                    found = True
                if found == True: break;
            if found == True: break;
        if found == True: break;
        decomp_size = decomp_size -1
    if found == False:
        result = None
    return result
#----------------------------------------------------------------------------------

#------------------------------exhaustive 3--------------------------------

def size_degree_check(obd,  P):
    """for every node in OBD calculates its [degree(n) - linksToNodesAlreadyInOBD]
    and verifies whether in the remaining part of OBD there is an element of at least that size (all bigger must have equal label)"""
    outcome = True
    flatOBD = [item for sublist in obd for item in sublist]     # we get a flat list from a list of lists
    seen = []
    for i in range(len(flatOBD)):
        n = flatOBD[i]
        linksback = 0
        for el in seen:
            if P.has_edge(el, n) or P.has_edge(n, el):
                linksback = linksback + 1
        out_degree = P.degree(n) - linksback
        # now verify whether we have such strength in the rest of obd
        targetElement = None
        for elobd in obd:
            if n in elobd:
                targetElement = elobd
        #       we now in which element is n - now check from here on
        remaining_obd = obd[obd.index(targetElement)+1:]
        sizes = [len(x) for x in remaining_obd]
        if (len(sizes)>0) and (max(sizes) < out_degree):
            outcome = False
            return outcome
        seen.append(n)
    return outcome


def getOBD3(P):
    result = None
    found = False
    max_degree = max(list(P.degree().values()))
    IDs = []
    for n in P.nodes():
        IDs.append(P.node[n]['id'])
    # we will try with largest possible decomposition size and then go lower, if nothing is found
    decomp_size = len(IDs)
    while decomp_size > 0:
        # now we go over all possible permutations of IDs
        permutations = itertools.permutations(IDs)      # this has to be recreated each time we go over it again
        for perm in permutations:
            splits = split_list(list(perm),  decomp_size)
            for s in splits:
                # now this is our candidate OBD
                # -------speedup B: checking sizes of decomposition elements against out-degrees
                sizeCheck = size_degree_check(s,  P)
                # -------
                if sizeCheck and OBDcorrect(P, s) and connectedOBD(P,  s):        # connectedOBD is additional condition because of our depth-first approach
                    result = s
                    found = True
                if found == True: break;
            if found == True: break;
        if found == True: break;
        decomp_size = decomp_size -1
    if found == False:
        result = None
    return result
#----------------------------------------------------------------------------------
#------------------------------exhaustive 4--------------------------------

def any_triangles(G):
    """checks and outputs (True, False) whether there are any triangles in graph G"""
    for x in G.nodes():
        for y in G.nodes():
            for z in G.nodes():
                if (x != y) and (x !=z) and (y!=z):
                   if  (G.has_edge(x, y) or G.has_edge(y, x)) and (G.has_edge(x, z) or G.has_edge(z, x)) and (G.has_edge(z, y) or G.has_edge(y, z)):
                       return True
    # if all triplets were checked and we did not find a triangle, then we can only return False
    return False


def getOBD4(P):
    if any_triangles(P):
        return None
    result = None
    found = False
    max_degree = max(list(P.degree().values()))
    IDs = []
    for n in P.nodes():
        IDs.append(P.node[n]['id'])
    # we will try with largest possible decomposition size and then go lower, if nothing is found
    decomp_size = len(IDs)
    while decomp_size > 0:
        # now we go over all possible permutations of IDs
        permutations = itertools.permutations(IDs)      # this has to be recreated each time we go over it again
        for perm in permutations:
            splits = split_list(list(perm),  decomp_size)
            for s in splits:
                # now this is our candidate OBD
                if OBDcorrect(P, s) and connectedOBD(P,  s):        # connectedOBD is additional condition because of our depth-first approach
                    result = s
                    found = True
                if found == True: break;
            if found == True: break;
        if found == True: break;
        decomp_size = decomp_size -1
    if found == False:
        result = None
    return result
#----------------------------------------------------------------------------------

#------------------------------exhaustive 2plus4--------------------------

def getOBD2plus4(P):
    if any_triangles(P):
        return None    
    result = None
    found = False
    IDs = []
    for n in P.nodes():
        IDs.append(P.node[n]['id'])
    # we will try with largest possible decomposition size and then go lower, if nothing is found
    decomp_size = len(IDs)
    while decomp_size > 0:
        # now we go over all possible permutations of IDs
        permutations = itertools.permutations(IDs)      # this has to be recreated each time we go over it again
        for perm in permutations:
            splits = split_list(list(perm),  decomp_size)
            for s in splits:
                # now this is our candidate OBD
                # -------speedup A: checking for neighbors in elements of split
                noneighbors = True
                for nodelist in s:
                    if len(nodelist)>1:
                        if any_neighbors(nodelist,  P):
                            noneighbors = False
                # -------
                if noneighbors and OBDcorrect(P, s) and connectedOBD(P,  s):        # connectedOBD is additional condition because of our depth-first approach
                    result = s
                    found = True
                if found == True: break;
            if found == True: break;
        if found == True: break;
        decomp_size = decomp_size -1
    if found == False:
        result = None
    return result
#----------------------------------------------------------------------------------





#------------------------------HEURISTIC 3--------------------------------



def to_graph(l):
    """ l is a list of lists"""
    G = nx.Graph()
    for part in l:
        # each sublist is a bunch of nodes
        G.add_nodes_from(part)
        # it also imlies a number of edges:
        G.add_edges_from(to_edges(part))
    return G

def to_edges(l):
    """ 
        treat `l` as a Graph and returns it's edges 
        to_edges(['a','b','c','d']) -> [(a,b), (b,c),(c,d)]
    """
    it = iter(l)
    last = next(it)

    for current in it:
        yield last, current
        last = current    

#G = to_graph(l)
#print connected_components(G)

def partitions(set_):
    if not set_:
        yield []
        return
    for i in xrange(2**len(set_)/2):
        parts = [set(), set()]
        for item in set_:
            parts[i&1].add(item)
            i >>= 1
        for b in partitions(parts[1]):
            yield [parts[0]]+b

#for p in partitions(["a", "b", "c", "d"]):
#print p


def h3_step(d,  P,  label):
##    print "started with decomp element %s" % str(d)
    # trenutna dekompozicija d na P, hocem celotno od tu dalje
    # d is a list like [2, 3]
    # first we check if d has any neighbors:
    if any_neighbors(d,  P):
##        print "Fail because neighbors detected in %s" % str(d)
        return (False,  [])
    else:
        #---now lets get the situation
        labeledOnes = []
        for n in d:
            if (('OBDlabel' in P.node[n].keys()) and (P.node[n]['OBDlabel'] != None)):
                labeledOnes.append(n)
        if len(labeledOnes) == len(d):
            return (True,  [])  # was done already from some other decomp. element
        elif ((len(labeledOnes) < len(d)) and (len(labeledOnes) > 0)):       # so, if some are labeled, but not all
            return (False,  [])
        else:   # none are labeled
            for n in d:
                P.node[n]['OBDlabel'] = label
        new_label = label + 1
    all_labeled = d
    output = [d]
    neighbors_to_d = []     # this will be a list of lists, for each element e in d it will hold e's neighbors that are not labeled yet
    for el in d:
        neighbors_to_d.append([x for x in P.neighbors(el) if (('OBDlabel' not in P.node[x].keys()) or (P.node[x]['OBDlabel']==None) or (P.node[x]['OBDlabel']>=P.node[el]['OBDlabel']))  ])
    if neighbors_to_d == []:
##        print "Success, because no more unlabeled neighbors for %s" % str(d)
        return (True,  [d])
    #now we'll merge them according to connected components
    tempG = to_graph(neighbors_to_d)
    components = nx.connected_components(tempG)
    # components contains all groups of nodes that can have different decomposition labels, at least according to local information
    # we try with the most defragmented components, and then merge them (PARTITIONING) if it fails in later steps
    # when all partitions are exhausted, we report failure back
    indices = set(range(len(components)))       # set of indices will be partitioned
##    print "components: %s" % str(components)
##    print "indices: %s" % str(indices)
    for partits in partitions(indices):
        for par in itertools.permutations(partits):
            # par is one partition of indeces, like: [ set([0]) , set([1]) , set([2])   ]  or [ [0], [1,2]  ]  that correspond to e.g.   [  [1],  [2,3,4]   ]
##            print "trying par: %s" % str(par)
            this_try = True     # all decomposition elements in partition have to succeed
            all_decomps = []
            this_try_labeled = []
            for d_next_inds in par:
                d_next_inds = list(d_next_inds)       # we make a list back from a set
                # now we have to merge the components with these indices into a decomposition element candidate
                d_next = []
                for i in d_next_inds:
                    d_next = d_next + components[i]
                # d_next is now the new candidate partition class
##                print "and trying the next decomp candidate in next recursive step: %s" % str(d_next)
                (success,  partial_decomp) = h3_step(d_next,  P,  new_label)
                if success == True:
                    all_decomps = all_decomps + partial_decomp
                    this_try_labeled = this_try_labeled + partial_decomp
                    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX problem: several possible solutions and not all elements are duplicates!!!
                else:
                    this_try = False
            if this_try == True:     # obviously this partition was OK in recursions
                output = output + all_decomps
##                print "Success in recursion below. Outputting %s" % str(output)
                return (True,  output)
            else:
                for alist in this_try_labeled:
                    for nodeid in alist:
                        P.node[nodeid]['OBDlabel'] = None
    # if we came to here it means all partitions of indices of components were exhausted without solution
##    print "Fail because all options exhausted"
    return (False,  output)

def get_heuristic3_OBD(P):
    #
    for n in P.nodes():
        root = n
        (success, result) = h3_step([root],  P,  1)
        if success:
            #----might have duplicates, so we'll remove them
            nice_result = []
            for el in result:
                if el not in nice_result:
                    nice_result.append(el)
##            print "as success we get OBD: %s" % str(nice_result)
            if ( OBDcorrect(P, nice_result) and connectedOBD(P,  nice_result) ): 
                return nice_result
            else:
                pass
##                print "The produced OBD was either not correct or not connected"
##        print "----------------------------------"
        #----cleaning after this root node was not successful
        for nn in P.nodes():
            if ('OBDlabel' in P.node[nn].keys()):
                P.node[nn]['OBDlabel'] = None
        #-----------------
    # if we did not return any solution before, then None was found
    return None




#----------------------------------------------------------------------------------

#------------HEURISTIC 4    ---------------------------------------------

def get_components(partOBD,  P):
    flat_partialOBD = [item for sublist in partOBD for item in sublist]     # we get a flat list from a list of lists
    #
    meta_neighbors = []     # this will contain all contents of neighbors_to_d for all d-s
    #print "partObd: ",partOBD
    for d in partOBD:
        neighbors_to_d = []     # this will be a list of lists, for each element e in d it will hold e's neighbors that are not labeled yet
        for el in d:
            neighbors_to_d.append([x for x in P.neighbors(el) if (x not in flat_partialOBD)])
        meta_neighbors = meta_neighbors + neighbors_to_d
    #now we'll merge them according to connected components
    tempG = to_graph(meta_neighbors)
    #print "tempG",meta_neighbors
    components = nx.connected_components(tempG)
    return components
    


def labelon(partialOBD,  P):
    #print "came into labelon() with partialOBD: %s" % str(partialOBD)
    flat_partialOBD = [item for sublist in partialOBD for item in sublist]     # we get a flat list from a list of lists
    #print partialOBD
    if len(flat_partialOBD) == len(P.nodes()):      # check for the end of recursion
##        print "and YES, we are at recursion end"
        if ( OBDcorrect(P, partialOBD) and connectedOBD(P,  partialOBD) ):
            #print "and even correct and connected - FINISH."
            return partialOBD
        else:
            #print "but not correct OBD or not connected"
            return None
    else:       # else: get all candidates to continue (next connected components) and try on all of them
        components = list(get_components(partialOBD,  P))
        #print "Components: ",components
        # now to partialOBD we add each component separately, but also each possible merging of these components, including full merge
        candidates = []     # this will hold all such candidates, each candidate is a list of vertices
        for L in range(1, len(components)+1):
            for subset in itertools.combinations(components, L):
                cand = subset   # but this is a list of lists - we have to flatten it
                candFlat = [x for sub in cand for x in sub]
                candidates.append(candFlat)
        for c in candidates:
            new_partial_OBD = partialOBD + [c]
##            print "starting recursive call with new_partialOBD: %s" % str(new_partial_OBD)
            result = labelon(new_partial_OBD,  P)
##            print "back from recursion call for new_partialOBD: %s" % str(new_partial_OBD)
##            print "and result is: %s" % str(result)
            if result != None:
                return result
    # if I came here without returning something , then nothing was found below me
    return None
 
def get_all_labelon(partialOBD,  P,result):
    #print "came into labelon() with partialOBD: %s" % str(partialOBD)
    flat_partialOBD = [item for sublist in partialOBD for item in sublist]     # we get a flat list from a list of lists
    #print partialOBD
    if len(flat_partialOBD) == len(P.nodes()):      # check for the end of recursion
##        print "and YES, we are at recursion end"
        if ( OBDcorrect(P, partialOBD) and connectedOBD(P,  partialOBD) ):
            #print "and even correct and connected - FINISH."
            return partialOBD
        else:
            #print "but not correct OBD or not connected"
            return None
    else:       # else: get all candidates to continue (next connected components) and try on all of them
        components = list(get_components(partialOBD,  P))
        #print "Components: ",components
        # now to partialOBD we add each component separately, but also each possible merging of these components, including full merge
        candidates = []     # this will hold all such candidates, each candidate is a list of vertices
        for L in range(1, len(components)+1):
            for subset in itertools.combinations(components, L):
                cand = subset   # but this is a list of lists - we have to flatten it
                candFlat = [x for sub in cand for x in sub]
                candidates.append(candFlat)
        for c in candidates:
            new_partial_OBD = partialOBD + [c]
##            print "starting recursive call with new_partialOBD: %s" % str(new_partial_OBD)
            result.append(labelon(new_partial_OBD,  P))
##            print "back from recursion call for new_partialOBD: %s" % str(new_partial_OBD)
##            print "and result is: %s" % str(result)
            if len(result) != 0:
                return result
    # if I came here without returning something , then nothing was found below me
    return None 
    

def get_heuristic4_OBD(P,  startNode = None):
    #
    if startNode == None:
        for n in P.nodes():
            result = labelon([[n]],  P)
            if result != None:
                return result
        return None
    else:
        result = labelon([[startNode]],  P)
        if result != None:
            return result
        return None
    
def get_heuristic4_OBD_1(P,  startNode = None):
    #
    if startNode == None:
        for n in P.nodes():
            result = get_all_labelon([[n]],  P,[])
            if len(result) != 0:
               return result
        return None
    else:
        result = get_all_labelon([[startNode]],  P,[])
        if len(result) != 0:
            return result
        return None
    
def get_flatList(P,  startNode = None):
    if startNode == None:
        result=[]
        for n in P.nodes():
            result.append([n])
            if result != None:
                return result
        return None
    else:
        result=[[startNode]]
        for n in P.nodes():
            if(n!=startNode):
                result.append([n])
            
        if result != None:
            return result
        return None





####pattern_file_name = "pattern1.gml"
##pattern_file_name = "graph6c_15.gml"
## ./problemAnalysis/graph8c_random_663.gml
####P = nx.read_gml(pattern_file_name)
####print "reading done."

#pattern_file_name = "/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/PATTERNS/PATTERNS_DBLP/PATTERNS_400_BATCH/patterns_size_6/dblppattern_7bdc87d4ce3840fdba8d5aca887558d1/dblppattern_7bdc87d4ce3840fdba8d5aca887558d1.gml"; 
#pattern_file_name = "/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/PATTERNS/PATTERNS_DBLP/PATTERNS_400_BATCH/patterns_size_10/dblppattern_d3c77c1cd78e45c39ea44b2bf6ce027a/dblppattern_d3c77c1cd78e45c39ea44b2bf6ce027a.gml"; 
#pattern_file_name = "/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/PATTERNS/PATTERNS_DBLP/PATTERNS_400_BATCH/patterns_size_15/dblppattern_3bf3b4272afa4b6ea2c4af77a7805284/dblppattern_3bf3b4272afa4b6ea2c4af77a7805284.gml"; 

#P = nx.read_gml(pattern_file_name); 
#print "OBD"
#print get_heuristic4_OBD(P)

# OBdecomp = [ [0], [1] , [2, 3], [4],  [5] ]

##start = time.time()
##res = get_heuristic1_OBD(P)
##stop = time.time()
##
##print res
##print "Calculation took %.2f seconds." % (stop-start)


# call with: > python OBDsearch.py patternX.gml [resultfile.obd] [computer_name]
##if __name__=="__main__":
##    import sys
##    pattern_file_name = sys.argv[1]
##    result_file_name = None
##    computer_name = None
##    if len(sys.argv)>2:
##        result_file_name = sys.argv[2]
##    if len(sys.argv)>3:
##        computer_name = sys.argv[3]
##    P = nx.read_gml(pattern_file_name)
##    start = time.time()
##    obd = getOBD(P)
##    stop = time.time()
##    if obd != None:
##        print obd
##    else:
##        print "None, OBD not found."
##    if result_file_name != None:
##        resultfile = open(result_file_name,  'w')
##        resultfile.write(str(obd)); resultfile.write('\n')
##        if computer_name !=None:
##            resultfile.write("Finding OBD took %.2f seconds on %s." % (stop-start,  computer_name))
##        else:
##            resultfile.write("Finding OBD took %.2f seconds." % (stop-start))

