'''
Created on Mar 18, 2015
Class for performing exhaustive search
@author: irma
'''
from sampler_general_ex import *
import time
import pickle
import numpy
import networkx as nx
import sampling_utils as su
import matplotlib.pyplot as plt
import OBDsearch
import os
import graph_manipulator.visualization as vis
import random
import sched
import multiprocessing
import algorithms.exhaustive_approach_inf as exhaustive
import monitor_process.process_monitor
import threading
import report_results.report_exhaustive_approach as report
import report_results.exhaustive_report as full_report
from threading import Thread, Semaphore
from monitor_process import  monitor_thread
import argparse
import graph_manipulator.graph_analyzer as analyzer
import report_results.NoResults_exception as exc
import sys,timeit,logging
import sampling_utils as utils
import utils as ut
#from report_results import exhaustive_report as report


def my_excepthook(ex_cls, ex, tb):
    logging.critical(''.join(traceback.format_tb(tb)))
    logging.critical('{0}: {1}'.format(ex_cls, ex))

def get_nr_emb_within_time(data_graph_path,pattern_path,output_path,time_seconds):
    print "Exhaustive checkup ...."
    nr_emb=None
    monitoring_marks=utils.generate_monitoring_marks(time_seconds,time_seconds)
    
    data_graph=None
    try:
       data_graph=nx.read_gpickle(data_graph_path)
    except:
       data_graph=nx.read_gml(data_graph_path)
       
    number_of_nodes_in_data=len(data_graph)
    pattern=nx.read_gml(pattern_path)
    #vis.visualize_graph(pattern, "sat")
    #analyzer.add_values_in_pattern_for_graph_if_missing(pattern)
    output_path=os.path.join(output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    root_node_predicate_name=None #well, not predefined. Let the algorithm find it and denote it (its id in the pattern) 
    pattern_name=os.path.basename(pattern_path)[:-4]
    
#     logging.basicConfig(
#          level=logging.DEBUG,
#          filename=os.path.join(output_path,'error_exhaustive.log'),
#          filemode='w')
#     sys.excepthook = my_excepthook
    
    root_node=None  
    #first check if the root node is determined by some other algorithm
    if not os.path.exists(os.path.join(output_path,'root_node.dec')): 
        hist=analyzer.get_sorted_labels_by_occurence_frequency_in_graph(data_graph_path)
        root_node,root_node_predicate_name=ut.choose_root_node(pattern,root_node_predicate_name,hist)
        with open(os.path.join(output_path,'root_node.dec'),'w') as f:
            f.write(str(root_node)+" ")
            f.write(str(root_node_predicate_name)+"\n")
            f.write("Determined by exhaustive approach")
    else:
        #read root node from the file
        with open(os.path.join(output_path,'root_node.dec'),'r') as f:
            for line in f.readlines():
                root_node=int(line.split(" ")[0])
                root_node_predicate_name=str(line.split(" ")[1].rstrip().lstrip())
                break
    
    print "root node predicate name: ",root_node_predicate_name     
    #get root nodes
    root_nodes = [x for x in data_graph.nodes() if data_graph.node[x]['predicate']==root_node_predicate_name]
    print "Number of root nodes: ",len(root_nodes)
    
    #get OBD 
    print "Root node,",pattern.node[root_node]
    OBdecomp = OBDsearch.get_heuristic4_OBD(pattern, startNode = root_node)
    
    if OBdecomp==None:
        print "No ombdecomp!"
        no_obd_decomp=True
        with open(os.path.join(output_path,'no_obdecomp.info'),'w') as f:
            f.write("No OBDecomp!")
        OBdecomp=OBDsearch.get_flatList(pattern, startNode=root_node)
             
    #get ordered list from OBD
    Plist = [item for sublist in OBdecomp for item in sublist]
    print "Using OBD: %s" % str(OBdecomp)
    print "and Plist: %s" % str(Plist)
    print "monitoring marks: ",monitoring_marks
    start = timeit.default_timer()
    try:
        lock = threading.Lock()
        print "starting scheduler"
        s = sched.scheduler(time.time, time.sleep)
        e1=s.enter(0, 4,exhaustive.find_nr_emb,(data_graph,  pattern,  Plist,  root_nodes,output_path,lock))
        t = threading.Thread(target=s.run)
        t.daemon=True
        t.start()
        time.sleep(time_seconds)
        end=timeit.default_timer()
        print "Main finished after ",end-start,"seconds"
        freq_dict=experiments.globals.fdict_exhaustive_limited
        if len(freq_dict) == 0:
            nr_emb=None
        else:
           nr_emb = 0
           for k in freq_dict.keys():
              nr_emb = nr_emb + freq_dict[k]
    except Wrong_root_node as e:
        print "Exception for the node occurred!"
    return nr_emb

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-data_graph_path', metavar='N',help='path to data file')
    parser.add_argument('-pattern_path', metavar='N',help='path to data file')
    parser.add_argument('-output_path', metavar='N',help='path to data file')
    parser.add_argument('-redo', default=False,action='store_true',help='flag for denoting redoing of experiment for this pattern. By default False')
    parser.add_argument('-root_node_predicate_name',default=None, metavar='N',help='path to data file')
    parser.add_argument('-time_interval',default=300, type=int,metavar='N',help='marking interval')
    parser.add_argument('-max_time',default=36000, metavar='N',type=int,help='maximum running time')
    parser.add_argument('-write',default=True,action='store_false',help='save to file a pickle having all the embeddings')
    
    print "Running exhaustive approach"
    
    args = parser.parse_args()
    print "Writing pickles???",args.write
    command=su.make_command_string(sys.argv)
    #set monitoring mark util. Monitor every five minutes until the end of time :)
    monitoring_marks=utils.generate_monitoring_marks(args.time_interval,args.max_time)
    data_graph=None
    print "Loading data ..."
    try:
       data_graph=nx.read_gpickle(args.data_graph_path)
    except:
       data_graph=nx.read_gml(args.data_graph_path)
    print "Data loaded ..."
    number_of_nodes_in_data=len(data_graph)
    print "Number of nodes: ",number_of_nodes_in_data
    pattern=nx.read_gml(args.pattern_path)   

    #analyzer.add_values_in_pattern_for_graph_if_missing(pattern)
    output_path=os.path.join(args.output_path,'exhaustive_approach')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
#     logging.basicConfig(
#          level=logging.DEBUG,
#          filename=os.path.join(args.output_path,'error_exhaustive.log'),
#          filemode='w')
#     sys.excepthook = my_excepthook
    root_node_predicate_name=args.root_node_predicate_name #well, not predefined. Let the algorithm find it and denote it (its id in the pattern) 
    pattern_name=os.path.basename(args.pattern_path)[:-4]
    print "PATTERN NAME: ",pattern_name
    if(not(os.path.exists(output_path))):
      os.makedirs(output_path)
    
    #write down the calling commands
    with open(os.path.join(output_path,"command.comm"),"w") as f:
        f.write(command)
        
    #check if pattern invalid
    if utils.is_invalid(pattern):
        with open(os.path.join(output_path,"invalid.info"),"w") as f:
            f.write("Invalid pattern")
    #Check if the result exists for this pattern for exhaustive approach. If yes, and -redo set to False, don't redo the experiment and just exit
    if not args.redo:
        for file in os.listdir(output_path):
            if file.startswith("results_") or file.startswith("no_results"):
                print "Results already exists. Exiting ..."
                sys.exit()
    #writing input gml into output
    if(not os.path.exists(output_path)):
        os.makedirs(output_path)
    if not(os.path.exists(args.output_path+'/input_pattern.gml')):
        nx.write_gml(pattern, args.output_path+'/input_pattern.gml')
    #DETERMINING ROOT NODE
    root_node=None   
    print "Root node predicate name: ",root_node_predicate_name
    print "Exists? ",os.path.join(args.output_path,'root_node.dec'),os.path.exists(os.path.join(args.output_path,'root_node.dec'))
    if root_node_predicate_name!=None or not os.path.exists(os.path.join(args.output_path,'root_node.dec')): 
        hist=analyzer.get_sorted_labels_by_occurence_frequency_in_graph(args.data_graph_path)
        root_node,root_node_predicate_name=ut.choose_root_node(pattern,root_node_predicate_name,hist)
        with open(os.path.join(args.output_path,'root_node.dec'),'w') as f:
            f.write(str(root_node)+" ")
            f.write(str(root_node_predicate_name)+"\n")
            f.write("Determined by exhaustive approach")
    else:
        #read root node from the file
        with open(os.path.join(args.output_path,'root_node.dec'),'r') as f:
            for line in f.readlines():
                root_node=int(line.split(" ")[0])
                root_node_predicate_name=str(line.split(" ")[1].rstrip().lstrip())
                break
    print "root node predicate name: ",root_node_predicate_name     
    #get root nodes
    root_nodes = [x for x in data_graph.nodes() if data_graph.node[x]['predicate']==root_node_predicate_name]
    print "Number of root nodes: ",len(root_nodes)
    #get OBD 
    print "Root node id: ",root_node
    print "Root node,",pattern.node[root_node]
    OBdecomp = OBDsearch.get_heuristic4_OBD(pattern, startNode = root_node)
    if OBdecomp==None:
        print "No ombdecomp!"
        no_obd_decomp=True
        with open(os.path.join(output_path,'no_obdecomp.info'),'w') as f:
            f.write("No OBDecomp!")
        OBdecomp=OBDsearch.get_flatList(pattern, startNode=root_node)  
    #get ordered list from OBD
    Plist = [item for sublist in OBdecomp for item in sublist]
    print "Using OBD: %s" % str(OBdecomp)
    print "and Plist: %s" % str(Plist)
    print "monitoring marks: ",monitoring_marks
    start = timeit.default_timer()
    with open(os.path.join(output_path,"start.time"),"w") as f:
        f.write(time.strftime("%d/%m/%Y")+"\n")
        f.write(time.strftime("%H:%M:%S"))
    try:
        lock = threading.Lock()
        p=exhaustive.Exhaustive_sampling_inf(data_graph,  pattern,  Plist,  root_nodes,output_path,lock)
        m=None
        m=monitor_process.process_monitor.monitor_process_exhaustive(p,monitoring_marks,lock,output_path)
        mt = threading.Thread(target=m)
        mt.daemon=True
        mt.start()
        p.run()
        p.abort=True  
        end=timeit.default_timer()
        print "Main finished after ",end-start,"seconds"
        print "FINAL: Number of nodes observed: ",experiments.globals.temporary_observed
        print "Root node observe: ",experiments.globals.nr_root_nodes_observed_so_far,"out of: ",experiments.globals.nr_root_nodes
        if m.timeout:
            with open(output_path+"/timeout.info",'w') as f:
                f.write("exhaustive finished with timeout!")
        try:
            report.report_results_exhaustive(experiments.globals.freq_dict_exhaustive,experiments.globals.temporary_observed[0],p.output_path,start,end,Plist,pattern_name,number_of_nodes_in_data,args.write)
        except exc.NoResults_Exception as e:
            with open(output_path+"/no_results.info",'w') as f:
                print "fudicts is empty!: No results for this pattern: "+args.pattern_path
                f.write("no results for this pattern!, fudicts is empty!")
    except Wrong_root_node as e:
        print "Exception for the node occurred!"
    
    #write down per root node embeddings increment
    #print experiments.globals.root_node_embeddings
    #with open(output_path+"/per_node_emb_increment.csv",'w') as f:
    #    previous_value_emb=0
    #    for l in experiments.globals.root_node_embeddings:
    #        f.write(str(l[0])+","+str(l[1]-previous_value_emb)+","+str(l[2])+"\n")
    #        previous_value_emb=l[1]
    
    #write down reports
    if args.write==True:
        pickout = open(os.path.join(output_path,'monitoring_reports.pickle'), 'wb')
        pickle.dump(m.report_structures, pickout)
        pickout.close()
     
    #write down monitoring marks
    pickout = open(os.path.join(output_path,'monitoring_marks.pickle'), 'wb')
    pickle.dump(monitoring_marks, pickout)
    pickout.close()
    with open(os.path.join(output_path,"end.time"),"w") as f:
        f.write(time.strftime("%d/%m/%Y")+"\n")
        f.write(time.strftime("%H:%M:%S"))
    full_report.exhaustive_report(args.output_path,args.redo)
    

        



    

                    
    
    
