'''
Created on Apr 17, 2015

@author: irma
'''
import time,copy,random,math,os
import sampling_core.sampler_general_ex as smplr
import approaches.globals_sampling
#import approaches.create_csv_batch_file,os
from multiprocessing import Process, Queue
import threading,csv
import sched,timeit
import multiprocessing as mp
from decimal import Decimal, getcontext

class Random_vertex_sampling:
   D=None
   P=None
   Plist=None
   root_nodes=None
   output_path=None
   nodes_observed=-1
   lock=None
   freq_dict=None
   abort=False
   current_iteration=-1
   nr_embeddings_exhaustive=0
   nr_vertices_in_network=0
   FreqValue = {}
   
   def __init__(self,D, P, Plist, root_nodes,output_path,lock,current_iteration):
          self.D=D
          self.P=P
          self.Plist=Plist
          self.root_nodes=root_nodes
          self.output_path=output_path
          self.start_time_monitor=0
          self.end_time_monitor=0
          self.lock=lock
          self.current_iteration=current_iteration

    
   def run(self):
        """
        This is based on a procedure "sampling_exhaustive_general2()", but is limited by a number of nodes it can observe in domain graph D: nlimit
        A procedure that is GENERAL and can sample general graphs for patterns
        D : domain graph (networkx graph with 'predicate' and 'value' attributes)
        P : pattern graph (networkx graph with 'predicate' and 'value' attributes, and 'target' boolean value)
        Plist : ordered list of P nodes
        root_nodes: list of nodes of D that match the root node of P, given in advance, not considered part of sampling procedure
        """
        approaches.globals_sampling.globalist_randomnode = []
        approaches.globals_sampling.globaltimes_randomnode = [time.time()]
        approaches.globals_sampling.nr_iterations=0
        approaches.globals_sampling.root_node_samples={}
        approaches.globals_sampling.root_node_nr_samples={}
        approaches.globals_sampling.nr_root_nodes=len(self.root_nodes)
        approaches.globals_sampling.temporary_observed=[]
        approaches.globals_sampling.temporary_observed.append(0)
        self.nr_vertices_in_network=len(self.D.nodes())
        nr_iterations=1
        unique_nr_embeddings=0
        self.freq_dict={}    # dictionary with tuples of values as keys and frequency as value: (my_salary_value, his_salary_value, my_satisfaction)
        number_of_targets = 0
        for node in self.P.nodes():
            if self.P.node[node]['target'] == True:
                number_of_targets += 1
        self.nodes_observed = 0
        observed_so_far=[]
        root_nodes_already_observed=[]
        while True:
            if(self.abort==True):
                nr_emb=approaches.globals_sampling.sum_number_of_embeddings
                return 
            n = self.root_nodes[random.randrange(len(self.root_nodes))]
            self.nodes_observed = self.nodes_observed + 1
            list_for_spent = []
            list_for_spent.append(self.nodes_observed)            
            approaches.globals_sampling.nr_embeddings_exhaustive=0
            approaches.globals_sampling.temporary_embeddings=[]
            start = timeit.default_timer()
            infinity = float("inf")
            smplr.rec_fit_limited_global(n, self.D,  self.P,  self.Plist,  0,  [],[infinity],  list_for_spent, self.freq_dict,1,self.lock,"random",self.root_nodes)
            end=timeit.default_timer()
            approaches.globals_sampling.root_node_embeddings.append((self.D.node[n], approaches.globals_sampling.nr_embeddings_exhaustive, (end - start)))
            mappings_list=smplr.temp_result
            row={}
            approaches.globals_sampling.nr_iterations+=1
            nr_of_embeddings = get_nr_embeddings(approaches.globals_sampling.freq_dict_exhaustive, approaches.globals_sampling.nr_iterations)
            overall_nr_emb_estimate= ((nr_of_embeddings) / float(approaches.globals_sampling.nr_iterations)) * len(self.root_nodes)
            overall_nr_emb=get_nr_embeddings(approaches.globals_sampling.freq_dict_exhaustive, approaches.globals_sampling.nr_iterations)
            nr_extra_embeddings=(overall_nr_emb - approaches.globals_sampling.sum_number_of_embeddings)
            
            self.FreqValue[approaches.globals_sampling.nr_iterations] = (nr_of_embeddings* len(self.root_nodes), overall_nr_emb_estimate)
            
            approaches.globals_sampling.sum_number_of_embeddings_aux+=Decimal(overall_nr_emb_estimate)
            approaches.globals_sampling.sum_squared_number_of_embeddings_aux+=Decimal(math.pow((overall_nr_emb_estimate), 2))
            
            approaches.globals_sampling.sum_number_of_embeddings+=Decimal(nr_extra_embeddings)
            approaches.globals_sampling.sum_of_the_square_embeddings+=Decimal(math.pow((nr_extra_embeddings), 2))
        return [approaches.globals_sampling.globalist_randomnode, approaches.globals_sampling.globaltimes_randomnode]
    
def get_nr_embeddings(freq_dict,iterations):
    nr_emb=0
    for k in freq_dict.keys():
        nr_emb+=freq_dict[k]
    return nr_emb
