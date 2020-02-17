'''
Created on Jul 13, 2015

@author: irma
'''
import argparse,os
import random,pickle

def parse_command(command,exp_name):
    split_string=command[0].split(" ")
    command=""
    resulting_string=[]
    script_name=split_string[0]
    data_graph_path=""
    pattern_path=""
    output_path=""
    exhaustive_approach_results_path=""
    runs=""
    time_interval=""
    max_time=""
    commands=split_string[0]
    if exp_name=='furer':
        command=split_string[0]+","
    if exp_name=='ffurer':
        command=split_string[0].replace("furer_sampling_approach.py","false_furer_sampling_approach.py")+","
    if exp_name=='random':
        command=split_string[0].replace("furer_sampling_approach.py","random_vertex_sampling_approach.py")+","
    if exp_name=='exhaustive':
        command=split_string[0].replace("furer_sampling_approach.py","exhaustive_approach.py")+","

        
    for i in xrange(0,len(split_string)):
        if split_string[i]=="-data_graph_path":
            data_graph_path=split_string[i+1]+","
        if split_string[i]=="-pattern_path":
            pattern_path=split_string[i+1]+","
        if split_string[i]=="-output_path":
            output_path=split_string[i+1]+","
        if split_string[i]=="-exhaustive_approach_results_path":
            exhaustive_approach_results_path=split_string[i+1]+","
        if split_string[i]=="-runs":
            runs=split_string[i+1]+","
        if split_string[i]=="-time_interval":
            time_interval=split_string[i+1]+","
        if split_string[i]=="-max_time":
            max_time=split_string[i+1] 
            

    resulting_string=command+data_graph_path+pattern_path+output_path+exhaustive_approach_results_path+runs+time_interval+max_time
    return resulting_string

def make_interrupted_files_param(results,not_finished_commands,algorithm):
    file=open(os.path.join(results,algorithm+'interrupted.data'),'w')
    file.write("script,data_graph_path,pattern_path,output_path,exhaustive_approach_results_path,runs,time_interval,max_time\n")
    for (exp_name,command_path) in not_finished_commands:
        command=open(command_path,'r').readlines()
        file.write(parse_command(command,exp_name)+"\n")
    file.close()
    print "file saved to: ",os.path.join(results,algorithm+'interrupted.data')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-results', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-no_interrupt',default=False,action="store_true", help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')

    args = parser.parse_args() 
    results=args.results
    level=results.split("/")[-2].split("_")[-1]
    
    nr_patterns=0
    nr_selected_so_far=0
    nr_not_selected_so_far=0
    not_completed=0
    completed_furer=0
    completed_false_furer=0
    completed_rnd=0
    completed_exhaustive=0
    
    incompleted_furer=0
    incompleted_false_furer=0
    incompleted_rnd=0
    incompleted_exhaustive=0
    
    incomplete_furer=[]
    incomplete_false_furer=[]
    incomplete_rnd=[]
    incomplete_exhaustive=[]
    incomplete_fur_random_ord=[]
    
    monitoring_not_complete=[]
    
    monitored_furer=[]
    monitored_ff=[]
    monitored_random=[]
    monitored_exh=[]
    monitored_exh_not_finished=[]
    
    
    not_finished=[]
    not_finished_commands=[]
    one_not_selected=None
    selected_furer=[]
    not_finished=0
    not_finished_patterns=[]
    not_finished_patterns_exhaustive=[]
    pattern=0
    batches_selected=[]
    problem_selected=[]
    not_selected=[]
    conditionally_selected=[]
    failed_exhaustive=[]
    undetermined_count=0
    undetermined=[]
    for dir in os.listdir(results):
        if dir.startswith("batch"):
            #print "BATCHES"
            for pattern_res in os.listdir(os.path.join(results,dir)):
                pattern+=1   
                print "PATTERN: ",pattern
                result_to_batch=os.path.join(results,dir,pattern_res)
                selected=None
                print "Exists? ",os.path.join(result_to_batch,'selected.info'),os.path.exists(os.path.join(result_to_batch,'selected.info'))
                print "Exists? ",os.path.join(result_to_batch,'not_selected.info'),os.path.exists(os.path.join(result_to_batch,'not_selected.info'))
                print "Exists? ",os.path.join(result_to_batch,'conditionally_selected.info'),os.path.exists(os.path.join(result_to_batch,'conditionally_selected.info'))
                print "Exists? ",os.path.join(result_to_batch,'problem_selected.info'),os.path.exists(os.path.join(result_to_batch,'problem_selected.info'))
                            
                if os.path.exists(os.path.join(result_to_batch,'not_selected.info')):
                    nr_not_selected_so_far+=1
                    not_selected.append(result_to_batch)
                    selected=False
                    continue
                    
                if os.path.exists(os.path.join(result_to_batch,'conditionally_selected.info')):
                    conditionally_selected.append(result_to_batch)
                    selected=False
                    continue
                    
                if os.path.exists(os.path.join(result_to_batch,'problem_selected.info')):
                    problem_selected.append(result_to_batch)
                    selected=False
                    #continue
                
                if os.path.exists(os.path.join(result_to_batch,'selected.info')):
                    nr_selected_so_far+=1
                    selected_furer.append(result_to_batch)
                    batches_selected.append(result_to_batch)
                    selected=True            

                if selected:
                    print "SELECTED!"
                    if os.path.exists(os.path.join(result_to_batch,'results_furer','complete.info')):
                        if os.path.exists(os.path.join(result_to_batch,'results_furer','monitoring')) and len(os.listdir(os.path.join(result_to_batch,'results_furer','monitoring')))!=0:
                            monitored_furer.append(os.path.join(result_to_batch,'results_furer'))  
                        else:
                            monitoring_not_complete.append(('furer',os.path.join(result_to_batch,'results_furer','command.comm'))) 
                        if os.path.exists(os.path.join(result_to_batch,'results_furer','monitoring_reports.pickle')):
                              pkl_file = open(os.path.join(result_to_batch,'results_furer','monitoring_reports.pickle'), 'rb')
                              monitoring_reports=pickle.load(pkl_file)  
                              if len(monitoring_reports)==1 and 0 in monitoring_reports.keys():
                                  monitoring_reports=monitoring_reports[0]
                              if len(monitoring_reports)<120:
                                  monitoring_not_complete.append(('furer',os.path.join(result_to_batch,'results_furer','command.comm')))
                        completed_furer+=1
                    else:
                        incompleted_furer+=1
                        incomplete_furer.append(('furer',os.path.join(result_to_batch,'results_furer','command.comm')))
                        not_finished_patterns.append(('furer',os.path.join(result_to_batch,'results_furer','command.comm')))
                              
                    if os.path.exists(os.path.join(result_to_batch,'results_false_furer','complete.info')):
                        if os.path.exists(os.path.join(result_to_batch,'results_false_furer','monitoring')) and len(os.listdir(os.path.join(result_to_batch,'results_false_furer','monitoring')))!=0:
                            monitored_ff.append(os.path.join(result_to_batch,'results_false_furer'))
                        if os.path.exists(os.path.join(result_to_batch,'results_false_furer','monitoring_reports.pickle')):
                              pkl_file = open(os.path.join(result_to_batch,'results_false_furer','monitoring_reports.pickle'), 'rb')
                              monitoring_reports=pickle.load(pkl_file)  
                              if 0 in monitoring_reports.keys() and len(monitoring_reports)==1:
                                  monitoring_reports=monitoring_reports[0]
                              if len(monitoring_reports)<120:
                                  monitoring_not_complete.append(('ffurer',os.path.join(result_to_batch,'results_false_furer','command.comm')))
                        completed_false_furer+=1
                    else:
                        incompleted_false_furer+=1
                        incomplete_false_furer.append(('ffurer',os.path.join(result_to_batch,'results_false_furer','command.comm')))
                        not_finished_patterns.append(('ffurer',os.path.join(result_to_batch,'results_furer','command.comm')))
                        
                    if os.path.exists(os.path.join(result_to_batch,'random_vertex_approach','complete.info')):
                        if os.path.exists(os.path.join(result_to_batch,'random_vertex_approach','monitoring')) and len(os.listdir(os.path.join(result_to_batch,'random_vertex_approach','monitoring')))!=0:
                            monitored_random.append(os.path.join(result_to_batch,'random_vertex_approach'))
                        if os.path.exists(os.path.join(result_to_batch,'random_vertex_approach','monitoring_reports.pickle')):
                              pkl_file = open(os.path.join(result_to_batch,'random_vertex_approach','monitoring_reports.pickle'), 'rb')
                              monitoring_reports=pickle.load(pkl_file)  
                              if 0 in monitoring_reports.keys() and len(monitoring_reports)==1:
                                  monitoring_reports=monitoring_reports[0]
                              if len(monitoring_reports)<120:
                                  monitoring_not_complete.append(('random',os.path.join(result_to_batch,'random_vertex_approach','command.comm')))
                        completed_rnd+=1
                    else:
                        incompleted_rnd+=1
                        incomplete_rnd.append(('random',os.path.join(result_to_batch,'random_vertex_approach','command.comm')))
                        not_finished_patterns.append(('random',os.path.join(result_to_batch,'random_vertex_approach','command.comm')))
                    
                    print "exists? ",os.path.join(result_to_batch,'results_false_furer_order_random'),os.path.exists(os.path.join(result_to_batch,'results_false_furer_order_random'))
                    #print "nr reportS: ",len(os.listdir(os.path.join(result_to_batch,'results_false_furer_order_random','monitoring')))
                    if os.path.exists(os.path.join(result_to_batch,'results_false_furer_order_random')):
                        if os.path.exists((os.path.join(result_to_batch,'results_false_furer_order_random','monitoring'))) and len(os.listdir(os.path.join(result_to_batch,'results_false_furer_order_random','monitoring')))<120:
                            incomplete_fur_random_ord.append(('rnd_fur',os.path.join(result_to_batch,'results_false_furer_order_random','command.comm')))
                        
                    print "Exists exhaustive?",os.path.exists(os.path.join(result_to_batch,'exhaustive_approach','results_'+pattern_res+'.res'))
                    if os.path.exists(os.path.join(result_to_batch,'exhaustive_approach','results_'+pattern_res+'.res')):
                        #if os.path.exists(os.path.join(result_to_batch,'exhaustive_approach','monitoring')) and len(os.listdir(os.path.join(result_to_batch,'exhaustive_approach','monitoring')))!=0:
                        #    monitored_exh.append(os.path.join(result_to_batch,'exhaustive_approach'))
                        if os.path.exists(os.path.join(result_to_batch,'exhaustive_approach','monitored.info')):
                            monitored_exh.append(os.path.join(result_to_batch,'exhaustive_approach'))
                        else:
                            monitored_exh_not_finished.append(os.path.join(result_to_batch,'exhaustive_approach'))
                        completed_exhaustive+=1
                    else:
                        incompleted_exhaustive+=1
                        incomplete_exhaustive.append(('exhaustive',os.path.join(result_to_batch,'exhaustive_approach','command.comm')))
                        not_finished_patterns.append(('exhaustive',os.path.join(result_to_batch,'exhaustive_approach','command.comm')))
                    if os.path.exists(os.path.join(result_to_batch,'exhaustive_approach','no_results.info')):
                        failed_exhaustive.append(os.path.join(result_to_batch))
                    continue
                else:
                    undetermined.append(result_to_batch)
                    undetermined_count+=1
                    
                    
    print "NR PATTERNS OVER ALL BATCHES: ",pattern
    print "Nr selected results over all batches: ",len(batches_selected)
    print "Nr NOT selected results in these batches: ",nr_not_selected_so_far
    
    with open(os.path.join(results,'selected_patterns_list.info'),'w') as f:
        for p in batches_selected:
            f.write(p+"\n")
        
    
    print "Results furer complete:",completed_furer
    print "Results false furer complete:",completed_false_furer
    print "Results rnd complete:",completed_rnd
    print "Results exhaustive complete:",completed_exhaustive
    print "----------------------------------------------"
    print "Results furer incomplete:",incompleted_furer
    #for f in incomplete_furer:
    #    print f
    #print "________________________________________________" 
    #print "Results false furer incomplete:",incompleted_false_furer
    #for f in incomplete_false_furer:
    #    print f
    #print "________________________________________________" 
    #print "Results rnd incomplete:",incompleted_rnd
    #for f in incomplete_rnd:
    #    print f
    #print "________________________________________________" 
    print "Results exhaustive incomplete:",incompleted_exhaustive
    for f in incomplete_exhaustive:
        print f
    print "________________________________________________" 
    
    print "Undetermined: ",undetermined_count
    #for und in undetermined:
    #    print und
    print "Problem selected ..."
    print " -------------------- Failed exhaustive: WARNING --------------------------- \n"
    for e in problem_selected:
         print e
    print "-------------------------------------------------------------------------------"
    print "Monitored ..."
    print "Monitored furer: ",len(monitored_furer)
    print "Monitored false furer: ",len(monitored_ff)
    print "Monitored random: ",len(monitored_random)
    print "Monitored exhaustive: ",len(monitored_exh)
    print "Exhaustive non-monitored: "
    for m in monitored_exh_not_finished:
        print m

    print "Furer non-monitored: "
    for m in monitoring_not_complete:
        print m
    
    if len(batches_selected)>100:
        print "More than needed patterns selected!"
        random.shuffle(batches_selected)
        cut=len(batches_selected)-100
        print "Need to cut: ",cut,"patterns!"
        cutting=batches_selected[0:cut]
        for c in cutting:
            os.rename(os.path.join(c,'selected.info'),os.path.join(c,'extra_selected.info'))
    print "--------- CONDITIONALLY SELECTED -------------------"
    for c in conditionally_selected:
        print c
    print "----------------------------------------------------"
    print "INTERRUPTED: ",len(not_finished_patterns)
    if(args.no_interrupt==False):
        print "Interrupted exhaustive:  ",len(incomplete_exhaustive)
        print "Interrupted furer:  ",len(incomplete_furer)
        print "Interrupted false_furer:  ",len(incomplete_false_furer)
        print "Interrupted random:  ",len(incomplete_rnd)
        make_interrupted_files_param(os.path.join(args.results),incomplete_exhaustive,"exhaustive")
        make_interrupted_files_param(os.path.join(args.results),incomplete_furer,"furer")
        make_interrupted_files_param(os.path.join(args.results),incomplete_false_furer,"false_furer")
        make_interrupted_files_param(os.path.join(args.results),incomplete_rnd,"random")
        make_interrupted_files_param(os.path.join(args.results),incomplete_fur_random_ord,"fur_random_ord")
    print "Number of incomplete monitorings: ",len(monitoring_not_complete)
    make_interrupted_files_param(os.path.join(args.results),monitoring_not_complete,"all")
       

    
        
        
    



        

        
    
        
        
            
            
            