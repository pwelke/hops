'''
Created on Mar 22, 2015

@author: irma
'''
'''
Created on Mar 22, 2015

@author: irma
'''
'''
Created on Mar 20, 2015

@author: irma
'''
from sampler_general_ex import *
import utils as u
import OBDsearch
import sampler_general_ex as sampler
import os
import numpy
import pickle
import sampling_utils as utils 
import itertools
import threading
import algorithms.false_furer_algorithm as false_furer
import monitor_process.process_monitor as monitor
import report_results.false_furer_report as report
import argparse
import graph_manipulator.graph_analyzer as analyzer
import sys,shutil
import algorithms.furer_algorithm as furer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-data_graph_path', metavar='N',help='path to data file')
    parser.add_argument('-pattern_path', metavar='N',help='path to data file')
    parser.add_argument('-output_path', metavar='N',help='path to data file')
    parser.add_argument('-exhaustive_approach_results_path', metavar='N',help='path to data file')
    parser.add_argument('-redo', default=False,action='store_true',help='flag for denoting redoing of experiment for this pattern. By default False')
    parser.add_argument('-runs',default=1, metavar='N',type=int,help='path to data file')
    parser.add_argument('-ignore', default=False,action='store_true',help='Ignore the fact that the patterns was not selected by short furer')
    parser.add_argument('-time_interval', metavar='N',type=int,help='time interval in seconds')
    parser.add_argument('-max_time', metavar='N',type=int,help='path to data file')
    parser.add_argument('-selected',default=False,action='store_true',help='do approximate approach only if the pattern is selected by the exhaustive approach')
    parser.add_argument('-s',default=False,action='store_true',help='use a fixed seed')
    parser.add_argument('-write',default=True,action='store_false',help='save to file a pickle having all the embeddings')

    args = parser.parse_args()
    experiments.globals.same_seed=args.s
    monitoring_marks=utils.generate_monitoring_marks(args.time_interval,args.max_time)    
    print "Performing false furer...."
    all_falsefurer_times = []
    falsefudicts = []
    pathname = os.path.dirname(sys.argv[0]) 
    command=su.make_command_string(sys.argv)
    data_graph=None
    try:
       data_graph=nx.read_gpickle(args.data_graph_path)
    except:
       data_graph=nx.read_gml(args.data_graph_path) 
    pattern=nx.read_gml(args.pattern_path)
    analyzer.add_values_in_pattern_for_graph_if_missing(pattern)
    output_path=os.path.join(args.output_path,"results_false_furer")
    pattern_file_name=os.path.basename(args.pattern_path)[0:-4]
    nr_nodes_data_graph=len(data_graph)
    

    #Redoing and deleting the existing results
    if args.redo==True and os.path.exists(output_path):
        print "We are redoing and deleting existing results"
        shutil.rmtree(output_path)
        
    #make the output path directory
    if(not(os.path.exists(output_path))):
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
    
     #check if the pattern is actually chosen by Furer approach
    print os.path.join(args.output_path,'selected.info')
    if not args.ignore and not os.path.exists(os.path.join(args.output_path,'selected.info')):
        print "The pattern was not selected by short-furer!"
        with open(os.path.join(args.output_path,'not_selected.info'),'w') as f:
            f.write(" The pattern was not selected by short Furer approach!")
            #shutil.rmtree(os.path.join(output_path,'n_limits'))
            #shutil.rmtree(os.path.join(output_path,'monitoring'))
        sys.exit()
    
    #check if there are target predicates / if not make the result invalid
    if analyzer.count_nr_target_predicates(pattern)==0:
        with open(os.path.join(output_path,"invalid.info"),'w') as f:
            print "No target predicates ..."
            f.write("No target predicates") 
            #sys.exit()
    
    
    
    #Check if the result exists for this pattern for false furer approach. If yes, and -redo set to False, don't redo the experiment and just exit
    if not args.redo:
        for file in os.listdir(output_path):
            if file.startswith("complete") or file.startswith("no_exhaustive_approach_results"):               
                print "Results already exists. Exiting ..."
                sys.exit()
    
    #check if pattern selected by exhaustive approach (if flag set). otherwise don't do it
    if args.selected==True and (os.path.exists(os.path.join(args.exhaustive_approach_results_path,'selected.info'))):
        with open(output_path+"/not_selected_by_exhaustive.info",'w') as f:
            f.write("The pattern in question was not selected by exhaustive algorithm w.r.t. selection criteria")
            sys.exit()

    #check if pattern invalid. if yes there is no point in calculation / calculate anyway for to be safe. but output file invalid.info
    if os.path.exists(os.path.join(args.pattern_path,"invalid.info")):
        print "Pattern is invalid... problem with sampling approaches"
        with open(os.path.join(output_path,"invalid.info"),"w") as f:
            f.write("invalid pattern "+args.pattern_path)
    
    #writing input gml into output
    if(not os.path.exists(output_path)):
        os.makedirs(output_path)
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
    
    all_randnode_times = []
    rndicts = []
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
    print "Number of NLIMIT values: ",len(NLIMIT_values)
    root_nodes = [x for x in data_graph.nodes() if data_graph.node[x]['predicate']==pattern.node[root_node]['predicate']]
    root_nodes=sorted(root_nodes)
    #get OBD 
    print "Root node: ",root_node,pattern.node[root_node]['predicate']
    print "Number of root nodes:",len(root_nodes)

    OBdecomp = OBDsearch.get_heuristic4_OBD(pattern, startNode = root_node)
    OBdecomp_false=None
    if OBdecomp!=None:
       OBdecomp_false = [[item] for sublist in OBdecomp for item in sublist]
    else:
       OBdecomp_false =OBDsearch.get_flatList(pattern, startNode=root_node)
    print "OBD: ",OBdecomp_false
    Plist = [item for sublist in OBdecomp_false for item in sublist]
    plot_result_dict = {}
    monitoring_reports={}
    average_time=0
    
    print "monitoring marks: ",monitoring_marks
    for i in range(args.runs):
        print "Run:",i
        lock = threading.Lock()
        start=time.time() 
        furer.Furer.running_bug_fixed_code=False 
        p=furer.Furer(data_graph,  pattern,  OBdecomp_false,  root_nodes,NLIMIT_values,output_path,lock,i,nr_embeddings)
        m=monitor.monitor_process_false_furer(p,monitoring_marks,lock,i,nr_nodes_data_graph,-1,False,args.write)
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
               f.write("Furer only run for 1 hour, and this pattern didn't fall into the selection interval") 
            sys.exit()     
        fdictionaries_falseFurer = experiments.globals.globalist_furer[i]
        times_falseFurer = experiments.globals.globaltimes_furer[i][1:]       # all without first element, which is absolute time of start
        all_falsefurer_times.append(times_falseFurer)
        falsefudicts.append(fdictionaries_falseFurer)
        monitoring_reports[i]=m.report_structures
    
    average_time=average_time/args.runs
    
    #write down fudicts
    if args.write==True:
        pickout = open(os.path.join(output_path,'fudicts.pickle'), 'wb')
        pickle.dump(falsefudicts, pickout)
        pickout.close()
        
        #write down monitoring reports
        pickout = open(os.path.join(output_path,'monitoring_reports.pickle'), 'wb')
        pickle.dump(monitoring_reports, pickout)
        pickout.close()
        
    #write down furer times
    pickout = open(os.path.join(output_path,'all_furer_times.pickle'), 'wb')
    pickle.dump(all_falsefurer_times, pickout)
    pickout.close()
    
    
    #write down monitoring marks
    pickout = open(os.path.join(output_path,'monitoring_marks.pickle'), 'wb')
    pickle.dump(monitoring_marks, pickout)
    pickout.close()
    
    #write down Plist
    pickout = open(os.path.join(output_path,'Plist.pickle'), 'wb')
    pickle.dump(Plist, pickout)
    pickout.close()
    
    with open(output_path+"/average_running_time.time",'w') as f:
        f.write("Average running time over" +str(args.runs)+" runs: "+str(average_time)+" seconds\n")
    
    #report.report_monitoring(monitoring_marks,output_path,detailed_result_path,monitoring_reports,args.exhaustive_approach_results_path,data_graph,pattern,Plist,args.runs,pattern_file_name)    #print monitoring_reports    
    #report.report(output_path,detailed_result_NLIMIT_path,falsefudicts,plot_result_dict,all_falsefurer_times,args.exhaustive_approach_results_path,data_graph,pattern,Plist,NLIMIT_values,args.runs,pattern_file_name,experiments.globals.nlimit_iteration_counter,experiments.globals.nlimit_nr_embeddings)
    print "False Furer finished"
    with open(output_path+"/complete.info",'w') as f:
        f.write("All reporting completed")
    
    report.main(args.output_path,args.data_graph_path,args.redo,args.write,monitoring_reports)
       
