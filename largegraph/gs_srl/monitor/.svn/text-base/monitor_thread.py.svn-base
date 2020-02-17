'''
Created on Apr 16, 2015

@author: irma
'''
from threading import Thread, Semaphore
import sys  
import time,timeit
import report_results.report_exhaustive_approach as report
import threading
import numpy
import os  
import time  
import pickle
import copy

class Processor(Thread):
    def __init__(self, workerSemaphore, processorSemaphore,parent_process):
        super(Processor, self).__init__()
        self.workerSemaphore    = workerSemaphore
        self.processorSemaphore = processorSemaphore
        self.parent_process=parent_process
        
    def run(self):
        while True:
            # wait for the worker to finish
            self.processorSemaphore.acquire()
            time_interval=5
            fdict_exhaustive=self.parent_process.freq_dict
            output_path=self.parent_process.output_path
            monitoring_time=5
            nr_observed_nodes=self.parent_process.nodes_observed
            short_graph_file_name=self.parent_process.short_graph_file_name
            Plist=self.parent_process.Plist
            
            print "PROCESSOR TOOK SEMAPHORE",time_interval
            
            print "FDICT SIZE first: ",len(fdict_exhaustive)
    
            if(not(os.path.exists(os.path.join(output_path,'time_'+str(time_interval))))):
               os.mkdir(os.path.join(output_path,'time_'+str(time_interval)))
            infofile = open(os.path.join(output_path,'time_'+str(time_interval),'info.txt'),  'w')
            infofile.write("was running this for: %d seconds\n" % monitoring_time)
            infofile.write("Total number of observations: %d \n"  % nr_observed_nodes)
            print "FDICT SIZE third: ",len(fdict_exhaustive) 
            infofile.write("Number of combinations: %d \n" % len(fdict_exhaustive))
            
            sum = 0
            for k in fdict_exhaustive.keys():
                sum = sum + fdict_exhaustive[k]
            
            print "Number of embeddings: ",sum
            infofile.write("Number of embeddings: %d \n" % sum)
            infofile.write("Frequencies in combinations:\n")
            
            flist = []
            for k in fdict_exhaustive.keys():
                flist.append(fdict_exhaustive[k])
            
            print "Flist size: ",len(flist)
            infofile.write("minimum: %d \n" % min(flist))
            infofile.write("maximum: %d \n" % max(flist))
            infofile.write("mean: %d \n" % numpy.mean(flist))
            infofile.write("median: %d \n" % numpy.median(flist))
            infofile.write("root node id: %s \n" % Plist[0])
            print "Info done, now pickling..."              
            print "Written in: ",output_path
            infofile.close()
            
            picklename = os.path.join(output_path,"fdict_exhaustive_%s.pickle" % short_graph_file_name)   
            pickout = open(picklename, 'wb')
            print "FDICT SIZE third: ",len(fdict_exhaustive) 
            #pickle.dump(copy.deepcopy(fdict_exhaustive), pickout)
            #pickout.close()     
            timepickout = open("extime.pickle", 'wb')
            extime= []
            timepickout.close()
            
            
            self.workerSemaphore.release()
            
            
            
                              
            

