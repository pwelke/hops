'''
Created on Apr 13, 2015

@author: irma
'''
'''
    Report results - write the important statistics to the file
    '''
import numpy
import os,sys
import pickle
from report_results import NoResults_exception
import approaches
    
def report_results_exhaustive(fdict_exhaustive,nr_observed_nodes,output_path,start,stop,Plist,pattern_name):
        if len(fdict_exhaustive) == 0:
            raise NoResults_exception('no results for this pattern: fdict exhaustive is empty!!!')
        infofile = open(os.path.join(output_path,'results_'+pattern_name+'.res'),  'w')
        infofile.write("Exhaustive procedure took %d seconds.\n" % int(stop-start))
        infofile.write("Total number of observations: %d \n"  % nr_observed_nodes)
        infofile.write("Number of combinations: %d \n" % len(fdict_exhaustive))
        infofile.write("Percentage of seen root nodes so far:" + str(approaches.globals_sampling.nr_root_nodes_observed_so_far / float(approaches.globals_sampling.nr_root_nodes)) + "\n")
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
        picklename = os.path.join(output_path,"%s.pickle" %pattern_name)
        pickout = open(picklename, 'wb')
        pickle.dump(fdict_exhaustive, pickout)
        pickout.close()
        
        timepickout = open(os.path.join(output_path,"extime.pickle"), 'wb')
        extime= []
        extime.append(stop-start)
        pickle.dump(extime, timepickout)
        timepickout.close()

def report_results_exhaustive_monitoring(monitoring_reports,monitoring_marks,output_path):
        for i in range(0,len(monitoring_reports)):
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
            infofile.write("Percentage of seen root nodes so far:"+str(monitoring_reports[i].nr_root_nodes_observed_so_far/float(monitoring_reports[i].nr_root_nodes))+"\n")

            sum = 0
            for k in fdict_exhaustive.keys():
                sum = sum + fdict_exhaustive[k]
            
            infofile.write("Number of embeddings: %d \n" % sum)
            infofile.write("Frequencies in combinations:\n")
            
            flist = []
            for k in fdict_exhaustive.keys():
                flist.append(fdict_exhaustive[k])
            if len(flist)>0:
              infofile.write("minimum: %d \n" % min(flist))
              infofile.write("maximum: %d \n" % max(flist))
              infofile.write("mean: %d \n" % numpy.mean(flist))
              infofile.write("median: %d \n" % numpy.median(flist))

def report_results_scheduler(fdict_exhaustive,nr_observed_nodes,monitoring_time,output_path,Plist,time_interval,pattern_name):
        if(not(os.path.exists(os.path.join(output_path,'time_'+str(time_interval))))):
           os.makedirs(os.path.join(output_path,'time_'+str(time_interval)))
        infofile = open(os.path.join(output_path,'time_'+str(time_interval),'info.txt'),  'w')
        infofile.write("recorded ar: %d th minute\n" % monitoring_time)
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
        
        picklename = os.path.join(output_path,"fdict_exhaustive_%.pickle" %pattern_name)   
        timepickout = open("extime.pickle", 'wb')
        timepickout.close()
        
        
        
def report_number_of_observations(nodes_observed,output_path,time_interval):
    if(not(os.path.exists(os.path.join(output_path,'time_'+str(time_interval))))):
           os.mkdir(os.path.join(output_path,'time_'+str(time_interval)))
    infofile = open(os.path.join(output_path,'time_'+str(time_interval),'info.txt'),  'w')
        
    infofile.write("Total number of observations: %d \n"  % nodes_observed)
    infofile.close()
            
