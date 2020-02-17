'''
Created on Apr 17, 2015

@author: irma
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
   def __init__(self,D, P, OBdecomp, root_nodes,output_path,lock,current_iteration,nr_embeddings):
          self.D=D
          self.P=P
          self.OBdecomp=OBdecomp
          self.root_nodes=root_nodes
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
        OBdecomp : ordered bipartite decomposition on P, which is given. First element is list with a root node. # [ [2] , [1,3] , [4] , [5, 6] ]
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
        self.sum_estimates = 0
        getcontext().prec = 100
        seed_counter=1
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
            rand_nr=random.randrange(len(self.root_nodes))
            n = self.root_nodes[rand_nr]
            self.iteration_counter = self.iteration_counter +1
            self.nodes_observed = self.nodes_observed + 1
            list_for_spent = []
            list_for_spent.append(self.nodes_observed)

            result = smplr.find_embeddings_Furer([n], self.D,  self.P,  self.OBdecomp,  0,  [],  list_for_spent,  self.Zlist_dict,  self.iteration_counter,  0,self.current_iteration)
            self.nodes_observed = list_for_spent[0]
            matches_found_root_node=0
            actualX = 0
            if result[1] != None:
                actualX = result[0] * len(self.root_nodes)
                matches_found_root_node=actualX
                mapping = result[1]     # this is mapping for OBdecomp FLAT.
                OBd_flat = [item for sublist in self.OBdecomp for item in sublist]
                target_values = []
                for i in range(len(OBd_flat)):
                    if self.P.node[OBd_flat[i]]['target'] == True:
                        if 'value' in self.D.node[mapping[i]]:
                            value=self.D.node[mapping[i]]['value']
                            value_tuple = (self.P.node[OBd_flat[i]]['label'] , value)
                            if self.ordering_of_target_nodes!=None:
                                target_values[self.ordering_of_target_nodes[OBd_flat[i]]]=value_tuple
                            else:
                                target_values.append(value_tuple)
                target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.
                with self.lock:
                    if target_tuple in self.Zlist_dict:   # this checks for KEYS in Zlist_dict
                        self.Zlist_dict[target_tuple] = self.Zlist_dict[target_tuple]+ actualX
                    else:
                        self.Zlist_dict[target_tuple] = 0
                        self.Zlist_dict[target_tuple] = self.Zlist_dict[target_tuple] + actualX

            # tends to be slow for large number of iterations (obviously). do it by foot.
            # nr_emb=get_nr_embeddings(self.Zlist_dict,self.iteration_counter)
            self.sum_estimates += actualX
            nr_emb = self.sum_estimates / float(self.iteration_counter)
            
            self.FreqValue[self.iteration_counter] = (actualX, nr_emb)

            approaches.globals_sampling.sum_number_of_embeddings+=Decimal(nr_emb)
            approaches.globals_sampling.sum_of_the_square_embeddings+=Decimal(math.pow((nr_emb), 2))
            approaches.globals_sampling.sum_number_of_extra_embeddings+=Decimal(matches_found_root_node)
            approaches.globals_sampling.sum_of_the_square_extra_embeddings+=Decimal(math.pow((matches_found_root_node), 2))
            approaches.globals_sampling.embeddings_estimate=nr_emb
            approaches.globals_sampling.nr_iterations=self.iteration_counter
        return [approaches.globals_sampling.globalist_furer, approaches.globals_sampling.globaltimes_furer]

def get_nr_embeddings(Zlist,current_iteration):
    nr_emb=0
    for k in Zlist.keys():
        nr_emb+=Zlist[k]/float(current_iteration)
    return nr_emb






