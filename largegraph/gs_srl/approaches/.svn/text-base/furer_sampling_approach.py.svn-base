'''
Created on Mar 22, 2015

@author: irma
'''
'''
Created on Mar 20, 2015

@author: irma
'''
import logging
import traceback
from sampler_general_ex import *
import utils as u
import OBDsearch
import sampler_general_ex as sampler
import os,shutil,time
import numpy,random
import pickle
import itertools
import threading
import algorithms.furer_algorithm as furer
from globals import *
import monitor_process.process_monitor
import report_results.furer_report as report
import argparse
import sampling_utils as utils
import graph_manipulator.graph_analyzer as analyzer
import sys
from threading import Thread
from experiments import sampler_general_ex as smplr
import multiprocessing as mp
import atexit
import algorithms.false_furer_algorithm as false_furer
import report_results.check_isomorphism_selected as isomorphism_check
import experiments.exhaustive_approach


def delete_running_file(path):
    os.remove(path)
    
def my_excepthook(ex_cls, ex, tb):
    logging.critical(''.join(traceback.format_tb(tb)))
    logging.critical('{0}: {1}'.format(ex_cls, ex))
 
def get_current_selected_patterns(selected_patterns_file,cutoff):
    nr=0
    with open(selected_patterns_file,'r') as f:
           nr = int(f.readlines()[0])
    return nr

def increase_number_of_selected_patterns(selected_patterns_file,N):
     new_number=N+1
     with open(selected_patterns_file,'w') as f:
         f.write(str(new_number)+"\n")
     
    
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-data_graph_path', metavar='N',help='path to data file')
    parser.add_argument('-pattern_path', metavar='N',help='path to data file')
    parser.add_argument('-output_path', metavar='N',help='path to data file')
    parser.add_argument('-pattern_level_results', metavar='N',help='path to general pattern file - not batch')
    parser.add_argument('-exhaustive_approach_results_path', metavar='N',help='path to data file')
    parser.add_argument('-runs',default=1, metavar='N',type=int,help='path to data file')
    parser.add_argument('-time_interval', default=300,metavar='N',type=int,help='time interval in seconds')
    parser.add_argument('-redo', default=False,action='store_true',help='flag for denoting redoing of experiment for this pattern. By default False')
    parser.add_argument('-max_time',default=36000,type=int,help='path to data file')
    parser.add_argument('-select_on',type=int,default=12,help='on which time mark interval would you like to select the pattern: default 12 - after 12*time_interval minutes')
    parser.add_argument('-selected',default=False,action='store_true',help='do approximate approach only if the pattern is selected by the exhaustive approach')
    parser.add_argument('-sample',default=False,action='store_true',help='if the flag is set, furer will be only run for one hour and it will be decided if the pattern is selected or not')
    parser.add_argument('-cutoff',default=100,type=int,help='number of patterns selected per level : default is 100')
    parser.add_argument('-preselection',default=False,action='store_true',help='do preselection; stop earlier; after 5 minutes')
    parser.add_argument('-s',default=False,action='store_true',help='use a fixed seed')
    parser.add_argument('-iu',default=False,action='store_true',help='ignore upper bound when selecting patterns')
    parser.add_argument('-write',default=True,action='store_false',help='save to file a pickle having all the embeddings')

   
    args = parser.parse_args()     
    experiments.globals.same_seed=args.s
    pre_selection_done=False   
    if not(args.preselection):
        pre_selection_done=True
    pathname = os.path.dirname(sys.argv[0]) 
    command=su.make_command_string(sys.argv)
    monitoring_marks=utils.generate_monitoring_marks(args.time_interval,args.max_time)
    all_furer_times = []
    fudicts = []
    no_obd_decomp=False
    data_graph=None
    print "Loading data ..."
    try:
      data_graph=nx.read_gpickle(args.data_graph_path)
    except:
      data_graph=nx.read_gml(args.data_graph_path)
    print "Loaded data"
    pattern=nx.read_gml(args.pattern_path)
    analyzer.add_values_in_pattern_for_graph_if_missing(pattern)
    output_path=os.path.join(args.output_path,"results_furer")
    experiments.globals.output_path=output_path
    
    pattern_file_name=os.path.basename(args.pattern_path)[:-4]
    nr_nodes_data_graph=len(data_graph)
    
    pattern_general_level=os.path.dirname(os.path.dirname(os.path.dirname(args.pattern_path)))
    print "Path general level: ",pattern_general_level
    
    pattern_level_results=None
    if args.pattern_level_results==None:
        pattern_level_results=os.path.dirname(os.path.dirname(args.output_path))
    else:
        pattern_level_results=args.pattern_level_results
    
    print pattern_level_results

    #Redoing and deleting the existing results
    if args.redo==True and os.path.exists(output_path):
        print "We are redoing and deleting existing results"
        print output_path
        shutil.rmtree(output_path)

    #make the output path directory
    if(not(os.path.exists(output_path))):
        os.makedirs(output_path)
        
    #check if selected_patterns.info exists. If not, create it
    if not os.path.exists(os.path.join(pattern_level_results,'selected_patterns.info')):
        with open(os.path.join(pattern_level_results,'selected_patterns.info'),'w') as f:
            f.write(str(0))
        
#     logging.basicConfig(
#          level=logging.DEBUG,
#          filename=os.path.join(args.output_path,'error_furer.log'),
#          filemode='w')
#     sys.excepthook = my_excepthook
     
    #check if pattern invalid
    if utils.is_invalid(pattern):
        print "Pattern is invalid"
        with open(os.path.join(output_path,"invalid.info"),"w") as f:
            f.write("Invalid pattern")
    
    #Override the flag: if flag one hour is set, but there exists selected.info or not selected.info in the main output folder,
    #then override one hour flag and set it to false so that full Furer can be done
    if args.redo==False and args.sample and (os.path.exists(os.path.join(args.output_path,'selected.info')) or  os.path.exists(os.path.join(args.output_path,'not_selected.info'))):
        args.sample=False
        if args.redo==False and not(args.sample) and not(os.path.exists(os.path.join(args.output_path,'selected.info')) or  os.path.exists(os.path.join(args.output_path,'not_selected.info'))):
           args.sample=True
    
    #check if preselection done for this pattern
    if args.preselection:
        if os.path.exists(os.path.join(args.output_path,'preselected.info')) or os.path.exists(os.path.join(args.output_path,'not_preselected.info')):
           pre_selection_done=True
    if args.preselection:
        if not args.redo and os.path.exists(os.path.join(args.output_path,'not_preselected.info')):
            print "This pattern is not preselected. Aborting Furer! Are you sure you're not supposed to disable preselection"
            sys.exit()
    
    #check if needed to run (experiments completed)
    if args.redo==False:
        print "no redo... exits?","sampling?",args.sample,os.path.join(args.output_path,'selected.info'),os.path.exists(os.path.join(args.output_path,'selected.info')),os.path.join(args.output_path,'not_selected.info'),os.path.exists(os.path.join(args.output_path,'not_selected.info'))
        if args.sample==True and ((os.path.exists(os.path.join(args.output_path,'selected.info')) or os.path.exists(os.path.join(args.output_path,'not_selected.info')))):
           print "Results already sampled. Pattern selected or not selected!"
           sys.exit()
        else:
            if os.path.exists(output_path+"/complete.info"):
                print "Results already sampled. Pattern selected or not selected!"
                sys.exit()
    
    #check if there are target predicates / if not make the result invalid
    if analyzer.count_nr_target_predicates(pattern)==0:
        with open(os.path.join(output_path,"invalid.info"),'w') as f:
            f.write("No target predicates") 
            print "No target predicates ..."
    
    #write down the calling commands
    with open(os.path.join(output_path,"command.comm"),"w") as f:
        f.write(command)

    #Check if the result exists for this pattern for furer approach. If yes, and -redo set to False, don't redo the experiment and just exit
    if not args.redo:
        for file in os.listdir(output_path):
            if not args.sample and (file.startswith("complete") or file.startswith("no_exhaustive_approach_results")):                
             print "Results already exist. Exiting ..."
             sys.exit()
    
    #check if pattern invalid. if yes there is no point in calculation / calculate anyway for to be safe. but output file invalid.info
    if os.path.exists(os.path.join(args.pattern_path,"invalid.info")):
        print "Pattern is invalid... problem with sampling approaches"
        with open(os.path.join(output_path,"invalid.info"),"w") as f:
            f.write("invalid pattern "+args.pattern_path)
 
     #writing input gml into output
    nx.write_gml(pattern, args.output_path+'/input_pattern.gml')
    
    #choose or load root node and nr observations
    desired_predicate=None
    print "Specified root node? ",os.path.join(args.output_path,'root_node.dec')
    if args.sample or not(os.path.exists(os.path.join(args.output_path,'root_node.dec'))):
        hist=analyzer.get_sorted_labels_by_occurence_frequency_in_graph(args.data_graph_path)
        root_node,root_predicate_name=u.choose_root_node(pattern,desired_predicate,hist)
        with open(os.path.join(args.output_path,'root_node.dec'),'w') as f:
            f.write(str(root_node)+" "+root_predicate_name.rstrip().lstrip()+"\n")
            f.write("Chosen by furer during the selection ...")
    else: #else, it is not selection so root node was already decided by someone
        with open(os.path.join(args.output_path,'root_node.dec'),'r') as f:
            for line in f.readlines():
                root_node=int(line.split(" ")[0])
                root_node_predicate_name=str(line.split(" ")[1].rstrip().lstrip())
                break
        
    #if it's not the selection phase it means the exhaustive approach is run, therefore read NLIMIT values from the file
    
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
    
    
    #get root nodes
    root_nodes = [x for x in data_graph.nodes() if data_graph.node[x]['predicate']==pattern.node[root_node]['predicate']]
    root_nodes=sorted(root_nodes)
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
    
    if flat_list:
        no_obd_decomp=True
        
    print "Running false Furer option? ",no_obd_decomp
    Plist = [item for sublist in OBdecomp for item in sublist]
    plot_result_dict = {}
    
    print "OBD Decomp: ",OBdecomp
    
    monitoring_reports={}
    average_time=0
    
    with open(os.path.join(output_path,"OBDDecomp.info"),'w') as f:
        f.write("OBDecomp:\n") 
        f.write(str(OBdecomp)+"\n")
    
    
    #making running file
    with open(os.path.join(output_path,"running.info"),'w') as f:
        f.write("running") 
        f.write(time.strftime("%c")+"\n")
    atexit.register(delete_running_file, os.path.join(output_path,"running.info"))
    
    
    if args.preselection and not(pre_selection_done):
        args.select_on=0
    print "Number of monitoring marks: ",len(monitoring_marks)
    print "Doing sampling? ",args.sample
    print "Doing preselection? ",args.preselection
    print "Is this pattern preselected? ",pre_selection_done
    print "Marking on which interval point?,",args.select_on
    print "Cutoff for pattern selection is: ",args.cutoff
    print "Monitoring marks: ",monitoring_marks

    for i in range(args.runs):
        if args.preselection and not(pre_selection_done):
            print "STARTED PRE-SELECTING"
        else:
            print "STARTED SAMPLING ..."
        lock = threading.Lock()
        start=time.time() 
        furer.Furer.running_bug_fixed_code=False 
        if no_obd_decomp:
          p=furer.Furer(data_graph,  pattern,  OBdecomp,  root_nodes,NLIMIT_values,output_path,lock,i,nr_embeddings)
        else:
          p=furer.Furer(data_graph,  pattern,  OBdecomp,  root_nodes,NLIMIT_values,output_path,lock,i,nr_embeddings)
        m=monitor_process.process_monitor.monitor_process_furer(p,monitoring_marks,lock,i,nr_nodes_data_graph,args.select_on,args.sample,os.path.join(pattern_level_results,'selected_patterns.info'),args.cutoff,output_path,args.iu,args.write)
        mt = threading.Thread(target=m)
        mt.daemon=True
        mt.start()
        p.run() 
        p.abort=True
        print "main finished"       
        end=time.time()
        average_time+=end-start
        #check if monitoring finished succesfully if the experiment is for one hour
        if args.sample:
            with open(os.path.join(output_path,'sampleFurer.info'),'w') as f:
                f.write("Performed selection by Furer at \n")
                f.write(time.strftime("%c")+"\n")               
            print m.successful_monitoring
            
            if m.successful_monitoring==False:
                #if monitoring not successful
                print "Monitoring not successful"
                if m.limit_exceeded==True:
                    with open(args.output_path+"/selected_patterns_lim.info",'w') as f:
                        f.write("Limit for selectable patterns is exceeded. Execution aborted.")
                if args.preselection:
                    if not(pre_selection_done):
                      with open(args.output_path+"/not_preselected.info",'w') as f:
                           f.write("Furer only run for 1 hour, and this pattern didn't fall into the selection interval \n") 
                           f.write("Estimated nr embeddings: "+str(m.nr_embeddings)+"\n")
                           f.write("Stdeviation: "+str(m.stdeviation)+"\n")
                           f.write("Nr nodes in data graph: "+str(m.nr_nodes_data_graph)+"\n")
                           f.write(time.strftime("%c")+"\n")
                           sys.exit()       
                with open(args.output_path+"/not_selected.info",'w') as f:
                       f.write("Furer only run for 1 hour, and this pattern didn't fall into the selection interval \n") 
                       f.write("Estimated nr embeddings: "+str(m.nr_embeddings)+"\n")
                       f.write("Stdeviation: "+str(m.stdeviation)+"\n")
                       f.write("Nr nodes in data graph: "+str(m.nr_nodes_data_graph)+"\n")
                       f.write(time.strftime("%c")+"\n")
                       sys.exit()
                        
            else: #else mark this result as selected by Furer in general path (where root node is)
                #check if selected patterns exceeds the cutoff capacity. If yes, make conditional select.
                #if not, mark the pattern as selected
                print "Monitoring successful!"
                #check if this selected pattern is isomorphic to some existing selected pattern
                #check if exhaustive has embeddings
                nr_emb_exh=None
                nr_emb_exh=experiments.exhaustive_approach.get_nr_emb_within_time(args.data_graph_path,args.pattern_path, args.output_path, 60);
                print "Number of exmbeddings by exhaustive: ",nr_emb_exh
                if nr_emb_exh==None:
                    with open(os.path.join(args.output_path,'problem_selected.info'),'w') as f:
                        f.write("Selected by Furer but not by exhaustive!...\n")
                        f.write("Estimated nr embeddings: "+str(m.nr_embeddings)+"\n")
                        f.write("Stdeviation: "+str(m.stdeviation)+"\n")
                        f.write("Nr nodes in data graph: "+str(m.nr_nodes_data_graph)+"\n")
                        f.write("Ran sampled furer: selection of patterns \n")
                        f.write("Pattern selected at: \n")
                        f.write(time.strftime("%c")+"\n")
                        sys.exit()     
                    
                if isomorphism_check.main(pattern_level_results,pattern_general_level,args.pattern_path):
                     with open(os.path.join(args.output_path,'isomorphic_selected.info'),'w') as f:
                        f.write("Selected by Furer but isomorphic with already selected ones...\n")
                        f.write("Estimated nr embeddings: "+str(m.nr_embeddings)+"\n")
                        f.write("Stdeviation: "+str(m.stdeviation)+"\n")
                        f.write("Nr nodes in data graph: "+str(m.nr_nodes_data_graph)+"\n")
                        f.write("Ran sampled furer: selection of patterns \n")
                        f.write("Pattern selected at: \n")
                        f.write(time.strftime("%c")+"\n")
                        sys.exit()
                          
                if args.preselection and not(pre_selection_done):
                    with open(os.path.join(args.output_path,'preselected.info'),'w') as f:
                        print "Pre-Selected pattern: writing to file: ",os.path.join(args.output_path,'selected.info')
                        f.write("Selected by Furer ...\n")
                        f.write("Estimated nr embeddings: "+str(m.nr_embeddings)+"\n")
                        f.write("Stdeviation: "+str(m.stdeviation)+"\n")
                        f.write("Nr nodes in data graph: "+str(m.nr_nodes_data_graph)+"\n")
                        f.write("Ran sampled furer: selection of patterns \n")
                        f.write("Pattern selected at: \n")
                        f.write(time.strftime("%c")+"\n")
                        sys.exit()   
                
                sleep_random_time=random.randint(3,25)
                time.sleep(sleep_random_time)
                if nr_emb_exh!=None:
                    with open(os.path.join(args.output_path,'selected.info'),'w') as f:
                            print "Selected pattern: writing to file: ",os.path.join(args.output_path,'selected.info')
                            f.write("Selected by Furer ...\n")
                            f.write("Estimated nr embeddings: "+str(m.nr_embeddings)+"\n")
                            f.write("Stdeviation: "+str(m.stdeviation)+"\n")
                            f.write("Nr nodes in data graph: "+str(m.nr_nodes_data_graph)+"\n")
                            f.write("Ran sampled furer: selection of patterns \n")
                            f.write("Pattern selected at: \n")
                            f.write(time.strftime("%c")+"\n")
                    N=get_current_selected_patterns(os.path.join(pattern_level_results,'selected_patterns.info'),args.cutoff)
                    if N>=args.cutoff:
                        if os.path.exists(os.path.join(args.output_path,'selected.info')):
                           os.remove(os.path.join(args.output_path,'selected.info'))
                        print "Capacity for selection exceeded .... informally selecting the pattern ..."
                        with open(os.path.join(args.output_path,'conditionally_selected.info'),'w') as f:
                            f.write("Selected by Furer but the number of selected patterns per level exceeded...\n")
                            f.write("Estimated nr embeddings: "+str(m.nr_embeddings)+"\n")
                            f.write("Stdeviation: "+str(m.stdeviation)+"\n")
                            f.write("Nr nodes in data graph: "+str(m.nr_nodes_data_graph)+"\n")
                            f.write("Ran sampled furer: selection of patterns \n")
                            f.write("Pattern selected at: \n")
                            f.write(time.strftime("%c")+"\n")
                            sys.exit()     
                    else:
                        print "Increasing the number of selected patterns"
                        increase_number_of_selected_patterns(os.path.join(pattern_level_results,'selected_patterns.info'),N)
                        with open(os.path.join(args.output_path,'selected.info'),'w') as f:
                            print "Selected pattern: writing to file: ",os.path.join(args.output_path,'selected.info')
                            f.write("Selected by Furer ...\n")
                            f.write("Estimated nr embeddings: "+str(m.nr_embeddings)+"\n")
                            f.write("Stdeviation: "+str(m.stdeviation)+"\n")
                            f.write("Nr nodes in data graph: "+str(m.nr_nodes_data_graph)+"\n")
                            f.write("Ran sampled furer: selection of patterns \n")
                            f.write("Pattern selected at: \n")
                            f.write(time.strftime("%c")+"\n")
                            sys.exit()
                 
        fdictionaries_Furer = experiments.globals.globalist_furer[i]
        times_Furer = experiments.globals.globaltimes_furer[i][1:] 
        all_furer_times.append(times_Furer)
        fudicts.append(fdictionaries_Furer)
        print "Monitoring report: ",m.report_structures
        monitoring_reports[i]=m.report_structures      
    
    average_time=average_time/args.runs
    print "Do we save fudicts and monitoring reports?",args.write
    if args.write==True:
        #write down fudicts
        pickout = open(os.path.join(output_path,'fudicts.pickle'), 'wb')
        pickle.dump(fudicts, pickout)
        pickout.close()
        
        
        #write down monitoring reports
        pickout = open(os.path.join(output_path,'monitoring_reports.pickle'), 'wb')
        pickle.dump(monitoring_reports, pickout)
        pickout.close()
        
        
        
        #write down furer times
        pickout = open(os.path.join(output_path,'all_furer_times.pickle'), 'wb')
        pickle.dump(all_furer_times, pickout)
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
        f.write("Average running time over" +str(args.runs)+" runs: "+str(average_time)+" seconds\n")        #handle exhaustive approach results / pickle and stuff
    if args.sample==False:
        with open(output_path+"/complete.info",'w') as f:
            f.write("All reporting completed")
    #we did the full sampling. remove file if full Furer run
    if args.sample==False and os.path.exists(os.path.join(output_path,'sampleFurer.info')):
        os.remove(os.path.join(output_path,'sampleFurer.info'))

    report.main(args.output_path,args.data_graph_path,args.redo,args.write,monitoring_reports)

   
   

