'''
Created on May 13, 2015

@author: irma
'''
import experiments
'''
Created on Apr 17, 2015

@author: irma
'''
nr_iterations=None
report=None
current_time_snapshot=-1
default_key=None
globaltimes_randomnode={}
globalist_randomnode={}
cqi={}
globalist_furer={}
globaltimes_furer={}
nodes_observed={}
nr_target_nodes_no_head=0
embeddings_estimate=0
same_seed=False
sum_number_of_embeddings=0
sum_of_the_square_embeddings=0

sum_number_of_extra_embeddings=0
sum_of_the_square_extra_embeddings=0

number_of_observed_nodes=0
nr_iterations=0
nlimit_iteration_counter=[]
nlimit_nr_embeddings=[]
output_path=None
fdict_exhaustive_limited=None
sum_number_of_embeddings_aux=0
sum_squared_number_of_embeddings_aux=0
population_mean_random=0
population_stdev_random=0
abort=False
marking_exhaustive=False
candidates=0
temporary_embeddings=[]
temporary_observed=[]
nr_embeddings_exhaustive=0
main_exhaustive_reporting=False
monitoring_exhaustive_reporting=False
nr_root_nodes=None
nr_root_nodes_observed_so_far=None
last_seen_root_node=None
freq_dict_exhaustive={}
root_node_embeddings=[]
freq_dict_tuple_count={}
root_node_samples={}
root_node_nr_samples={}
experiment_name=None
nr_values_for_head=None
nr_non_observed_combinations=None
valueTuples=None
all_possible_target_combinations=None
count_of_combination_values_for_head={}

class Furer_reports:
    iteration_number=-1
    current_fdict=None
    number_of_observed_nodes=-1
    recorded_at_time=-1
    duration=0
    sum_nr_embeddings=0
    sum_of_the_square_embeddings=0
    
    sum_nr_extra_embeddings=0
    sum_of_the_extra_square_embeddings=0
    
    nr_iterations=0
    sum_number_of_embeddings_random=0
    sum_of_the_square_embeddings_random=0
    
    population_mean_random=0
    population_stdev_random=0
    nr_root_nodes=None
    nr_root_nodes_observed_so_far=None
    last_seen_root_node=None
    embeddings_estimate=None
    
    def __init__(self,iteration_number,current_fdict,number_of_observed_nodes,recorded_at_time,duration):
        self.iteration_number=iteration_number
        self.current_fdict=current_fdict
        self.number_of_observed_nodes=number_of_observed_nodes
        self.recorded_at_time=recorded_at_time
        self.duration=duration
        self.sum_nr_embeddings=experiments.globals.sum_number_of_embeddings
        self.sum_of_the_square_embeddings=experiments.globals.sum_of_the_square_embeddings
        
        self.sum_nr_embeddings_aux=experiments.globals.sum_number_of_embeddings_aux
        self.sum_of_the_square_embeddings_aux=experiments.globals.sum_squared_number_of_embeddings_aux
        
        self.nr_iterations=experiments.globals.nr_iterations
        self.population_mean_random=experiments.globals.population_mean_random
        self.population_stdev_random=experiments.globals.population_stdev_random
        self.nr_root_nodes=experiments.globals.nr_root_nodes
        self.nr_root_nodes_observed_so_far=experiments.globals.nr_root_nodes_observed_so_far
        self.last_seen_root_node=experiments.globals.last_seen_root_node
        self.sum_nr_extra_embeddings=experiments.globals.sum_number_of_extra_embeddings
        self.sum_of_the_extra_square_embeddings=experiments.globals.sum_of_the_square_extra_embeddings
        self.embeddings_estimate=experiments.globals.embeddings_estimate
        
    def __repr__(self):
        return "furer data Iteration nr: "+str(self.iteration_number)+"Nr observed nodes: "+str(self.number_of_observed_nodes)+"recorded at time:"+str(self.recorded_at_time)+" duration "+str(self.duration) \
               +"sum nr embeddings: "+str(self.sum_nr_embeddings)+" sum of the square embeddings: "+str(self.sum_of_the_square_embeddings)+ " nr sampling iterations: "+str(self.nr_iterations)\
               #+" Aux. random: "+str(self.sum_nr_embeddings_aux)+ "Aux: suared: "+str(self.sum_of_the_square_embeddings_aux)
