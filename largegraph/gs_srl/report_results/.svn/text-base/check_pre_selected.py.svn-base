'''
Created on Jul 13, 2015

@author: irma
'''
import argparse,os
import random

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
    print "file saved to: ",os.path.join(results,'interrupted.data')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-results', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-no_interrupt',default=False,action="store_true", help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-batches',default=[],nargs='+', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')

    args = parser.parse_args() 
    results=args.results
    level=results.split("/")[-2].split("_")[-1]
    desired_batches=[]
    for b in args.batches:
        desired_batches.append("batch"+str(b))
    print desired_batches
    pre_selected_patterns=[]
    not_pre_selected_patterns=[]
    problem_selected_patterns=[]
    isomorphic=[]
    nr_patterns_seen=0
    for dir in os.listdir(results):
        if dir.startswith("batch"):
            if len(desired_batches)!=0 and not(dir in desired_batches):
                continue
            print "BATCHES",dir
            for pattern_res in os.listdir(os.path.join(results,dir)):
                nr_patterns_seen+=1
                result_to_batch=os.path.join(results,dir,pattern_res)
                #print result_to_batch
                
                if os.path.exists(os.path.join(result_to_batch,'preselected.info')):
                    pre_selected_patterns.append(result_to_batch)
                if os.path.exists(os.path.join(result_to_batch,'problem_selected.info')):
                    problem_selected_patterns.append(result_to_batch)
                
                if os.path.exists(os.path.join(result_to_batch,'isomorphic_selected.info')):
                    isomorphic.append(result_to_batch)
                            
                if os.path.exists(os.path.join(result_to_batch,'not_preselected.info')):
                    not_pre_selected_patterns.append(result_to_batch)
                    continue
    for p in pre_selected_patterns:
        print p            
    print "Number of preselected patterns: ",len(pre_selected_patterns)
    print "Number of non pre selected patterns ",len(not_pre_selected_patterns)
    print "Number of seen patterns: ",nr_patterns_seen
    print "Nr isomorphic detected: ",len(isomorphic) 
    print "Problem selected patterns: ",len(problem_selected_patterns)
                    
                

               
    

        
        
    



        

        
    
        
        
            
            
            