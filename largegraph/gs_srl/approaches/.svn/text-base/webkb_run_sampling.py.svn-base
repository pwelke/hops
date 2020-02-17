'''
Created on Oct 4, 2016

@author: irma
'''
'''
Created on Sep 28, 2016

@author: irma
'''
import os
import subprocess
batch=1
patterns_size=5
while True:
    if batch==1: #already created so just do the sampling
       #subprocess.call("python /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/generate_patterns/generate_patterns_from_selected.py -data_graph /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/DATA/WEBKB/webkb.gml -output /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_WEBKB//patterns_size_"+str(patterns_size)+"/batch1/ -exp webkb -results_previous_level /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_WEBKB/patterns_size_"+str(patterns_size-1)+"/ -previous_level "+str(patterns_size-1)+" -data_set_short_label webkb -patterns_previous_level /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_WEBKB//patterns_size_"+str(patterns_size-1)+"/",shell=True)
       subprocess.call("python /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/generate_commands.py -data_graph_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/DATA/WEBKB/webkb.gml -pattern_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_WEBKB//patterns_size_"+str(patterns_size)+"/batch1/ -output_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_WEBKB/patterns_size_"+str(patterns_size)+"/batch1/ -output_script /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(patterns_size)+"/batch1/ -path_to_scripts /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/ -runs 1 -time_interval 300 -level "+str(patterns_size)+" -max_time 36000 -pattern_level_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_WEBKB/patterns_size_"+str(patterns_size)+"/",shell=True)
       subprocess.call("wsub -l walltime=06:00:00 -l nodes=5:ppn=20:ivybridge,pmem=3gb -N "+str(patterns_size)+"_wk_"+str(batch)+"_smpl -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/sampling/worker_script/fur_"+str(patterns_size)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/sampling/worker_script/param.data -A lp_dtai1",shell=True)
    else:
        print "/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_WEBKB//patterns_size_"+str(patterns_size)+"/batch"+str(batch-1)
        generate_batch="python /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/create_new_batch.py -batch_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_WEBKB//patterns_size_"+str(patterns_size)+"/batch"+str(batch-1)+"/ -pattern_level "+str(patterns_size)+" -batch_number "+str(batch-1)+" -output /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_WEBKB//patterns_size_"+str(patterns_size)+"/ -data_label webkb -N 400"
        generate_commands="python /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/generate_commands.py -data_graph_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/DATA/WEBKB/webkb.gml -pattern_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_WEBKB//patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/ -output_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_WEBKB/patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/ -output_script /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/ -path_to_scripts /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/ -runs 1 -time_interval 300 -level "+str(patterns_size)+" -max_time 36000 -pattern_level_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_WEBKB/patterns_size_"+str(patterns_size)+"/"
        run_sampling="wsub -l walltime=06:00:00 -l nodes=5:ppn=20:ivybridge,pmem=3gb -N fur_"+str(patterns_size)+"_wk_b"+str(batch)+"_smpl -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/sampling/worker_script/fur_"+str(patterns_size)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/sampling/worker_script/param.data -A lp_dtai1"
        #print "================================================"
        #print generate_batch
        #print generate_commands
        #print run_sampling
        #print "+++++++++++++++++++++++++++++++++++++++++++++++++"
        subprocess.call(generate_batch, shell=True,)
        subprocess.call(generate_commands, shell=True)
        subprocess.call(run_sampling, shell=True,stdin=None, stdout=None, stderr=None)
    
    batch+=1
    
    if batch>10:
        break
        
    with open("/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_WEBKB//patterns_size_"+str(patterns_size)+"/selected_patterns.info","r") as f:
        nr_selected=int(f.readline())
        if nr_selected>=100:
            break
    