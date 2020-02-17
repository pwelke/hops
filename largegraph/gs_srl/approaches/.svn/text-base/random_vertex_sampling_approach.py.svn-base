'''
Created on Mar 20, 2015

@author: irma
'''
import threading
from sampler_general_ex import *
import OBDsearch
import sampler_general_ex as sampler
import sampling_utils as utils
import os
import utils as u
import numpy
import pickle
import sampling_utils as su
import itertools
import algorithms.random_vertex_sampling as random
import monitor_process.process_monitor as monitor
import timeit
import unittest
from experiments.globals import *
import graph_manipulator.graph_analyzer as analyzer
import argparse
import report_results.random_report as report
import sys
from threading import Thread
import atexit
import shutil

def delete_running_file(path):
    os.remove(path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-data_graph_path', metavar='N',help='path to data file')
    parser.add_argument('-pattern_path', metavar='N',help='path to data file')
    parser.add_argument('-output_path', metavar='N',help='path to data file')
    parser.add_argument('-exhaustive_approach_results_path', metavar='N',help='path to data file')
    parser.add_argument('-runs', default=1, metavar='N',type=int,help='path to data file')
    parser.add_argument('-run_nr', metavar='N',type=int,default=-1,help='if running in parallel, then has some value, otherwise it is -1')
    parser.add_argument('-time_interval', default=300,metavar='N',type=int,help='time interval in seconds')
    parser.add_argument('-redo', default=False,action='store_true',help='flag for denoting redoing of experiment for this pattern. By default False')
    parser.add_argument('-ignore', default=False,action='store_true',help='Ignore the fact that the patterns was not selected by short furer')
    parser.add_argument('-max_time', default=36000,metavar='N',type=int,help='path to data file')
    parser.add_argument('-par', metavar='N',default=False,help='flag to denote parallel running of threads')
    parser.add_argument('-selected',default=False,action='store_true',help='do approximate approach only if the pattern is selected by the exhaustive approach')
    parser.add_argument('-write',default=True,action='store_false',help='save to file a pickle having all the embeddings')

    args = parser.parse_args()
    
    print "RUNNING RANDOM VERTEX APPROACH"
    pathname = os.path.dirname(sys.argv[0]) 
    command=su.make_command_string(sys.argv)

    monitoring_marks=utils.generate_monitoring_marks(args.time_interval,args.max_time)
    data_graph=None
    try:
       data_graph=nx.read_gpickle(args.data_graph_path)
    except:
       data_graph=nx.read_gml(args.data_graph_path) 
    print "Processing pattern: ",args.pattern_path
    pattern=nx.read_gml(args.pattern_path)
    analyzer.add_values_in_pattern_for_graph_if_missing(pattern)
    nr_nodes_data_graph=len(data_graph)
    
   
    if args.run_nr!=-1:
      output_path=os.path.join(args.output_path,'random_vertex_approach','run_'+str(args.run_nr))
    else:
      output_path=os.path.join(args.output_path,'random_vertex_approach')

    #writing input gml into output
    if(not os.path.exists(output_path)):
        os.makedirs(output_path)
    
    #write down the calling commands
    with open(os.path.join(output_path,"command.comm"),"w") as f:
        f.write(command)
    
    #check if pattern invalid
    if utils.is_invalid(pattern):
        with open(os.path.join(output_path,"invalid.info"),"w") as f:
            f.write("Invalid pattern")
        #stop execution: no point
        #sys.exit()
    
    #check if the pattern is actually selected by Furer
    if not args.ignore and not os.path.exists(os.path.join(args.output_path,'selected.info')):
        print "The pattern was not selected by short-furer! (in "+os.path.join(args.output_path,'selected.info')+")"
        with open(os.path.join(output_path,'not_selected.info'),'w') as f:
            f.write(" The pattern was not selected by short Furer approach!")
        #remove n_limits and monitoring folders (nothing to report there)
        #shutil.rmtree(os.path.join(output_path,'n_limits'))
        #shutil.rmtree(os.path.join(output_path,'monitoring'))
        sys.exit()
    
    #check if there are target predicates / if not make the result invalid
    if analyzer.count_nr_target_predicates(pattern)==0:
        with open(os.path.join(output_path,"invalid.info"),'w') as f:
            f.write("No target predicates") 
            print "No target predicates ..."
            #sys.exit()
    
    #check if pattern selected by exhaustive approach (if flag set). otherwise don't do it
    if args.selected==True and (os.path.exists(os.path.join(args.exhaustive_approach_results_path,'selected.info'))):
        with open(output_path+"/not_selected_by_exhaustive.info",'w') as f:
            print "The pattern in question was not selected by exhaustive algorithm w.r.t. selection criteria"
            f.write("The pattern in question was not selected by exhaustive algorithm w.r.t. selection criteria")
            sys.exit()
            
    pattern_file_name=os.path.basename(args.pattern_path)[:-4]
    detailed_result_path=os.path.join(output_path,"monitoring")
    detailed_result_NLIMIT_path=os.path.join(output_path,"n_limits")
    output_path_random=os.path.join(output_path)
    
    print "GENERAL OUTPUT PATH: ",output_path_random
    #create all the results directories (even if there is no result for exhaustive)
    if(not(os.path.exists(output_path_random))):
        os.makedirs(output_path_random)

    #Check if the result exists for this pattern for random approach. If yes, and -redo set to False, don't redo the experiment and just exit
    if not args.redo:
        for file in os.listdir(output_path_random):
            if file.startswith("complete"):
                print "Results already exists. Exiting ..."
                sys.exit()
            if  file.startswith("no_exhaustive_approach_results"):
                print "No exhaustive approach results. Exiting ..."
                sys.exit()

    nx.write_gml(pattern, output_path+'/input_pattern.gml')
    
    #choose or load root node and nr observations
    if not os.path.exists(os.path.join(args.output_path,'root_node.dec')):
        hist=analyzer.get_sorted_labels_by_occurence_frequency_in_graph(args.data_graph_path)
        root_node,root_predicate_name=u.choose_root_node(pattern,None,hist)
        with open(os.path.join(args.output_path,'root_node.dec'),'w') as f:
            f.write(str(root_node)+" "+root_predicate_name.rstrip().lstrip()+"\n")
            f.write("Chosen by furer during the selection ...")
    else: #else, it is not selection so root node was already decided by someone
        with open(os.path.join(args.output_path,'root_node.dec'),'r') as f:
            for line in f.readlines():
                root_node=int(line.split(" ")[0])
                root_node_predicate_name=str(line.split(" ")[1].rstrip().lstrip())
                break
    
    print "Pattern file name:",pattern_file_name
    print "Exhaustive result path: ",os.path.join(args.exhaustive_approach_results_path,'results_'+pattern_file_name+'.res')
  
    exhaustive_approach_results_file=os.path.join(args.exhaustive_approach_results_path,'results_'+pattern_file_name+'.res')
    all_randnode_times = []
    rndicts = []
      
    #IRMA: might be fixed later to another number 
    exhaustive_approach_results_file=os.path.join(args.exhaustive_approach_results_path,'results_'+pattern_file_name+'.res')
    if os.path.exists(exhaustive_approach_results_file):
        all_randnode_times = [] 
        NLIMIT_values,dummy,nr_embeddings=u.get_observation_intervals_and_root_node_id(exhaustive_approach_results_file) 
        print "Number of embeddings found by exhaustive: ",nr_embeddings
    else:
        interval_length=int(math.ceil((sys.maxint/15)))
        intervals=[1]
        for i in range(1,15):
            intervals.append(intervals[i-1]+interval_length+1)
        nr_embeddings=0
        NLIMIT_values=intervals
    
    #print "Number of NLIMIT values: ",len(NLIMIT_values)
    print "Number of embeddings found by exhaustive: ",nr_embeddings
    root_nodes = [x for x in data_graph.nodes() if data_graph.node[x]['predicate']==pattern.node[root_node]['predicate']]
    #get OBD 
    print "Number of root nodes: ",len(root_nodes)
    if len(root_nodes)==0:
       with open(os.path.join(output_path,"invalid.info"),"w") as f:
            f.write("There are no root nodes for this pattern")
            sys.exit()
        #get OBD 
    OBdecomp = OBDsearch.get_heuristic4_OBD(pattern, startNode = root_node)
    print OBdecomp
    print "Root node id: ",root_node
    print "Root node",pattern.node[root_node]
    print "Number of root nodes: ",len(root_nodes)
    print "OBdecomp",OBdecomp
    Plist=[]
    if OBdecomp==None:
        print "No ombdecomp!"
        no_obd_decomp=True
        with open(os.path.join(output_path,'no_obdecomp.info'),'w') as f:
            f.write("No OBDecomp!")
        OBdecomp=OBDsearch.get_flatList(pattern, startNode=root_node)
    #check if list flat
    flat_list=True
    for n in OBdecomp:
        if(len(n)!=1):
            flat_list=False
            break 
    Plist = [item for sublist in OBdecomp for item in sublist]
    plot_result_dict = {}    
    print "OBD Decomp: ",OBdecomp 
    #OBdecomp = OBDsearch.get_heuristic4_OBD(pattern, startNode = root_node)
    #get ordered list from OBD
    #Plist = [item for sublist in OBdecomp for item in sublist]
    plot_result_dict = {}
    monitoring_reports={}
    average_time=0
    parallel=args.par    
    #making running file
    with open(os.path.join(output_path,"running.info"),'w') as f:
        f.write("running") 
    atexit.register(delete_running_file, os.path.join(output_path,"running.info"))
    print "Monitoring marks: ",monitoring_marks
    #Threads run sequentially
    for i in range(args.runs):
            print 'RUN: ',i
            lock = threading.Lock()
            start=time.time()
            experiments.globals.output_path=output_path
            p=random.Random_vertex_sampling(data_graph,  pattern,  Plist,  root_nodes,NLIMIT_values,output_path,lock,i,nr_embeddings)
            m=None
            m=monitor.monitor_process_random_vertex(p,monitoring_marks,lock,i,nr_nodes_data_graph,-1,False,output_path,args.write)
            mt = threading.Thread(target=m)
            mt.daemon=True
            mt.start()
            p.run() 
            p.abort=True
            print "main finished"       
            end=time.time()     
            average_time+=end-start 
            #check if monitoring finished succesfully
            if m.successful_monitoring==False:
            #if not, no point to report. make a file to say that Furer finished before time
                with open(output_path+"/not_selected.info",'w') as f:
                    f.write("Random only run for 1 hour, and this pattern didn't fall into the selection interval") 
                #remove the running info
                os.remove(os.path.join(output_path,"running.info"))
                sys.exit()      
            fdictionaries_limited = experiments.globals.globalist_randomnode[i]
            times_limited = experiments.globals.globaltimes_randomnode[i][1:]   
            all_randnode_times.append(times_limited)
            rndicts.append(fdictionaries_limited)
            monitoring_reports[i]=m.report_structures
    
    average_time=average_time/args.runs
    
    
    if args.write==True:
        pickout = open(os.path.join(output_path,'rndicts.pickle'), 'wb')
        pickle.dump(rndicts, pickout)
        pickout.close()
        
          #write down monitoring reports
        pickout = open(os.path.join(output_path,'monitoring_reports.pickle'), 'wb')
        pickle.dump(monitoring_reports, pickout)
        pickout.close()
          
    pickout = open(os.path.join(output_path,'all_randnode_times.pickle'), 'wb')
    pickle.dump(all_randnode_times, pickout)
    pickout.close()
    
    #write down monitoring marks
    pickout = open(os.path.join(output_path,'monitoring_marks.pickle'), 'wb')
    pickle.dump(monitoring_marks, pickout)
    pickout.close()
    
    #write down Plist
    pickout = open(os.path.join(output_path,'Plist.pickle'), 'wb')
    pickle.dump(Plist, pickout)
    pickout.close()
    
    
    #with open(output_path+"/per_node_emb_increment.csv",'w') as f:
    #    previous_value_emb=0
    #    for l in experiments.globals.root_node_embeddings:
    #        f.write(str(l[0])+","+str(l[1]-previous_value_emb)+","+str(l[2])+"\n")
    #        previous_value_emb=l[1]
    
    with open(output_path+"/average_running_time.time",'w') as f:
        f.write("Average running time over" +str(args.runs)+" runs: "+str(average_time)+" seconds\n")
        f.write("NR LIMITS: "+str(len(NLIMIT_values)))
    #report.report(rndicts,all_randnode_times,NLIMIT_values,plot_result_dict,args.runs,detailed_result_NLIMIT_path,output_path_random,args.exhaustive_approach_results_path,pattern_file_name,experiments.globals.nlimit_nr_embeddings)
    print "Random finished"

    with open(output_path+"/complete.info",'w') as f:
        f.write("All reporting completed")
    report.main(args.output_path,args.data_graph_path,args.redo,"my",args.write,monitoring_reports)
    
    


           
