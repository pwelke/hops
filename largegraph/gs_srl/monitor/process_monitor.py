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
import approaches.globals_sampling,math
import pickle
import os
import traceback
import sampling_core.sampler_general_ex as smplr
#from approaches import furer_sampling_approach
#import algorithms.exhaustive_approach_inf as exhaustive
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
                    approaches.globals_sampling.abort=True
                    self.timeout=True
                    return
                time.clock()
                sleeping_interval=self.times[self.counter]-self.mark
                time.sleep(sleeping_interval)
                self.mark=self.times[self.counter]
                if self.p.abort==True:
                    return

                with self.lock:
                     approaches.globals_sampling.marking_exhaustive=True
                     freq_dict_copy=copy.deepcopy(approaches.globals_sampling.freq_dict_exhaustive)
                     nodes_observed_copy=copy.deepcopy(approaches.globals_sampling.temporary_observed)
                     approaches.globals_sampling.temporary_embeddings=[]
                     nr_emb_temp=0
                     for k in freq_dict_copy.keys():
                        nr_emb_temp = nr_emb_temp + freq_dict_copy[k]
                     report_structure=approaches.globals_sampling.Furer_reports(1, freq_dict_copy, nodes_observed_copy, self.times[self.counter], sleeping_interval)
                     self.report_structures.append(report_structure)
                     nr_emb_temp=0
                     for k in freq_dict_copy.keys():
                        nr_emb_temp = nr_emb_temp + freq_dict_copy[k]  
                     approaches.globals_sampling.marking_exhaustive=False
                     if self.output_path!=None:
                      pickout = open(os.path.join(self.output_path,'monitoring_reports.pickle'), 'wb')
                      pickle.dump(self.report_structures, pickout)
                      pickout.close()
                     self.p.freq_dict=copy.deepcopy(freq_dict_copy)
                     approaches.globals_sampling.temporary_embeddings=[]
                     approaches.globals_sampling.marking_exhaustive=False
                     
            except:
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
                 approaches.globals_sampling.abort=True
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
                total_freq_dict_copy = copy.deepcopy(approaches.globals_sampling.freq_dict_exhaustive)
                nodes_observed_copy=copy.deepcopy(self.p.nodes_observed)
                report_structure=approaches.globals_sampling.Furer_reports(self.p.current_iteration, total_freq_dict_copy, nodes_observed_copy, self.times[self.counter], sleeping_interval)
                self.report_structures.append(report_structure)
                if  self.write==True:
                    pickout = open(os.path.join(self.output_path,'monitoring_reports.pickle'), 'wb')
                    pickle.dump(self.report_structures, pickout)
                    pickout.close()
                #print "Nr iterations",approaches.globals.nr_iterations
                avg=0
                if approaches.globals_sampling.nr_iterations!=0:
                  avg= (float(Decimal(approaches.globals_sampling.sum_number_of_embeddings)) / approaches.globals_sampling.nr_iterations) * (approaches.globals_sampling.nr_root_nodes)
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
            if(self.p.abort==True):
                return
            #if the time for running is exceeded, set flag to the main process that it should finish
            if self.counter>=len(self.times):
                self.p.abort=True
                return
            time.clock()
            sleeping_interval=self.times[self.counter]-self.mark
            time.sleep(sleeping_interval)
            processing_time_start=time.time()
            self.mark=self.times[self.counter]
            if self.p.abort==True:
                return
            N=0
            if self.stop_at_selection_failure==True and N>=self.cutoff:
                #print "Pattern is not selected: ABORT MAIN PROCEDURE"
                self.successful_monitoring=False
                self.p.abort=True
                self.limit_exceeded=True
                return
                
            #we have to put some structures under the lock
            with self.lock:
                total_Zlist_dict_copy = copy.deepcopy(self.p.Zlist_dict)
                furer_dict=smplr.handle_quota_Furer(self.p.D,  self.p.P, total_Zlist_dict_copy,  [0,None], self.p.iteration_counter,self.thread_number)
                nodes_observed_copy=copy.deepcopy(self.p.nodes_observed)
                report_structure=approaches.globals_sampling.Furer_reports(self.p.current_iteration, furer_dict, nodes_observed_copy, self.times[self.counter], sleeping_interval)
                self.report_structures.append(report_structure)
                if self.write==True:
                    pickout = open(os.path.join(self.output_path,'monitoring_reports.pickle'), 'wb')
                    pickle.dump(self.report_structures, pickout)
                    pickout.close()
                nr_embeddings_temp=approaches.globals_sampling.embeddings_estimate
                self.nr_embeddings=nr_embeddings_temp

            if self.stop_at_selection_failure==True:
                if self.counter==(self.check_selection_on_nth_mark): #we count from zero
                    nr_embeddings_temp=approaches.globals_sampling.embeddings_estimate
                    self.nr_embeddings=nr_embeddings_temp
                    a= (Decimal(approaches.globals_sampling.sum_of_the_square_extra_embeddings) - (Decimal(math.pow(approaches.globals_sampling.sum_number_of_extra_embeddings, 2)) / approaches.globals_sampling.nr_iterations)) / (approaches.globals_sampling.nr_iterations - 1)
                    self.stdeviation=math.sqrt(a / (approaches.globals_sampling.nr_iterations - 1))
                    lower_bound=nr_embeddings_temp+3*self.stdeviation
                    upper_bound=nr_embeddings_temp-3*self.stdeviation
                    if self.ignore_upper_limit==True:
                        upper_bound=0
                    if lower_bound>=math.sqrt(self.nr_nodes_data_graph) and upper_bound<=self.nr_nodes_data_graph:
                        self.successful_monitoring=True
                        self.p.abort=True
                        return
                    else:
                        self.successful_monitoring=False
                        self.p.abort=True
                        return
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
                report_structure=approaches.globals_sampling.Furer_reports(self.p.current_iteration, furer_dict, nodes_observed_copy, self.times[self.counter], sleeping_interval)
                self.report_structures.append(report_structure)
                nr_embeddings_temp=0
                #print "sum of number of embeddings: ",approaches.globals.sum_number_of_embeddings
                #print "nr iterations",approaches.globals.nr_iterations

                if(approaches.globals_sampling.nr_iterations!=0):
                   nr_embeddings_temp= approaches.globals_sampling.sum_number_of_embeddings / approaches.globals_sampling.nr_iterations
                #print "Nr embeddings found at the mark at time point: ",self.counter*sleeping_interval," is ",nr_embeddings_temp

            #check if the result falls within the selection interval at 60th minute (after one hour). Since we mark time
            #after every five minutes, this is the 12th counter value
            if self.stop_at_selection_failure==True:
                if self.counter==(self.check_selection_on_nth_mark-1): #we count from zero
                    #get number of embeddings for the current result
                    #they are recorded in globals
                    a= approaches.globals_sampling.sum_of_the_square_embeddings - ((math.pow(approaches.globals_sampling.sum_number_of_embeddings, 2) / approaches.globals_sampling.nr_iterations))
                    #a=(nr_iterations[counter]*sum_of_squares[counter])-(math.pow(sum_of_embeddings[counter], 2))
                    stdeviation=math.sqrt(a / (approaches.globals_sampling.nr_iterations - 1))
                    #print "Check if pattern can be selected at: ",self.times[self.counter]
                    #print "Standard deviation: ",stdeviation
                    #print "Nr nodes in data graph: ",self.nr_nodes_data_graph
                    nr_embeddings= approaches.globals_sampling.sum_number_of_embeddings / approaches.globals_sampling.nr_iterations
                    #print "Nr embeddings estimate: ",nr_embeddings
                    #print "lower bound: ",math.sqrt(self.nr_nodes_data_graph)-3*stdeviation
                    #print "Upper bound: ",self.nr_nodes_data_graph+3*stdeviation
                    if nr_embeddings>math.sqrt(self.nr_nodes_data_graph)-3*stdeviation and nr_embeddings<self.nr_nodes_data_graph+3*stdeviation:
                        print("Pattern is selected: continue")
                    else:
                        print ("Pattern is not selected: ABORT MAIN PROCEDURE")
                        self.successful_monitoring=False
                        self.p.abort=True
                        #mark unsuccessful monitoring in order not to report it
                        return
            self.processing_time+=(time.time()-processing_time_start)
