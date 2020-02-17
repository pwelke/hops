'''
Created on Apr 15, 2015

@author: irma
'''
import time
import timeit
import threading
import report_results.report_exhaustive_approach as report
import report_results.report_furer_approach as report_furer
import copy
import experiments.globals,math
import pickle
import os
import traceback
import experiments.sampler_general_ex as smplr
from experiments import furer_sampling_approach
import algorithms.exhaustive_approach_inf as exhaustive
from decimal import Decimal, getcontext

class monitor_process_exhaustive:
    counter=-1
    times=[]
    lock=None
    mark=0
    report_structures=[]
    output_path=None
    timeout=False
    
    def __init__(self,p,monitoring_marks,lock,output_path):
        self.p = p
        self.lock=lock
        self.times=monitoring_marks
        self.report_structures=[]
        self.output_path=output_path
        
    def __call__(self):
        while True:
            try:
                self.counter+=1
                if(self.p.abort==True):
                    return
                if self.counter>=len(self.times):
                    self.p.abort=True
                    experiments.globals.abort=True
                    self.timeout=True
                    return
                
                start_time_monitor=time.time()
                time.clock()
                sleeping_interval=self.times[self.counter]-self.mark
                time.sleep(sleeping_interval)
                processing_time_start=time.time()
                self.mark=self.times[self.counter]
                if self.p.abort==True:
                    return
                #print "slept for: ",sleeping_interval, " noting results"
               
                #Not marking anything now
                with self.lock:
                     experiments.globals.marking_exhaustive=True
                     freq_dict_copy=copy.deepcopy(experiments.globals.freq_dict_exhaustive)
                     nodes_observed_copy=copy.deepcopy(experiments.globals.temporary_observed)
                     mappings=copy.deepcopy(experiments.globals.temporary_embeddings)
                     experiments.globals.temporary_embeddings=[]
                     Plist_copy=copy.deepcopy(self.p.Plist)
                     #print "EMB BEFORE UPDATE:"
                     nr_emb_temp=0
                     for k in freq_dict_copy.keys():
                        nr_emb_temp = nr_emb_temp + freq_dict_copy[k]  
                     print nr_emb_temp
                     
                     #if not experiments.globals.main_exhaustive_reporting:
                         #print "Updating freq dict"
                         #print "Number of nodes observed: ",experiments.globals.temporary_observed
                         #print "Root node observe: ",experiments.globals.nr_root_nodes_observed_so_far,"out of: ",experiments.globals.nr_root_nodes
                         #print "Nr combination for this last observed root node: ",experiments.globals.candidates
                         #print "Nr global emb before addition: (inside monitoring proces) ",experiments.globals.nr_embeddings_exhaustive 
                     report_structure=experiments.globals.Furer_reports(1,freq_dict_copy,nodes_observed_copy,self.times[self.counter],sleeping_interval)
                     self.report_structures.append(report_structure)
                     nr_emb_temp=0
                     for k in freq_dict_copy.keys():
                        nr_emb_temp = nr_emb_temp + freq_dict_copy[k]  
                     #print "counter: ",self.counter,sleeping_interval
                     #print "Nr embeddings found at the mark at time point: ",(self.counter+1)*sleeping_interval," is ",nr_emb_temp
                     experiments.globals.marking_exhaustive=False
                     pickout = open(os.path.join(self.output_path,'monitoring_reports.pickle'), 'wb')
                     pickle.dump(self.report_structures, pickout)
                     pickout.close()
                     self.p.freq_dict=copy.deepcopy(freq_dict_copy)
                     experiments.globals.temporary_embeddings=[]
                     #print "Nr emb exhaustive: ",experiments.globals.nr_embeddings_exhaustive
                     experiments.globals.marking_exhaustive=False
                     
            except:
                #print "error"
                traceback.print_exc()
    
class monitor_process_random_vertex:
    counter=0
    lock=None
    mark=0
    processing_time=0
    report_structures=None
    times=None
    thread=None
    check_selection_on_nth_mark=-1
    successful_monitoring=True
    stop_at_selection_failure=True
    nr_nodes_data_graph=-1
    nr_embeddings=-1
    stdeviation=-1
    nr_embeddings_lower_bound=-1
    output_path=None
    write=True
    
    
    def __init__(self,p,monitoring_marks,lock,thread,nr_nodes_data_graph,check_selection_on_nth_mark,stop_on_selection_failure_flag,output_path,write):
        self.p = p
        self.lock=lock
        self.times=monitoring_marks
        self.report_structures=[]
        self.thread=thread
        self.nr_nodes_data_graph=nr_nodes_data_graph
        self.check_selection_on_nth_mark=check_selection_on_nth_mark
        self.stop_at_selection_failure=stop_on_selection_failure_flag
        self.output_path=output_path
        self.write=write
        
    def __call__(self):
        while True:
            #if the process we are following finished, we don't run the monitor anymore
            if(self.p.abort==True):
                return
            
            #if the time for running is exceeded, set flag to the main process that it should finish
            if self.counter>=len(self.times):
                 self.p.abort=True
                 experiments.globals.abort=True
                 self.timeout=True
                 return
            
                   
            
            #otherwise, let the main process run for a designated time
            start_time_monitor=time.time()
            time.clock()
            #print "counter: ",self.counter
            #print self.counter,"out of",len(self.times)," marks"
            sleeping_interval=self.times[self.counter]-self.mark
            time.sleep(sleeping_interval)
            #print "Slept for ",sleeping_interval," seconds"
            processing_time_start=time.time()
            self.mark=self.times[self.counter]
            with self.lock:
                total_freq_dict_copy = copy.deepcopy(experiments.globals.freq_dict_exhaustive)
                nodes_observed_copy=copy.deepcopy(self.p.nodes_observed)
                report_structure=experiments.globals.Furer_reports(self.p.current_iteration,total_freq_dict_copy,nodes_observed_copy,self.times[self.counter],sleeping_interval)
                self.report_structures.append(report_structure)
                if  self.write==True:
                    pickout = open(os.path.join(self.output_path,'monitoring_reports.pickle'), 'wb')
                    pickle.dump(self.report_structures, pickout)
                    pickout.close()
                #print "Nr iterations",experiments.globals.nr_iterations
                avg=0
                if experiments.globals.nr_iterations!=0:
                  avg=(float(Decimal(experiments.globals.sum_number_of_embeddings))/experiments.globals.nr_iterations)*(experiments.globals.nr_root_nodes)
                #print "Estimated number of embeddings: ",avg

            self.processing_time+=(time.time()-processing_time_start)
            self.counter+=1
    
def get_nr_embeddings(freq_dict,iterations):
        nr_emb=0
        for k in freq_dict.keys():
            nr_emb+=freq_dict[k]
        return nr_emb            
'''
Class for monitoring furer process. This thread will let the main thread (furer algorithm) run for 
a designated number of seconds and then save some desired states of the algorithm. For instance, here
we calculate the frequencies and number of observed nodes within the time limit.
'''
class monitor_process_furer:
    counter=-1
    times=None
    lock=None
    mark=0
    report_structures=None
    processing_time=0
    thread_number=-1
    nr_nodes_data_graph=-1
    check_selection_on_nth_mark=-1
    successful_monitoring=True
    stop_at_selection_failure=True
    nr_embeddings=-1
    stdeviation=-1
    selected_patterns_info_file=None
    cutoff=-1
    output_path=None
    ignore_upper_limit=False
    write=True
    
    def __init__(self,p,monitoring_marks,lock,thread_number,nr_nodes_data_graph,check_selection_on_nth_mark,stop_on_selection_failure_flag,selected_patterns_info_file,cutoff,output_path,iu,write):
        self.p = p
        self.lock=lock
        self.report_structures=[]
        self.times=monitoring_marks
        self.thread_number=thread_number
        self.nr_nodes_data_graph=nr_nodes_data_graph
        self.check_selection_on_nth_mark=check_selection_on_nth_mark
        self.stop_at_selection_failure=stop_on_selection_failure_flag
        self.selected_patterns_info_file=selected_patterns_info_file
        self.cutoff=cutoff
        self.output_path=output_path
        self.limit_exceeded=False
        self.ignore_upper_limit=iu
        self.write=write

    def __call__(self):
        while True:
            self.counter+=1
            #print self.counter,"th mark"," out of",len(self.times)
            #if the process we are following finished, we don't run the monitor anymore
            if(self.p.abort==True):
                return
            
            #if the time for running is exceeded, set flag to the main process that it should finish
            if self.counter>=len(self.times):
                #print "TIMEOUT!"
                self.p.abort=True
                return
            
            #otherwise, let the main process run for a designated time
            start_time_monitor=time.time()
            time.clock()
            sleeping_interval=self.times[self.counter]-self.mark
            time.sleep(sleeping_interval)
            processing_time_start=time.time()
            self.mark=self.times[self.counter]
            if self.p.abort==True:
                return
            #print "slept for: ",sleeping_interval, " noting results"  
            #check if cutoff exceeded - if yes, abort the execution and mark monitoring false
            N=furer_sampling_approach.get_current_selected_patterns(self.selected_patterns_info_file, self.cutoff)
            #print "Already selected patterns,",N," cutoff: ",self.cutoff
            if self.stop_at_selection_failure==True and N>=self.cutoff:
                #print "Pattern is not selected: ABORT MAIN PROCEDURE"
                self.successful_monitoring=False
                self.p.abort=True
                self.limit_exceeded=True
                return
                
            #we have to put some structures under the lock
            with self.lock:
                #print "Monitor recording ...."
                total_Zlist_dict_copy = copy.deepcopy(self.p.Zlist_dict)
                furer_dict=smplr.handle_quota_Furer(self.p.D,  self.p.P, total_Zlist_dict_copy,  [0,None], self.p.iteration_counter,self.thread_number)
                nodes_observed_copy=copy.deepcopy(self.p.nodes_observed)
                report_structure=experiments.globals.Furer_reports(self.p.current_iteration,furer_dict,nodes_observed_copy,self.times[self.counter],sleeping_interval)
                self.report_structures.append(report_structure)
                #print "Adding reports. Number of reports now: ",len(self.report_structures)
                #save intermediate structure just in case
                    #write down monitoring reports
                if self.write==True:
                    pickout = open(os.path.join(self.output_path,'monitoring_reports.pickle'), 'wb')
                    pickle.dump(self.report_structures, pickout)
                    pickout.close()
                nr_embeddings_temp=experiments.globals.embeddings_estimate
                self.nr_embeddings=nr_embeddings_temp
                #print "nr observed nodes: ",nodes_observed_copy
                #print "Nr iterations: ",experiments.globals.nr_iterations
                #print "Nr embeddings found at the mark at time point: ",self.counter*sleeping_interval," is ",nr_embeddings_temp
                #print experiments.globals.sum_of_the_square_extra_embeddings
                #print (Decimal(math.pow(experiments.globals.sum_number_of_extra_embeddings, 2))/experiments.globals.nr_iterations)
                #a=(Decimal(experiments.globals.sum_of_the_square_extra_embeddings)-(Decimal(math.pow(experiments.globals.sum_number_of_extra_embeddings, 2))/experiments.globals.nr_iterations))/(experiments.globals.nr_iterations-1)
                #self.stdeviation=math.sqrt(a/(experiments.globals.nr_iterations-1))
                #lower_bound=nr_embeddings_temp+3*self.stdeviation
                #upper_bound=nr_embeddings_temp-3*self.stdeviation
                #print "Lower bound: ",lower_bound,lower_bound>=math.sqrt(self.nr_nodes_data_graph)
                #print "Upper bound: ",upper_bound,upper_bound<=self.nr_nodes_data_graph
                #print "Nr nodes in the data graph: ",self.nr_nodes_data_graph
                #print "Selectable w.r.t. upper bound? ",upper_bound<=self.nr_nodes_data_graph
                #print "Standard deviation: ",self.stdeviation

            #check if the result falls within the selection interval at 60th minute (after one hour). Since we mark time
            #after every five minutes, this is the 12th counter value
            #print "Stop at selection? ",self.stop_at_selection_failure
            if self.stop_at_selection_failure==True:
                #print self.counter,self.check_selection_on_nth_mark
                if self.counter==(self.check_selection_on_nth_mark): #we count from zero
                    #get number of embeddings for the current result
                    #they are recorded in globals
                    #print "Check if pattern can be selected at: ",self.times[self.counter]
                    #print "Nr nodes in data graph: ",self.nr_nodes_data_graph
                    nr_embeddings_temp=experiments.globals.embeddings_estimate
                    self.nr_embeddings=nr_embeddings_temp
                    #print "nr observed nodes: ",nodes_observed_copy
                    #print "Nr iterations: ",experiments.globals.nr_iterations
                    #print "Nr embeddings found at the mark at time point: ",self.counter*sleeping_interval," is ",nr_embeddings_temp
                    a=(Decimal(experiments.globals.sum_of_the_square_extra_embeddings)-(Decimal(math.pow(experiments.globals.sum_number_of_extra_embeddings, 2))/experiments.globals.nr_iterations))/(experiments.globals.nr_iterations-1)
                    self.stdeviation=math.sqrt(a/(experiments.globals.nr_iterations-1))
                    #print "Standard deviation: ",self.stdeviation
                    #print "Nr iterations: ",experiments.globals.nr_iterations
                    #print "upper bound: ",math.sqrt(self.nr_nodes_data_graph)-3*self.stdeviation
                    #print "lower bound: ",self.nr_nodes_data_graph+3*self.stdeviation
                    lower_bound=nr_embeddings_temp+3*self.stdeviation
                    upper_bound=nr_embeddings_temp-3*self.stdeviation
                    if self.ignore_upper_limit==True:
                        upper_bound=0
                    if lower_bound>=math.sqrt(self.nr_nodes_data_graph) and upper_bound<=self.nr_nodes_data_graph:
                        #print "Pattern is selected: continue"
                        self.successful_monitoring=True
                        self.p.abort=True
                        return
                    else:
                        #print "Pattern is not selected: ABORT MAIN PROCEDURE"
                        self.successful_monitoring=False
                        self.p.abort=True
                        #mark unsuccessful monitoring in order not to report it
                        return
                print "continue"
            self.processing_time+=(time.time()-processing_time_start)

class monitor_process_false_furer:
    counter=-1
    times=None
    lock=None
    mark=0
    report_structures=None
    processing_time=0
    thread_number=-1
    check_selection_on_nth_mark=-1
    successful_monitoring=True
    stop_at_selection_failure=True
    nr_nodes_data_graph=-1
    write=True
    
    def __init__(self,p,monitoring_marks,lock,thread_number,nr_nodes_data_graph,check_selection_on_nth_mark,stop_on_selection_failure_flag,write):
        self.p = p
        self.lock=lock
        self.report_structures=[]
        self.times=monitoring_marks
        self.thread_number=thread_number
        self.check_selection_on_nth_mark=check_selection_on_nth_mark
        self.stop_at_selection_failure=stop_on_selection_failure_flag
        self.nr_nodes_data_graph=nr_nodes_data_graph
        self.write=write

    def __call__(self):
        while True:
            self.counter+=1
            #if the process we are following finished, we don't run the monitor anymore
            if(self.p.abort==True):
                return
            
            #if the time for running is exceeded, set flag to the main process that it should finish
            if self.counter>=len(self.times):
                self.p.abort=True
                return
            
            #otherwise, let the main process run for a designated time
            start_time_monitor=time.time()
            sleeping_interval=self.times[self.counter]-self.mark
            time.sleep(sleeping_interval)
            #print "Slept for: ",sleeping_interval
            #print "Stop at selection?",self.stop_at_selection_failure
            processing_time_start=time.time()
            self.mark=self.times[self.counter]
            
            #we have to put some structures under the lock
            with self.lock:
                total_Zlist_dict_copy = copy.deepcopy(self.p.Zlist_dict)
                furer_dict=smplr.handle_quota_Furer(self.p.D,  self.p.P, total_Zlist_dict_copy,  [0,None], self.p.iteration_counter,self.thread_number)
                nodes_observed_copy=copy.deepcopy(self.p.nodes_observed)
                #print "Nodes observed: ",nodes_observed_copy
                report_structure=experiments.globals.Furer_reports(self.p.current_iteration,furer_dict,nodes_observed_copy,self.times[self.counter],sleeping_interval)
                self.report_structures.append(report_structure)
                nr_embeddings_temp=0
                #print "sum of number of embeddings: ",experiments.globals.sum_number_of_embeddings
                #print "nr iterations",experiments.globals.nr_iterations

                if(experiments.globals.nr_iterations!=0):
                   nr_embeddings_temp=experiments.globals.sum_number_of_embeddings/experiments.globals.nr_iterations
                #print "Nr embeddings found at the mark at time point: ",self.counter*sleeping_interval," is ",nr_embeddings_temp

            #check if the result falls within the selection interval at 60th minute (after one hour). Since we mark time
            #after every five minutes, this is the 12th counter value
            if self.stop_at_selection_failure==True:
                if self.counter==(self.check_selection_on_nth_mark-1): #we count from zero
                    #get number of embeddings for the current result
                    #they are recorded in globals
                    a=experiments.globals.sum_of_the_square_embeddings-((math.pow(experiments.globals.sum_number_of_embeddings, 2)/experiments.globals.nr_iterations))
                    #a=(nr_iterations[counter]*sum_of_squares[counter])-(math.pow(sum_of_embeddings[counter], 2))
                    stdeviation=math.sqrt(a/(experiments.globals.nr_iterations-1))
                    #print "Check if pattern can be selected at: ",self.times[self.counter]
                    #print "Standard deviation: ",stdeviation
                    #print "Nr nodes in data graph: ",self.nr_nodes_data_graph
                    nr_embeddings=experiments.globals.sum_number_of_embeddings/experiments.globals.nr_iterations
                    #print "Nr embeddings estimate: ",nr_embeddings
                    #print "lower bound: ",math.sqrt(self.nr_nodes_data_graph)-3*stdeviation
                    #print "Upper bound: ",self.nr_nodes_data_graph+3*stdeviation
                    if nr_embeddings>math.sqrt(self.nr_nodes_data_graph)-3*stdeviation and nr_embeddings<self.nr_nodes_data_graph+3*stdeviation:
                        print "Pattern is selected: continue"
                    else:
                        print "Pattern is not selected: ABORT MAIN PROCEDURE"
                        self.successful_monitoring=False
                        self.p.abort=True
                        #mark unsuccessful monitoring in order not to report it
                        return
            self.processing_time+=(time.time()-processing_time_start)
