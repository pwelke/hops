'''
Created on Apr 13, 2015

@author: irma
'''
'''
    Report results - write the important statistics to the file
    '''
import numpy
import os,sys
import time  
import pickle
import copy,math
from NoResults_exception import NoResults_Exception
import experiments
    
def report_results_exhaustive(fdict_exhaustive,nr_observed_nodes,output_path,start,stop,Plist,pattern_name,number_of_nodes_in_data,write):
        if len(fdict_exhaustive) == 0:
            raise NoResults_Exception('no results for this pattern: fdict exhaustive is empty!!!')
        print "Reporting exhaustive ..."
        #result for exhaustive approach (to be read by sampling algorithms)
        infofile = open(os.path.join(output_path,'results_'+pattern_name+'.res'),  'w')
        infofile.write("Exhaustive procedure took %d seconds.\n" % int(stop-start))
        infofile.write("Total number of observations: %d \n"  % nr_observed_nodes)
        infofile.write("Number of combinations: %d \n" % len(fdict_exhaustive))
        infofile.write("Percentage of seen root nodes so far:"+str(experiments.globals.nr_root_nodes_observed_so_far/float(experiments.globals.nr_root_nodes))+"\n")
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
    
        picklename = os.path.join(output_path,"fdict_exhaustive_%s.pickle" %pattern_name)
        if write==True:
          pickout = open(picklename, 'wb')
          pickle.dump(fdict_exhaustive, pickout)
          pickout.close()
        
        timepickout = open(os.path.join(output_path,"extime.pickle"), 'wb')
        extime= []
        extime.append(stop-start)
        pickle.dump(extime, timepickout)
        timepickout.close()
        print "Finished: infoed and pickled"
        
def report_results_exhaustive_monitoring(monitoring_reports,monitoring_marks,output_path):
        print "Doing reporting ..."
        print "Nr reports: ",len(monitoring_reports)
        for i in xrange(0,len(monitoring_reports)):
            fdict_exhaustive=monitoring_reports[i].current_fdict
            nr_observed_nodes=monitoring_reports[i].number_of_observed_nodes
            #result for exhaustive approach (to be read by sampling algorithms)
            infofile = open(os.path.join(output_path,'res_time_'+str(monitoring_marks[i])+'.info'),  'w')
            infofile.write("Monitoring mark %d .\n" % monitoring_marks[i])
            try: #hmm I must have changed the format of nr_observed nodes to be a list at some point
                infofile.write("Total number of observations: %d \n"  % nr_observed_nodes)
            except:
                infofile.write("Total number of observations: %d \n"  % nr_observed_nodes[0])
            infofile.write("Number of combinations: %d \n" % len(fdict_exhaustive))
            infofile.write("Last seen root node: "+str(monitoring_reports[i].last_seen_root_node)+"\n")
            infofile.write("Nr root nodes:"+str(monitoring_reports[i].nr_root_nodes)+"\n")
            print monitoring_reports[i].nr_root_nodes_observed_so_far
            print monitoring_reports[i].nr_root_nodes
            infofile.write("Percentage of seen root nodes so far:"+str(monitoring_reports[i].nr_root_nodes_observed_so_far/float(monitoring_reports[i].nr_root_nodes))+"\n")
            
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
            if len(flist)>0:
              infofile.write("minimum: %d \n" % min(flist))
              infofile.write("maximum: %d \n" % max(flist))
              infofile.write("mean: %d \n" % numpy.mean(flist))
              infofile.write("median: %d \n" % numpy.median(flist))

def report_results_scheduler(fdict_exhaustive,nr_observed_nodes,monitoring_time,output_path,Plist,time_interval,pattern_name):
        print "time interval",time_interval
        #fdict_exhaustive=copy.deepcopy(fdict_exhaustive_orig)
        print "FDICT SIZE first: ",len(fdict_exhaustive)

        if(not(os.path.exists(os.path.join(output_path,'time_'+str(time_interval))))):
           os.makedirs(os.path.join(output_path,'time_'+str(time_interval)))
        infofile = open(os.path.join(output_path,'time_'+str(time_interval),'info.txt'),  'w')
        infofile.write("recorded ar: %d th minute\n" % monitoring_time)
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
        
        picklename = os.path.join(output_path,"fdict_exhaustive_%.pickle" %pattern_name)   
        pickout = open(picklename, 'wb')
        print "FDICT SIZE third: ",len(fdict_exhaustive) 
        #pickle.dump(copy.deepcopy(fdict_exhaustive), pickout)
        #pickout.close()     
        timepickout = open("extime.pickle", 'wb')
        extime= []
        timepickout.close()
        
        
        
def report_number_of_observations(nodes_observed,output_path,time_interval):
    if(not(os.path.exists(os.path.join(output_path,'time_'+str(time_interval))))):
           os.mkdir(os.path.join(output_path,'time_'+str(time_interval)))
    infofile = open(os.path.join(output_path,'time_'+str(time_interval),'info.txt'),  'w')
        
    infofile.write("Total number of observations: %d \n"  % nodes_observed)
    infofile.close()
            
