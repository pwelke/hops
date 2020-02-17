"/vsc31168/"'''
from experiments.generate_commands_split_runs import wall_time_string
Created on Apr 30, 2015

@author: irma
'''
import os 
import argparse
from datetime import datetime
global wall_time_string
from report_results import *
import generate_commands_for_selected


def create_job_array_script(pbs_script_folder,commands_file,nr_nodes,nr_processes_per_node,node_type,experiment_name): 
    global wall_time_string   
      
    with open(os.path.join(pbs_script_folder,experiment_name+".pbs"),'w') as f:
        f.write("#!/bin/bash -l\n")
        f.write("module load Python/2.7.6-foss-2014a\n")
        f.write("#PBS -N "+experiment_name+"\n")
        f.write("#PBS -l nodes="+str(nr_nodes)+":ppn="+str(nr_processes_per_node)+":"+str(node_type)+"\n")
        f.write("#PBS -l walltime="+wall_time_string+"\n")
        f.write("#PBS -q default\n")
        f.write("cd $PBS_O_WORKDIR\n")
        path_to_scratch_logging="$VSC_SCRATCH_NODE/vsc31168/MARTIN_EXPERIMENTS/"
        f.write("mkdir -p "+path_to_scratch_logging+"/"+experiment_name+"\n")
        f.write("LOGSTDOUT="+path_to_scratch_logging+"/"+experiment_name+".stdout.log\n")
        f.write("LOGSTDERR="+path_to_scratch_logging+"/"+experiment_name+".stdout.log\n")  
        f.write("cmd=`head -${PBS_ARRAYID} "+commands_file+" | tail -1`\n")
        f.write("eval $cmd\n")
        f.write("rm pbs_*\n")

def get_nr_commands_in_worker_script(path):
    counter=-1
    with open(path,"r") as f:
        for line in f.readlines():
           counter+=1
    return counter

def create_worker_PBS_script_exhaustive(pbs_script_folder,worker_script_exhaustive_file,path_to_running_script,pattern_path,experiment_name): 
    #global wall_time_string   
    #date_object = datetime.strptime(wall_time_string, '%H:%M:%S')
    #time=date_object.time()
    nr_commands=get_nr_commands_in_worker_script(worker_script_exhaustive_file)
    #seconds_of_desired_time_sequentially=(time.hour*3600+time.minute*60+time.second)*nr_commands
    #recalculate time needed to run all the commands in the running script
    file=pbs_script_folder+"/"+experiment_name+"_ws.pbs"
    with open(file,'w') as f:
        f.write("#!/bin/bash -l\n")
        f.write("module load Python/2.7.6-foss-2014a\n")
        f.write("NPROC=`grep MHz /proc/cpuinfo |wc -l`\n")
        #f.write("required_seconds=$(("+str(seconds_of_desired_time_sequentially)+"/$NPROC))\n")
        f.write("wall_time=`date -u -d @$required_seconds +%T`\n")
        f.write("#PBS -N "+experiment_name+"\n")
        #f.write("#PBS -l nodes="+str(nr_nodes)+":ppn=$NPROC:"+str(node_type)+"\n")
        #f.write("#PBS -l walltime=$wall_time\n")
        #f.write("#PBS -l walltime="+wall_time_string+"\n")
        f.write("#PBS -q default\n")
        f.write("cd $PBS_O_WORKDIR\n")
        f.write("touch "+"$VSC_DATA/output/"+experiment_name+".txt \n") 
        f.write("touch "+"$VSC_DATA/output/"+experiment_name+"_error.txt \n") 
        path_to_scratch_logging="$VSC_SCRATCH_NODE/vsc31168/MARTIN_EXPERIMENTS/"
        f.write("mkdir -p "+path_to_scratch_logging+"/"+experiment_name+"\n")
        f.write("LOGSTDOUT="+path_to_scratch_logging+"/"+experiment_name+".stdout.log\n")
        f.write("LOGSTDERR="+path_to_scratch_logging+"/"+experiment_name+".stdout.log\n") 
        f.write("python "+ path_to_running_script+"exhaustive_approach.py -data_graph_path $data_graph_path -pattern_path $pattern_path -output_path $output_path > $VSC_DATA/output/"+experiment_name+".txt \ 2> $VSC_DATA/output/"+experiment_name+"/_error.txt\n")
    return file

def create_worker_PBS_script_sampling(pbs_script_folder,worker_script_exhaustive_file,path_to_running_script,pattern_path,experiment_name,approach_name_script,selected,pattern_level_path,iu): 
    #global wall_time_string   
    #date_object = datetime.strptime(wall_time_string, '%H:%M:%S')
    #time=date_object.time()
    nr_commands=get_nr_commands_in_worker_script(worker_script_exhaustive_file)
    #seconds_of_desired_time_sequentially=(time.hour*3600+time.minute*60+time.second)*nr_commands
    #recalculate time needed to run all the commands in the running script
    file=pbs_script_folder+"/"+experiment_name+"_ws.pbs"
    selected_command=""
    if selected==True:
        selected_command=" -selected "
    with open(file,'w') as f:
        f.write("#!/bin/bash -l\n")
        f.write("module load Python/2.7.6-foss-2014a\n")
        f.write("#PBS -N "+experiment_name+"\n")
        f.write("cd $PBS_O_WORKDIR\n")
        path_to_scratch_logging="$VSC_SCRATCH_NODE/vsc31168/MARTIN_EXPERIMENTS/"
        f.write("mkdir -p "+path_to_scratch_logging+"/"+experiment_name+"\n")
        f.write("LOGSTDOUT="+path_to_scratch_logging+"/"+experiment_name+".stdout.log\n")
        f.write("LOGSTDERR="+path_to_scratch_logging+"/"+experiment_name+".stdout.log\n")
        f.write("touch "+"$VSC_DATA/output/"+experiment_name+".txt \n") 
        f.write("touch "+"$VSC_DATA/output/"+experiment_name+"_error.txt \n") 
        f.write("#PBS -e $VSC_DATA/output/"+experiment_name+".txt \n")
        f.write("#PBS -o $VSC_DATA/output/"+experiment_name+"._error.txt \n")
        if pattern_level_path==None:
            f.write("python "+ path_to_running_script+approach_name_script+" -data_graph_path $data_graph_path -pattern_path $pattern_path -output_path $output_path -exhaustive_approach_results_path $exhaustive_approach_results_path -runs $runs -time_interval $time_interval -max_time $max_time"+selected_command+" -sample\n")
        else:
            print "IU: ",iu
            f.write("python "+ path_to_running_script+approach_name_script+" -data_graph_path $data_graph_path -pattern_path $pattern_path -output_path $output_path -exhaustive_approach_results_path $exhaustive_approach_results_path -runs $runs -time_interval $time_interval -max_time $max_time"+selected_command+" -pattern_level_results "+pattern_level_path+" -sample"+" -iu \n")


def create_PBS_script(pbs_script_folder,command_file_to_xargs,counter,experiment_name): 
    #global wall_time_string     
    file=pbs_script_folder+"/pbs_block_"+str(counter)+"_"+experiment_name.replace(" ","_")+".pbs"
    with open(file,'w') as f:
        f.write("#!/bin/bash -l\n")
        f.write("module load Python/2.7.6-foss-2014a\n")
        f.write("#PBS -N "+experiment_name+"\n")
        #f.write("#PBS -l nodes="+str(nr_nodes)+":ppn="+str(nr_processes_per_node)+":"+str(node_type)+"\n")
        #f.write("#PBS -l walltime="+wall_time_string+"\n")
        f.write("#PBS -q default\n")
        f.write("TMPDIR=/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/workdir/\n")
        f.write("mkdir -p TMPDIR\n")
        f.write("cd $TMPDIR\n") 
        path_to_scratch_logging="$VSC_SCRATCH_NODE/vsc31168/MARTIN_EXPERIMENTS/"
        split_command=command_file_to_xargs.split('/')
        path_log= split_command[-5:-2]  
        for p in path_log:
            path_to_scratch_logging+="/"+p
        f.write("mkdir -p "+path_to_scratch_logging+"/"+experiment_name+"\n")    
        f.write("LOGSTDOUT="+path_to_scratch_logging+"/"+experiment_name+".stdout.log\n")
        f.write("LOGSTDERR="+path_to_scratch_logging+"/"+experiment_name+".stdout.log\n")  
        f.write("xargs -a " +command_file_to_xargs+" -P 10 -I COMMAND sh -c ""COMMAND"" 1> $LOGSTDOUT 2> $LOGSTDERR\n")
        f.write("rm pbs_*\n")

    

def split_commands(Max,commands,path,pattern_size,experiment_name):
    split=[commands[i:i+Max] for i in range(0,len(commands),Max)]
    pbs_script_folder=os.path.join(path,"PBS_scripts")
    if(not(os.path.exists(pbs_script_folder))):
        os.makedirs(pbs_script_folder)
    
    counter=1
    print "Number of blocks",len(split)
    for block in split:
       with open(path+"/commands_pattern_"+str(pattern_size)+"_"+str(counter)+".c_block",'w') as file:
           create_PBS_script(pbs_script_folder,path+"/commands_pattern_"+str(pattern_size)+"_"+str(counter)+".c_block",counter,experiment_name)
           counter+=1
           for elem in block:
               file.write(elem+"\n")

def main(data_graph_path,pattern_path,pattern_level_path,output_path_arg,output_script,path_to_scripts,level,runs,time_interval,max_time,selected,iu):
    batch_name=os.path.split(os.path.dirname(output_path_arg))[1]
    approaches=['exhaustive','random_vertex','furer','false_furer']
    #wall_time_string=str(wall_time_hours)+":"+str(wall_time_minutes)+":"+str(wall_time_seconds)
    
    #make directory worker_scripts
    worker_scripts_path=os.path.join(output_script,"worker_script")
    if(not os.path.exists(worker_scripts_path)):
        os.makedirs(worker_scripts_path)
    
    #make worker commands exhaustive file
    #exhaustive_data_worker_script_path=os.path.join(worker_scripts_path,"exhaustive_data.data")
    #worker_script_exhaustive_file=open(os.path.join(worker_scripts_path,"exhaustive_data.data"),'w')
    #header_exhaustive="data_graph_path,pattern_path,output_path\n"
    #worker_script_exhaustive_file.write(header_exhaustive)  
    header_samplings="data_graph_path,pattern_path,output_path,exhaustive_approach_results_path,runs,time_interval,max_time\n" 
    #make worker commands random vertex
    sampling_data_worker_script_path=os.path.join(worker_scripts_path,"param.data")
    worker_script_sampling_file=open(os.path.join(worker_scripts_path,"param.data"),'w')
    worker_script_sampling_file.write(header_samplings)

    commands_exhaustive=[]
    commands_random_vertex=[]
    commands_furer=[]
    commands_false_furer=[]
    selected_command=""
    if selected==True:
        selected_command=" -selected "
    
    print "PATTERN PATH: ",pattern_path
    for root, dirs, files in os.walk(pattern_path):
        print "FILES: ",files
        for file in files:
            if file.endswith('.gml'):
                output_path=os.path.join(output_path_arg,os.path.basename(file[:-4]))       
                if(not(os.path.exists(output_path))):
                    os.makedirs(output_path)   
                
                com_exhaustive='python '+path_to_scripts+'/exhaustive_approach.py'+' -data_graph_path '+data_graph_path+' -pattern_path '+os.path.join(root,file)+' -output_path '+output_path+"\n"
                com_random='python '+path_to_scripts+'/random_vertex_sampling_approach.py'+' -data_graph_path '+data_graph_path+' -pattern_path '+os.path.join(root,file)+' -output_path '+output_path+" -exhaustive_approach_results_path "+output_path+"/exhaustive_approach/ "+" -runs "+str(runs)+" -time_interval "+str(time_interval)+" -max_time "+str(max_time)+selected_command+"\n"    
                #worker_script_exhaustive_file.write(data_graph_path+","+os.path.join(root,file)+","+output_path+"\n")
                worker_script_sampling_file.write(data_graph_path+","+os.path.join(root,file)+","+output_path+","+output_path+"/exhaustive_approach/"+","+str(runs)+","+str(time_interval)+","+str(max_time)+"\n")    
                #commands_exhaustive.append(com_exhaustive)
                #commands_random_vertex.append(com_random)
                if iu==True:
                  commands_furer.append('python '+path_to_scripts+'/furer_sampling_approach.py'+' -data_graph_path '+data_graph_path+' -pattern_path '+os.path.join(root,file)+ ' -pattern_level_results '+pattern_level_path+  ' -output_path '+output_path+" -exhaustive_approach_results_path "+output_path+"/exhaustive_approach/ "+" -runs "+str(runs)+" -time_interval "+str(time_interval)+" -max_time "+str(max_time)+selected_command+" -iu"+"\n")
                else:
                  commands_furer.append('python '+path_to_scripts+'/furer_sampling_approach.py'+' -data_graph_path '+data_graph_path+' -pattern_path '+os.path.join(root,file)+ ' -pattern_level_results '+pattern_level_path+  ' -output_path '+output_path+" -exhaustive_approach_results_path "+output_path+"/exhaustive_approach/ "+" -runs "+str(runs)+" -time_interval "+str(time_interval)+" -max_time "+str(max_time)+selected_command+"\n")

                #commands_false_furer.append('python '+path_to_scripts+'/false_furer_sampling_approach.py'+' -data_graph_path '+data_graph_path+' -pattern_path '+os.path.join(root,file)+' -output_path '+output_path+" -exhaustive_approach_results_path "+output_path+"/exhaustive_approach/ "+" -runs "+str(runs)+" -time_interval "+str(time_interval)+" -max_time "+str(max_time)+selected_command+"\n")

    
    #worker_script_exhaustive_file.close()
    worker_script_sampling_file.close()
    path_for_commands_exhaustive=os.path.join(output_script,'commands_exhaustive')
    path_for_commands_random=os.path.join(output_script,'commands_random_vertex')
    path_for_commands_furer=os.path.join(output_script,'commands_furer')
    path_for_commands_false_furer=os.path.join(output_script,'commands_false_furer')
    
#     if not(os.path.exists(path_for_commands_exhaustive)):
#         os.makedirs(path_for_commands_exhaustive)
#         
#     if not(os.path.exists(path_for_commands_random)):
#         os.makedirs(path_for_commands_random)
        
    if not(os.path.exists(path_for_commands_furer)):
        os.makedirs(path_for_commands_furer)
        
#     if not(os.path.exists(path_for_commands_false_furer)):
#         os.makedirs(path_for_commands_false_furer)
    
    #split_commands(10,commands_exhaustive,path_for_commands_exhaustive,level,"exh_"+str(level)+"_"+batch_name)
    #split_commands(10,commands_random_vertex,path_for_commands_random,level,"rnd_"+str(level)+"_"+batch_name)
    split_commands(10,commands_furer,path_for_commands_furer,level,"fur_"+str(level)+"_"+batch_name)
    #split_commands(10,commands_false_furer,path_for_commands_false_furer,level,"ffur_"+str(level)+"_"+batch_name)


    #Make TEMPLATE FOR APPROACHES
#     with open(output_script+'template_exhaustive','w') as file:
#        com_exhaustive='python '+path_to_scripts+'/exhaustive_approach.py'+' -data_graph_path '+data_graph_path+' -pattern_path '+os.path.join(pattern_path,"$PATTERN","$PATTERN.gml")+' -output_path '+os.path.join(output_path_arg,"$PATTERN")+selected_command+"\n"
#        file.write(com_exhaustive)
#     
#     with open(output_script+'template_random','w') as file:
#         com_random='python '+path_to_scripts+'/random_vertex_sampling_approach.py'+' -data_graph_path '+data_graph_path+' -pattern_path '+os.path.join(pattern_path,"$PATTERN","$PATTERN.gml")+' -output_path '+os.path.join(output_path_arg,"$PATTERN")+" -exhaustive_approach_results_path "+os.path.join(output_path_arg,"$PATTERN","exhaustive_approach")+" -runs "+str(runs)+" -time_interval "+str(time_interval)+" -max_time "+str(max_time)+selected_command+"\n"
#         file.write(com_random)
    
    with open(output_script+'/template_furer','w') as file:
        com_furer='python '+path_to_scripts+'/furer_sampling_approach.py'+' -data_graph_path '+data_graph_path+' -pattern_path '+os.path.join(pattern_path,"$PATTERN","$PATTERN.gml")+' -pattern_level_results '+pattern_level_path+' -output_path '+os.path.join(output_path_arg,"$PATTERN")+" -exhaustive_approach_results_path "+os.path.join(output_path_arg,"$PATTERN","exhaustive_approach")+" -runs "+str(runs)+" -time_interval "+str(time_interval)+" -max_time "+str(max_time)+selected_command+"\n"
        file.write(com_furer)
        
#     with open(output_script+'template_ffurer','w') as file:
#         com_ffurer='python '+path_to_scripts+'/false_furer_sampling_approach.py'+' -data_graph_path '+data_graph_path+' -pattern_path '+os.path.join(pattern_path,"$PATTERN","$PATTERN.gml")+' -output_path '+os.path.join(output_path_arg,"$PATTERN")+" -exhaustive_approach_results_path "+os.path.join(output_path_arg,"$PATTERN","exhaustive_approach")+" -runs "+str(runs)+" -time_interval "+str(time_interval)+" -max_time "+str(max_time)+selected_command+"\n"
#         file.write(com_ffurer)
    
#     with open(output_script+'commands_exhaustive'+'_'+str(level)+'.list','w') as file:
#         for c in commands_exhaustive:
#             file.write(c+"\n")
#             
#     with open(output_script+'commands_random_vertex'+'_'+str(level)+'.list','w') as file:
#         for c in commands_random_vertex:
#             file.write(c+"\n")
            
    with open(output_script+'/commands_furer'+'_'+str(level)+'.list','w') as file:
        for c in commands_furer:
            file.write(c+"\n")
            
#     with open(output_script+'commands_false_furer'+'_'+str(level)+'.list','w') as file:
#         for c in commands_false_furer:
#             file.write(c+"\n")
    
    #Write worker script for all jobs exhaustive
    folder_job_arrays=os.path.join(output_script,'array_jobs')
    if not os.path.exists(folder_job_arrays):
        os.makedirs(folder_job_arrays)
    #create_job_array_script(folder_job_arrays, os.path.join(output_script+'commands_exhaustive'+'_'+str(level)+'.list'), nodes, ppn, node_type, "exhaustive_"+str(level))
    #create_worker_PBS_script_sampling(worker_scripts_path,sampling_data_worker_script_path,path_to_scripts,pattern_path,"rnd_"+str(level),"random_vertex_sampling_approach.py",selected,None)
    create_worker_PBS_script_sampling(worker_scripts_path,sampling_data_worker_script_path,path_to_scripts,pattern_path,"fur_"+str(level),"furer_sampling_approach.py",selected,pattern_level_path,iu)
    #create_worker_PBS_script_sampling(worker_scripts_path,sampling_data_worker_script_path,path_to_scripts,pattern_path,"ffur_"+str(level),"false_furer_sampling_approach.py",selected,None)
    #file_name_exhaustive=create_worker_PBS_script_exhaustive(worker_scripts_path,sampling_data_worker_script_path,path_to_scripts,pattern_path,"exh_"+str(level))
    
    #Create bash script for calling worker scripts in sequence
    bash_for_worker=open(os.path.join(worker_scripts_path,"test.sh"),'w')
    bash_for_worker.write("#!/bin/bash -l\n")
    #bash_for_worker.write("wsub -batch "+file_name_exhaustive+" -data "+exhaustive_data_worker_script_path+"\n")
    bash_for_worker.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-data_graph_path', metavar='N',help='path to data graph')
    parser.add_argument('-pattern_path', metavar='N',help='path to patterns to be processed')
    parser.add_argument('-pattern_level_path', metavar='N',help='path to patterns to be processed')
    parser.add_argument('-output_path', metavar='N',help='output path where results will be stored when commands ran')
    parser.add_argument('-output_script', metavar='N',help='path where the scripts will be saved')
    parser.add_argument('-path_to_scripts', metavar='N',help='path to execution script (for doing the counts)')
    parser.add_argument('-level', metavar='N',help='generate commands for Nth level of nodes in pattern lattice')
    parser.add_argument('-runs', metavar='N',type=int,help='number of runs for sampling approaches')
    parser.add_argument('-time_interval', metavar='N',type=int,help='time interval for result reporting (in seconds)')
    parser.add_argument('-max_time', metavar='N',type=int,help='max experiment time (in seconds)')
    parser.add_argument('-iu',default=False,action='store_true',help='ignore upper bound')
    parser.add_argument('-selected',default=False,action='store_true',help='do approximate approach only if the pattern is selected by the exhaustive approach')
    
    args = parser.parse_args()
    if args.level==None:
        raise Exception('specify the level')
    main(args.data_graph_path,args.pattern_path,args.pattern_level_path,args.output_path,os.path.join(args.output_script,"sampling"),args.path_to_scripts,args.level,args.runs,args.time_interval,args.max_time,args.selected,args.iu)
    #generate_commands_for_selected.main(args.data_graph_path,args.pattern_path,args.pattern_level_path,args.output_path,os.path.join(args.output_script,"selected_patterns"),args.path_to_scripts,args.level,args.runs,args.time_interval,args.max_time,args.selected)
    
