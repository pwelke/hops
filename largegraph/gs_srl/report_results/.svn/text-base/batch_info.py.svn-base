'''
Created on May 4, 2015

Given a directory with results, this script goes through all the results and checks specific 
statistics. For example, how many patterns have a results and how many patterns fit into a specific threshold
- mark them

@author: irma
'''
import argparse
import os
import subprocess
import create_csv_batch_file
import filter_batch_results
from experiments import create_new_batch
from experiments import generate_commands


def extract_level_of_patterns(path):
    strings=path.split("/")
    for s in strings:
        if s.startswith("patterns_size"):
            return s.split("_")[-1]

def main(results,redo,patterns,nlimits):    
    #should be a parent root of all batch results
    missing_results_patterns_exhaustive=[]
    missing_results_patterns_random=[]
    missing_results_patterns_furer=[]
    missing_results_patterns_ffurer=[]
    folder_name_exhaustive_approach='exhaustive_approach'
    folder_name_random_vertex='random_vertex_approach'
    folder_name_furer='results_furer'
    folder_name_false_furer='results_false_furer'
    numer_of_results_exhaustive=0
    exhaustive_pattern_names_without_results=[]
    invalid_patterns=[]
    exhaustive_pattern_no_possible_OBD=[]
    exhaustive_pattern_names_with_results=[]
    exhaustive_patterns_missing_results=[]
    number_of_no_results_exhaustive=0
    numer_of_results_random=0
    number_of_no_results_random_due_to_exhaustive=0
    random_patterns_missing_results=[]
    invalid_random_directories=[]
    numer_of_results_furer=0
    number_of_no_results_furer_due_to_exhaustive=0
    furer_patterns_missing_results=[]
    numer_of_results_false_furer=0
    number_of_no_results_false_furer_due_to_exhaustive=0
    false_furer_patterns_missing_results=[]
    
    result_file_name_exhaustive="info.txt"
    results_file_name_sampling_lack_of_results="no_exhaustive_approach_results.info"
    
    commands_missing_files=[]
    
    #make info folder for these experiments
    folder_info_name=results.split("/")[-2]
    batch=results.split("/")[-1]
    the_rest_of_path='/'.join(results.split("/")[:-2])
    the_rest_of_path1='/'.join(results.split("/")[:-1])
    path_to_info=os.path.join(the_rest_of_path1,"info",batch)
    print "PATH TO INFO: ",path_to_info
    csv_files=os.path.join(the_rest_of_path)
    output_selected_files=os.path.join(the_rest_of_path)
    if not os.path.exists(path_to_info):
        os.makedirs(path_to_info)
    
    print "Number of files in the directory: ",len(os.listdir(results))
    print " ---------------------- EXHAUSTIVE APPROACH ----------------------"    
    #for d in os.listdir(results):
       #print os.listdir(os.path.join(results,d))
       #print os.listdir(os.path.join(results,d,folder_name_false_furer))
    #EXHAUSTIVE APPROACH
    result_exhaustive_paths=[]
    for dir in os.listdir(results):
        directory=os.path.join(results,dir,folder_name_exhaustive_approach)
        directory_pattern=os.path.join(patterns,dir)
        if os.path.exists(os.path.join(directory_pattern,"invalid.info")):
            invalid_patterns.append(directory)
        if not os.path.exists(directory) or len(os.listdir(directory))==1:
            print "Missing result:",directory
            exhaustive_patterns_missing_results.append(directory) 
            missing_results_patterns_exhaustive.append(dir)
            continue    
        counter=0
        for file in os.listdir(directory):
            if file=="no_results.info":
                number_of_no_results_exhaustive+=1
                exhaustive_pattern_names_without_results.append(directory)
                counter+=1
            elif file.startswith("results_"):
                result_exhaustive_paths.append(directory)
                exhaustive_pattern_names_with_results.append(directory)
                numer_of_results_exhaustive+=1
                counter+=1
            elif file.startswith("no_obd"):
                exhaustive_pattern_no_possible_OBD.append(directory)
                counter+=1
    exhaustive_gen_info=open(os.path.join(path_to_info,"exhaustive_gen_info.info"),'w')                    
    #Write missing / non completed results of exhaustive approach                
    exhaustive_non_completed_results_file=open(os.path.join(path_to_info,"exhaustive_non_completed.info"),'w')
    exhaustive_completed_results=open(os.path.join(path_to_info,"exhaustive_completed.info"),'w')
    for f in exhaustive_pattern_names_with_results:
        exhaustive_completed_results.write(f+"\n")
    for f in exhaustive_patterns_missing_results:
        exhaustive_non_completed_results_file.write(f+"\n")
    exhaustive_non_completed_results_file.close()
    exhaustive_completed_results.close()
    
    print "Number of results for exhaustive approach: ",numer_of_results_exhaustive
    print "Number of results with zero embeddings",str(len( exhaustive_pattern_names_without_results))
    print "Missing exhaustive result (timeout!): ",len(exhaustive_patterns_missing_results)
    print "Number of impossible OBDs: ",len(exhaustive_pattern_no_possible_OBD)
    print "Number of invalid patterns: ",len(invalid_patterns)
    exhaustive_gen_info.write("Number of results for exhaustive approach: "+str(numer_of_results_exhaustive))
    exhaustive_gen_info.write(" Number of results with zero embeddings "+str(len(exhaustive_pattern_names_without_results)))
    exhaustive_gen_info.write(" Missing exhaustive result (folder and stuff): "+str(len(exhaustive_patterns_missing_results)))
    exhaustive_gen_info.write("Number of impossible OBDs: "+str(len(exhaustive_pattern_no_possible_OBD)))
    exhaustive_gen_info.close()
    
    #RANDOM APPROACH
    print "----------------------- RANDOM -----------------------------"   
    random_gen_info=open(os.path.join(path_to_info,"random_gen_info.info"),'w') 
    random_non_completed_results_file=open(os.path.join(path_to_info,"random_non_completed.info"),'w')
    random_some_other_problem=open(os.path.join(path_to_info,"random_some_other_problem.info"),'w')
    no_limit_results_random=[]
    not_selected_within_one_hour=[]
    running_at_the_moment=[]
    for pattern in os.listdir(results):
        print "PATTERN NAME: ",pattern
        directory=os.path.join(results,pattern,folder_name_random_vertex)
        if not os.path.exists(directory):
            random_patterns_missing_results.append(directory)
            missing_results_patterns_random.append(dir)
            continue
        if exists_file(directory,["no_exhaustive_approach_results.info","no_results.info"]):
            number_of_no_results_random_due_to_exhaustive+=1
            print "due to exhaustive"
            continue
        if exists_file(directory,["completed.info"]):
            numer_of_results_random+=1
            print "completed"
            continue
        if exists_file(directory,["running.info"]):
            running_at_the_moment.append(directory)
            print "running"
            continue
        if exists_file(directory,["not_selected.info"]):
            not_selected_within_one_hour.append(directory)
            print "not selected"
            continue
        if exists_file(directory,["invalid.info"]):
            invalid_random_directories.append(directory)
            print "invalid"
            continue
        if len(os.listdir(os.path.join(directory,"n_limits")))<nlimits:
            no_limit_results_random.append(dir)
            print "no nlimits"
            continue
        else:
            random_patterns_missing_results.append(directory)
            missing_results_patterns_random.append(dir)
    print "Running at the moment: ",len(running_at_the_moment)
    print "Number of results for random approach: ",numer_of_results_random
    print "Number of overall missing results: ",number_of_no_results_random_due_to_exhaustive+len(not_selected_within_one_hour)+len(invalid_random_directories)+len(random_patterns_missing_results)+len(no_limit_results_random)
    print "Number of missing results (due to exhaustive): ",number_of_no_results_random_due_to_exhaustive
    print "Number of not selected patterns:(within one hour) ",len(not_selected_within_one_hour) 
    print "Number of missing results (invalid)",len(invalid_random_directories) 
    print "Number of results never executed:",len(random_patterns_missing_results)
    print "Number of no n_limit results :",len(no_limit_results_random)
    for f in not_selected_within_one_hour:
        print f    
    random_gen_info.write("Number of results for random approach: "+str(numer_of_results_random)+ " Number of missing results:(due to exhaustive): "+str(number_of_no_results_random_due_to_exhaustive)+"Number of missing results:(never executed): "+str(len(random_patterns_missing_results))+"\n")
    for f in random_patterns_missing_results:
        random_non_completed_results_file.write(f+"\n")
    random_non_completed_results_file.close()
    random_gen_info.close()
    
    invalid_furer_directories=[]
    #FURER
    print "-----------------------  FURER -------------------------------------"   
    furer_gen_info=open(os.path.join(path_to_info,"furer_gen_info.info"),'w') 
    furer_non_completed_results_file=open(os.path.join(path_to_info,"furer_non_completed.info"),'w')
    incomplet_results_furer=[]
    no_limit_results=[]
    for pattern in os.listdir(results):
        directory=os.path.join(results,pattern,folder_name_furer)
        if not os.path.exists(directory):
            furer_patterns_missing_results.append(directory)
            missing_results_patterns_furer.append(dir)
            continue
        if exists_file(directory,["no_exhaustive_approach_results.info","no_results.info"]):
             number_of_no_results_furer_due_to_exhaustive+=1
             continue
        if exists_file(directory,["invalid.info"]):
             invalid_furer_directories.append(directory)
             continue
        if exists_file(directory,["fudicts.pickle"]):
            numer_of_results_furer+=1
            continue
        if len(os.listdir(os.path.join(directory,"n_limits")))<nlimits:
            no_limit_results.append(dir)
            continue
        else:
            furer_patterns_missing_results.append(directory)
            missing_results_patterns_furer.append(dir)
    print "Number of results for furer approach: ",numer_of_results_furer
    print " Number of missing results: (due to exhaustivE) ",number_of_no_results_furer_due_to_exhaustive
    print " Number of incomplete results: (never executed) ",len(furer_patterns_missing_results)      
    print "Number of invalid patterns: ",len(invalid_furer_directories)
    print "Number of no n_limit results: ",len(no_limit_results)
    furer_gen_info.write("Number of results for furer approach: "+str(numer_of_results_furer)+ " Number of missing results: "+str(len(furer_patterns_missing_results))+" Number of incomplete results: (never executed) "+str(len(furer_patterns_missing_results))+"\n")
    for f in furer_patterns_missing_results:
        furer_non_completed_results_file.write(f+"\n")
    furer_non_completed_results_file.close()
    furer_gen_info.close()
    
    #FALSE FURER
    print "--------------------------  FALSE FURER ---------------------------------------" 
    false_furer_gen_info=open(os.path.join(path_to_info,"false_furer_gen_info.info"),'w') 
    false_furer_non_completed_results_file=open(os.path.join(path_to_info,"false_furer_non_completed.info"),'w')
    invalid_false_furer_directories=[]
    incomplet_results_ffurer=[]
    no_limit_results_ffurer=[]
    for pattern in os.listdir(results):
        directory=os.path.join(results,pattern,folder_name_false_furer)
        if not os.path.exists(directory):
            false_furer_patterns_missing_results.append(directory)
            missing_results_patterns_ffurer.append(dir)
            continue
        if exists_file(directory,["no_exhaustive_approach_results.info","no_results.info"]):
             number_of_no_results_false_furer_due_to_exhaustive+=1
             continue
        if exists_file(directory,["invalid.info"]):
             invalid_false_furer_directories.append(directory)
             continue
        if exists_file(directory,["fudicts.pickle"]):
            numer_of_results_false_furer+=1
            continue
        if len(os.listdir(os.path.join(directory,"n_limits")))<nlimits:
            no_limit_results_ffurer.append(dir)
            continue
        else:
            false_furer_patterns_missing_results.append(directory)
            missing_results_patterns_ffurer.append(dir)
    print "Number of results for false furer approach: ",numer_of_results_false_furer
    print" Number of missing results (due to exhaustive): ",number_of_no_results_false_furer_due_to_exhaustive
    print "Number of incomplete results: ",len(false_furer_patterns_missing_results)               
    print "Number of no n_limit results: ",len(no_limit_results_ffurer)
    false_furer_gen_info.write("Number of results for false furer approach: "+str(numer_of_results_false_furer)+ " Number of missing results: "+str(number_of_no_results_false_furer_due_to_exhaustive)+"Number of incomplete results: "+str(len(false_furer_patterns_missing_results))+ "\n")
    for f in false_furer_patterns_missing_results:
        false_furer_non_completed_results_file.write(f+"\n")
    false_furer_non_completed_results_file.close()
    false_furer_gen_info.close()
    
    commands_scripts=results.replace("RESULTS","COMMANDS")
    commands=path_to_info
    
    #write a special file with missing files
    print "Writing missing files to:",os.path.join(commands,"missing_files") 
    file_missing_exhaustive=os.path.join(commands,"missing_files_exhaustive")
    file_missing_sampling=os.path.join(commands,"missing_files_sampling")


#WRITE EXHAUSTIVE
    with(open(file_missing_exhaustive,'a')) as f:
        f.write("command\n")
        for pattern in missing_results_patterns_exhaustive:
           #READ exhaustive template file
           template_file=open(os.path.join(commands_scripts,"template_exhaustive"),'r')
           command=get_template_command(template_file,pattern) 
           f.write(command+"\n")
    with(open(file_missing_sampling,'a')) as f:
        for pattern in missing_results_patterns_random:
            #READ random template file
               template_file=open(os.path.join(commands_scripts,"template_random"),'r')
               command=get_template_command(template_file,pattern) 
               f.write(command+"\n")
    with(open(file_missing_sampling,'a')) as f:
        for pattern in missing_results_patterns_furer:
            #READ random template file
           template_file=open(os.path.join(commands_scripts,"template_furer"),'r')
           command=get_template_command(template_file,pattern) 
           f.write(command+"\n")
    with(open(file_missing_sampling,'a')) as f: 
        for pattern in missing_results_patterns_ffurer:
            #READ random template file
           template_file=open(os.path.join(commands_scripts,"template_ffurer"),'r')
           command=get_template_command(template_file,pattern) 
           f.write(command+"\n")
           
     #make worker script for missing files
    make_default_worker_script(file_missing_exhaustive,commands)
    print "module load worker/1.5.0-intel-2014a"
    print "wsub -batch "+os.path.join(commands,"missing"+"_ws.pbs")+" -data "+os.path.join(commands,"missing_files_exhaustive")+" -A lp_tractable"
    print "wsub -batch "+os.path.join(commands,"missing"+"_ws.pbs")+" -data "+os.path.join(commands,"missing_files_sampling")+" -A lp_tractable"
    
def exists_file(directory,file_list):
    for f in os.listdir(directory):
        for file in file_list:
            if f==file:
                return True
    return False        
    
    
def get_nr_commands_in_worker_script(path):
    counter=-1
    with open(path,"r") as f:
        for line in f.readlines():
           counter+=1
    return counter    
    
def make_default_worker_script(path_to_commands_missing_files,commands_path):
    #recalculate time needed to run all the commands in the running script
    nr_commands=get_nr_commands_in_worker_script(path_to_commands_missing_files)

    file=os.path.join(commands_path,"missing"+"_ws.pbs")
    with open(file,'w') as f:
        f.write("#!/bin/bash -l\n")
        f.write("module load Python/2.7.6-foss-2014a\n")
        f.write("NPROC=`grep MHz /proc/cpuinfo |wc -l`\n")
        f.write("#PBS -N "+"missing"+"\n")
        f.write("#PBS -l nodes=1"+":ppn=$NPROC:nehalem"+"\n")
        f.write("#PBS -l wall_time=100:00:00"+"\n")
        f.write("#PBS -q default\n")
        f.write("cd $PBS_O_WORKDIR\n")
        path_to_scratch_logging="$VSC_SCRATCH_NODE/vsc31168/MARTIN_EXPERIMENTS/"
        f.write("mkdir -p "+path_to_scratch_logging+"/mising"+"\n")
        f.write("LOGSTDOUT="+path_to_scratch_logging+"/missing"+".stdout.log\n")
        f.write("LOGSTDERR="+path_to_scratch_logging+"/missing"+".stdout.log\n") 
        f.write("$command")

def get_template_command(template_file,pattern):
    #read one line from template file
    new_line=template_file.read().replace("$PATTERN",pattern)+" -redo"
    return new_line
        
     
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-results', metavar='N',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-redo',default=False,action='store_true',help='in case results already processed for this batch redo is false by default unless specified true')
    parser.add_argument('-patterns', metavar='N',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-N_LIMITS',default=16,type=int,help='number of nlimits')

    args = parser.parse_args() 
    main(args.results,args.redo,args.patterns,args.N_LIMITS)
    
    

  

    
    
