'''
Created on Jul 23, 2015

@author: irma
'''
import argparse,os



def create_worker_PBS_script(data_graph,path_to_running_script,reporting_algorithm,f): 
    experiment_name="reporting_results_"+reporting_algorithm
    #with open(file,'w') as f:
    f.write("#!/bin/bash -l\n")
    f.write("module load Python/2.7.6-foss-2014a\n")
    f.write("PBS -N "+experiment_name+"\n")
    f.write("cd $PBS_O_WORKDIR\n")
    f.write("python "+ path_to_running_script+reporting_algorithm+" -data "+ data_graph+" -result $pattern_path\n")



def main(data_path,selected_patterns_paths,command_output_path,path_to_scripts):
    path_to_scripts=path_to_scripts.replace("/experiments/",'/report_results/')
    if not os.path.exists(command_output_path):
        os.makedirs(command_output_path)
    header_samplings="pattern_path\n" 
    worker_script_sampling_file=open(os.path.join(command_output_path,"param.data"),'w')
    pbs_furer=open(os.path.join(command_output_path,"report_furer.pbs"),'w')
    pbs_false_furer=open(os.path.join(command_output_path,"report_false_furer.pbs"),'w')
    pbs_random=open(os.path.join(command_output_path,"report_random.pbs"),'w')
    pbs_exhaustive=open(os.path.join(command_output_path,"report_exhaustive.pbs"),'w')
    worker_script_sampling_file.write(header_samplings)
    
    commands_exhaustive=[]
    commands_random_vertex=[]
    commands_furer=[]
    commands_false_furer=[]
    
    for pattern in selected_patterns_paths:
        worker_script_sampling_file.write(pattern+"\n")
        commands_exhaustive.append('python '+path_to_scripts+'/report_exhaustive_approach.py'+' -data '+data_path+' -result '+pattern)
        commands_random_vertex.append('python '+path_to_scripts+'/random_report.py'+' -data '+data_path+' -result '+pattern)
        commands_furer.append('python '+path_to_scripts+'/furer_report.py'+' -data '+data_path+' -result '+pattern)
        commands_false_furer.append('python '+path_to_scripts+'/false_furer_report.py'+' -data '+data_path+' -result '+pattern)
    
    worker_script_sampling_file.close()
    create_worker_PBS_script(data_path,path_to_scripts,"report_exhaustive_approach.py",pbs_exhaustive)
    create_worker_PBS_script(data_path,path_to_scripts,'random_report.py',pbs_random)
    create_worker_PBS_script(data_path,path_to_scripts,'furer_report.py',pbs_furer)
    create_worker_PBS_script(data_path,path_to_scripts,"false_furer_report.py",pbs_false_furer)
    pbs_exhaustive.close()
    pbs_random.close()  
    pbs_furer.close()
    pbs_false_furer.close()
    
    with open(os.path.join(command_output_path,"commands_report_furer.comm"),'w') as f:
        for c in commands_furer:
            f.write(c+"\n")
    
    
    with open(os.path.join(command_output_path,"commands_report_false_furer.comm"),'w') as f:
        for c in commands_false_furer:
            f.write(c+"\n")
            
    with open(os.path.join(command_output_path,"commands_report_exhaustive_approach.comm"),'w') as f:
        for c in commands_exhaustive:
            f.write(c+"\n")
            
    with open(os.path.join(command_output_path,"commands_report_random.comm"),'w') as f:
        for c in commands_random_vertex:
            f.write(c+"\n")
#     
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Run exhaustive approach')
#     parser.add_argument('-data_graph_path', metavar='N',help='path to data graph')
#     parser.add_argument('-pattern_path', metavar='N',help='path to patterns to be processed')
#     parser.add_argument('-pattern_level_path', metavar='N',help='path to patterns to be processed')
#     parser.add_argument('-output_path', metavar='N',help='output path where results will be stored when commands ran')
#     parser.add_argument('-output_script', metavar='N',help='path where the scripts will be saved')
#     parser.add_argument('-path_to_scripts', metavar='N',help='path to execution script (for doing the counts)')
#     parser.add_argument('-level', metavar='N',help='generate commands for Nth level of nodes in pattern lattice')
#     
#     args = parser.parse_args()
#     main(args.data_graph_path,)
    