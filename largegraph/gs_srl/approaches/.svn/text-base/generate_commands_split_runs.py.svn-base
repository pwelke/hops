'''
Created on May 15, 2015

This script is created to make commands that will 
run the ten runs of sampling approaches in parallel. Might need this for
bigger patterns that take the maximum time. Or if we decide to use
time as stopping criteria

@author: irma
'''
import argparse,os


def create_PBS_script(pbs_script_folder,command_file_to_xargs,counter,nr_nodes,nr_processes_per_node,node_type,experiment_name): 
    global wall_time_string     
    file=pbs_script_folder+"/pbs_block_"+str(counter)+"_"+experiment_name.replace(" ","_")+".pbs"
    with open(file,'w') as f:
        f.write("#!/bin/bash -l\n")
        f.write("module load Python/2.7.6-foss-2014a\n")
        f.write("#PBS -N "+experiment_name+"\n")
        f.write("#PBS -l nodes="+str(nr_nodes)+":ppn="+str(nr_processes_per_node)+":"+str(node_type)+"\n")
        f.write("#PBS -l walltime="+wall_time_string+"\n")
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
        f.write("xargs -a " +command_file_to_xargs+" -P 4 -I COMMAND sh -c ""COMMAND"" 1> $LOGSTDOUT 2> $LOGSTDERR\n")
        f.write("rm pbs_*\n")

    

def split_commands(Max,commands,path,pattern_size,nr_nodes,nr_processes_per_node,node_type,experiment_name):
    split=[commands[i:i+Max] for i in range(0,len(commands),Max)]
    pbs_script_folder=os.path.join(path,"PBS_scripts")
    if(not(os.path.exists(pbs_script_folder))):
        os.makedirs(pbs_script_folder)
    
    counter=1
    print "Number of blocks",len(split)
    for block in split:
       with open(path+"/commands_pattern_"+str(pattern_size)+"_"+str(counter)+".c_block",'w') as file:
           create_PBS_script(pbs_script_folder,path+"/commands_pattern_"+str(pattern_size)+"_"+str(counter)+".c_block",counter,nr_nodes,nr_processes_per_node,node_type,experiment_name)
           counter+=1
           for elem in block:
               file.write(elem+"\n")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-data_graph_path', metavar='N',help='path to data graph')
    parser.add_argument('-pattern_path', metavar='N',help='path to patterns to be processed')
    parser.add_argument('-output_path', metavar='N',help='output path where results will be stored when commands ran')
    parser.add_argument('-output_script', metavar='N',help='path where the scripts will be saved')
    parser.add_argument('-path_to_scripts', metavar='N',help='path to execution script (for doing the counts)')
    parser.add_argument('-level', metavar='N',help='generate commands for Nth level of nodes in pattern lattice')
    parser.add_argument('-nodes', metavar='N',help='nr of nodes (for PBS script)')
    parser.add_argument('-ppn', metavar='N',help='processes per node')
    parser.add_argument('-node_type', metavar='N',help='type of computation node')
    parser.add_argument('-runs', metavar='N',type=int,help='number of runs for sampling approaches')
    parser.add_argument('-time_interval', metavar='N',type=int,help='time interval for result reporting (in seconds)')
    parser.add_argument('-max_time', metavar='N',type=int,help='max experiment time (in seconds)')
    parser.add_argument('-wall_time_hours', metavar='N',default='10',help='wall time hours')
    parser.add_argument('-wall_time_minutes', metavar='N',default='00',help='wall time minutes')
    parser.add_argument('-wall_time_seconds', metavar='N',default='00',help='wall time seconds')
    args = parser.parse_args()
    
    if args.level==None:
        raise Exception('specify the level')
    
   
    batch_name=os.path.split(os.path.dirname(args.output_path))[1]
    approaches=['exhaustive','random_vertex','furer','false_furer']
    
    runs=args.runs

    wall_time_string=str(args.wall_time_hours)+":"+str(args.wall_time_minutes)+":"+str(args.wall_time_seconds)
    commands_exhaustive=[]
    commands_random_vertex=[]
    commands_furer=[]
    commands_false_furer=[] 
    print " Number of patterns in this level: ",len(os.listdir(args.pattern_path))
    
    #Go through all patterns and all sampling approaches runs
    for dir in os.listdir(args.pattern_path):
            if os.path.isfile(os.path.join(args.pattern_path,dir)):
                continue
            for file in os.listdir(os.path.join(args.pattern_path,dir)):
                root=os.path.join(args.pattern_path,dir)
                if file.endswith('.gml'):
                    #exhaustive approach doesn't have multiple runs
                   output_exhaustive=os.path.join(args.output_path,os.path.basename(file[:-4]))
                   commands_exhaustive.append('python '+args.path_to_scripts+'/exhaustive_approach.py'+' -data_graph_path '+args.data_graph_path+' -pattern_path '+os.path.join(root,file)+' -output_path '+output_exhaustive+"\n")
                   #make separate runs
                   for i in xrange(1,11):
                        output_path=os.path.join(args.output_path,os.path.basename(file[:-4]),'run_'+str(i))
                        
                        if(not(os.path.exists(output_path))):
                            os.makedirs(output_path)
                            
                        commands_random_vertex.append('python '+args.path_to_scripts+'/random_vertex_sampling_approach.py'+' -data_graph_path '+args.data_graph_path+' -pattern_path '+os.path.join(root,file)+' -output_path '+output_path+" -exhaustive_approach_results_path "+output_exhaustive+"/exhaustive_approach/ "+" -runs "+str(1)+" -time_interval "+str(args.time_interval)+" -max_time "+str(args.max_time)+" -run_nr "+str(i)+"\n")
                        commands_furer.append('python '+args.path_to_scripts+'/furer_sampling_approach.py'+' -data_graph_path '+args.data_graph_path+' -pattern_path '+os.path.join(root,file)+' -output_path '+output_path+" -exhaustive_approach_results_path "+output_exhaustive+"/exhaustive_approach/ "+" -runs "+str(1)+" -time_interval "+str(args.time_interval)+" -max_time "+str(args.max_time)+" -run_nr "+str(i)+"\n")
                        commands_false_furer.append('python '+args.path_to_scripts+'/false_furer_sampling_approach.py'+' -data_graph_path '+args.data_graph_path+' -pattern_path '+os.path.join(root,file)+' -output_path '+output_path+" -exhaustive_approach_results_path "+output_exhaustive+"/exhaustive_approach/ "+" -runs "+str(1)+" -time_interval "+str(args.time_interval)+" -max_time "+str(args.max_time)+" -run_nr "+str(i)+"\n")
        
    nr_commands=0
    nr_commands+=len(commands_exhaustive) 
    nr_commands+=len(commands_random_vertex)
    nr_commands+=len(commands_furer)    
    nr_commands+=len(commands_false_furer) 
    
    print " Overall number of commands: ",nr_commands
    
    print "Splitting in blocks. ..."
        
    path_for_commands_exhaustive=os.path.join(args.output_script,'parallel_commands_pattern_'+str(args.level),'commands_exhaustive')
    path_for_commands_random=os.path.join(args.output_script,'parallel_commands_pattern_'+str(args.level),'commands_random_vertex')
    path_for_commands_furer=os.path.join(args.output_script,'parallel_commands_pattern_'+str(args.level),'commands_furer')
    path_for_commands_false_furer=os.path.join(args.output_script,'parallel_commands_pattern_'+str(args.level),'commands_false_furer')
    
    if not(os.path.exists(path_for_commands_exhaustive)):
        os.makedirs(path_for_commands_exhaustive)
        
    if not(os.path.exists(path_for_commands_random)):
        os.makedirs(path_for_commands_random)
        
    if not(os.path.exists(path_for_commands_furer)):
        os.makedirs(path_for_commands_furer)
        
    if not(os.path.exists(path_for_commands_false_furer)):
        os.makedirs(path_for_commands_false_furer)
        
    split_commands(10,commands_exhaustive,path_for_commands_exhaustive,args.level,args.nodes,args.ppn,args.node_type,"exhaustive_"+str(args.level)+"_"+batch_name)
    split_commands(10,commands_random_vertex,path_for_commands_random,args.level,args.nodes,args.ppn,args.node_type,"random vertex_"+str(args.level)+"_"+batch_name)
    split_commands(10,commands_furer,path_for_commands_furer,args.level,args.nodes,args.ppn,args.node_type,"furer_"+str(args.level)+"_"+batch_name)
    split_commands(10,commands_false_furer,path_for_commands_false_furer,args.level,args.nodes,args.ppn,args.node_type,"false_furer_"+str(args.level)+"_"+batch_name)
    
    with open(args.output_script+'parallel_commands_exhaustive'+'_'+str(args.level)+'.txt','w') as file:
        for c in commands_exhaustive:
            file.write(c)
            
    with open(args.output_script+'parallel_commands_random_vertex'+'_'+str(args.level)+'.txt','w') as file:
        for c in commands_random_vertex:
            file.write(c)
            
    with open(args.output_script+'parallel_commands_furer'+'_'+str(args.level)+'.txt','w') as file:
        for c in commands_furer:
            file.write(c)
            
    with open(args.output_script+'parallel_commands_false_furer'+'_'+str(args.level)+'.txt','w') as file:
        for c in commands_false_furer:
            file.write(c)

    