'''
@author: hoPS
'''


import approaches.globals_sampling
import copy
import math
import random
import time
from decimal import Decimal, getcontext
import approaches.globals_sampling
import sampling_core.sampler_general_ex as smplr

class Furer:
   D=None
   P=None
   root_nodes=None
   output_path=None
   nodes_observed=-1
   lock=None
   OBdecomp=None
   globalist_furer=None
   globaltimes_furer=None
   current_iteration=-1
   abort=False
   iteration_counter=0
   Zlist_dict=None
   report_flag=False
   freq_dict={}
   nr_embeddings_exhaustive=-1
   max_rec_fit_time=300
   ordering_of_target_nodes=None
   nr_targets=None
   
   FreqValue = {}
   def __init__(self, D, P, u, vs, output_path, lock, current_iteration, nr_embeddings):
          self.D=D
          self.P=P
          self.u = u
          self.vs = vs
          self.output_path=output_path
          self.start_time_monitor=0
          self.end_time_monitor=0
          self.lock=lock
          self.current_iteration=current_iteration
          self.nr_embeddings_exhaustive=nr_embeddings
          nr_target=0
          for n in P.nodes():
              if P.node[n]['target']==True:
                  nr_target+=1
          self.nr_targets=nr_target

       
   def run(self):
        """
        Do stuff in loop
        """
        approaches.globals_sampling.globaltimes_furer = [time.time()]
        approaches.globals_sampling.cqi = 0
        approaches.globals_sampling.globalist_furer = []

        freq_dict={}    # dictionary with tuples of values as keys and frequency as value
        self.Zlist_dict = {}     # Furer will result in a list of estimations for each tuple -> average of this list must be taken as frequency
        # out of debug we do not use a list actually: an integer is kept for every tuple, and divided by number of iterations at the end
        number_of_targets = 0
        for node in self.P.nodes():
            if self.P.node[node]['target'] == True:
                number_of_targets += 1
        # number_of_targets holds the number of target nodes that we are after
        self.nodes_observed = 0
        self.iteration_counter = 0
        getcontext().prec = 100
        seed_counter=1
        self.sum_estimates = 0
        while True:
            if(self.abort==True):
                for k in self.Zlist_dict.keys():
                    freq_dict[k] = (self.Zlist_dict[k])/float(self.iteration_counter)
                nr_emb=0
                for k in freq_dict.keys():
                    nr_emb+=freq_dict[k]
                return
            if approaches.globals_sampling.same_seed:
                random.seed(seed_counter)
                seed_counter+=1
            if self.iteration_counter % 1000 == 0:
                approaches.globals_sampling.cqi = approaches.globals_sampling.cqi + 1    # we increase the index of position of quota to check upon
                # total_Zlist_dict_copy = copy.deepcopy(self.Zlist_dict)
                smplr.handle_quota_Furer(self.D,  self.P, self.Zlist_dict,  [0,None], self.iteration_counter,self.current_iteration)

            # sample first image of u
            vi = random.randrange(len(self.vs))
            v = self.vs[vi]

            self.iteration_counter = self.iteration_counter + 1
            self.nodes_observed = self.nodes_observed + 1

            c, phi, phi_inv = find_tree_embeddings(self.u, v, {self.u: v}, {v: self.u}, self.P, self.D)
            c *= len(self.vs)

            if c > 0:
                target_values = []
                for i in range(self.P.number_of_nodes()):
                    if self.P.node[i]['target'] == True:
                        if 'value' in self.D.node[phi[i]]:
                            value=self.D.node[phi[i]]['value']
                            value_tuple = (self.P.node[i]['label'], value)
                            if self.ordering_of_target_nodes is not None:
                                target_values[self.ordering_of_target_nodes[i]] = value_tuple
                            else:
                                target_values.append(value_tuple)
                target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.
                with self.lock:
                    if target_tuple in self.Zlist_dict:   # this checks for KEYS in Zlist_dict
                        self.Zlist_dict[target_tuple] = self.Zlist_dict[target_tuple] + c
                    else:
                        self.Zlist_dict[target_tuple] = 0
                        self.Zlist_dict[target_tuple] = self.Zlist_dict[target_tuple] + c

            # tends to be slow for large number of iterations (obviously). do it by foot.
            # nr_emb=get_nr_embeddings(self.Zlist_dict,self.iteration_counter)
            self.sum_estimates += c
            nr_emb = self.sum_estimates / float(self.iteration_counter)

            self.FreqValue[self.iteration_counter] = (c, nr_emb)

            approaches.globals_sampling.sum_number_of_embeddings+=Decimal(nr_emb)
            approaches.globals_sampling.sum_of_the_square_embeddings+=Decimal(math.pow((nr_emb), 2))
            approaches.globals_sampling.sum_number_of_extra_embeddings+=Decimal(c)
            approaches.globals_sampling.sum_of_the_square_extra_embeddings+=Decimal(math.pow((c), 2))
            approaches.globals_sampling.embeddings_estimate=nr_emb
            approaches.globals_sampling.nr_iterations=self.iteration_counter

        return [approaches.globals_sampling.globalist_furer, approaches.globals_sampling.globaltimes_furer]


def get_nr_embeddings(Zlist,current_iteration):
    nr_emb=0
    for k in Zlist.keys():
        nr_emb+=Zlist[k]/float(current_iteration)
    return nr_emb


def n_max_matchings(A, B):
    """
    Compute the number of maximum matchings in a complete bipartite graph on A + B vertices.
    A and B are required to be nonnegative.
    Corner Case: If at least one of the sides has zero vertices, there is one maximal matching: the empty set.
    """
    a = min(A, B)
    b = max(A, B)
    c = 1

    if a != 0:
        for i in range(b-a+1, b+1):
            c *= i

    return c


def uniformRandomMaximumMatching(N_u, N_v, H, G):
    """
    Draw a maximum matching from a block disjoint bipartite graph uniformly at random and return it and
    the number of such matchings.

    Which vertex x can be assigned to which vertex y is given by x['predicate'] == y['predicate']

    :param N_u: list of vertices from H that must be assigned
    :param N_v: list of vertices from G that can be assigned to
    :return: M, c : a matching M, given as a map and the number of all maximum matchings c
    """

    hu = dict()
    hv = dict()
    c = 1

    # create blocks of identical symbols
    for x in N_u:
        try:
            hu[H.node[x]['predicate']].append(x)
        except KeyError:
            hu[H.node[x]['predicate']] = [x]

    for y in N_v:
        try:
            hv[G.node[y]['predicate']].append(y)
        except KeyError:
            hv[G.node[y]['predicate']] = [y]

    # shuffle target list
    for y in hv.keys():
        random.shuffle(hv[y])

    # compute uniform random maximal matching
    matching = dict()
    for x in hu.keys():
        try:
            for i, j in zip(hu[x], hv[x]):
                matching[i] = j
            c *= n_max_matchings(len(hu[x]), len(hv[x]))
        except KeyError:
            pass
    return matching, c


def find_tree_embeddings(u, v, phi, phi_inv, H, G):
    U_n = list()
    V_n = list()
    for u_neigh in H.neighbors(u):
        if u_neigh not in phi.keys():
            U_n.append(u_neigh)
    for v_neigh in G.neighbors(v):
        if v_neigh not in phi_inv.keys():
            V_n.append(v_neigh)

    M, c = uniformRandomMaximumMatching(U_n, V_n, H, G)
    if len(M) == len(U_n):
        # add matching to phi
        for x in M.keys():
            y = M[x]
            phi[x] = y
            phi_inv[y] = x
        # recurse
        for x in M.keys():
            c_rec, phi, phi_inv = find_tree_embeddings(x, M[x], phi, phi_inv, H, G)
            c *= c_rec
            if c == 0:
                break
    else:
        c = 0

    return c, phi, phi_inv




# taken from sampler_general_ex.py
# assumptions that I am now making:
# - predicate is a categorical label (and used in the same way we use labels)
# - there are no edge labels (they seem to be represented by intermediary 'label vertices' e.g. 'predicate=interaction'
# - if there is a 'valueinpattern' this is an additional restriction and this breaks our assumptions.
#   hence, we will remove this feature from the system for comparison purposes
def predicate_match(x, y):
    if x['predicate'] == y['predicate']:
        if y['valueinpattern']==1:
            if 'value' in x.keys() and x['value'] == y['value']:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

# taken from sampler_general_ex.py
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