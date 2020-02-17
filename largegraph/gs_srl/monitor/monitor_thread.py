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
            if(not(os.path.exists(os.path.join(output_path,'time_'+str(time_interval))))):
               os.mkdir(os.path.join(output_path,'time_'+str(time_interval)))
            infofile = open(os.path.join(output_path,'time_'+str(time_interval),'info.txt'),  'w')
            infofile.write("was running this for: %d seconds\n" % monitoring_time)
            infofile.write("Total number of observations: %d \n"  % nr_observed_nodes)
            infofile.write("Number of combinations: %d \n" % len(fdict_exhaustive))
            
            sum = 0
            for k in fdict_exhaustive.keys():
                sum = sum + fdict_exhaustive[k]
            infofile.write("Number of embeddings: %d \n" % sum)
            infofile.write("Frequencies in combinations:\n")
            
            flist = []
            for k in fdict_exhaustive.keys():
                flist.append(fdict_exhaustive[k])
            
            infofile.write("minimum: %d \n" % min(flist))
            infofile.write("maximum: %d \n" % max(flist))
            infofile.write("mean: %d \n" % numpy.mean(flist))
            infofile.write("median: %d \n" % numpy.median(flist))
            infofile.write("root node id: %s \n" % Plist[0])
            infofile.close()
            timepickout = open("extime.pickle", 'wb')
            timepickout.close()
            self.workerSemaphore.release()
            
            
            
                              
            

