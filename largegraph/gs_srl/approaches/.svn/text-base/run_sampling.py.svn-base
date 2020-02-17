'''
Created on Sep 28, 2016

@author: irma
'''
import os
import subprocess
batch=49
patterns_size=10
while True:
    if batch==1: #already created so just do the sampling
       subprocess.call("python /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/generate_patterns/generate_patterns_from_selected.py -data_graph /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/DATA/IMDB/imdb.gml -output /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB//patterns_size_"+str(patterns_size)+"/batch1/ -exp imdb -results_previous_level /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_IMDB/patterns_size_"+str(patterns_size-1)+"/ -previous_level "+str(patterns_size-1)+" -data_set_short_label imdb -patterns_previous_level /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB//patterns_size_"+str(patterns_size-1)+"/",shell=True)
       subprocess.call("python /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/generate_commands.py -data_graph_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/DATA/IMDB/imdb.gml -pattern_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB//patterns_size_"+str(patterns_size)+"/batch1/ -output_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_IMDB/patterns_size_"+str(patterns_size)+"/batch1/ -output_script /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(patterns_size)+"/batch1/ -path_to_scripts /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/ -runs 1 -time_interval 5 -level "+str(patterns_size)+" -max_time 300 -pattern_level_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB/patterns_size_"+str(patterns_size)+"/",shell=True)
       subprocess.call("wsub -l walltime=00:30:00 -l nodes=5:ppn=20:ivybridge -N "+str(patterns_size)+"_imdb_batch"+str(batch)+"_smpl -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/sampling/worker_script/fur_"+str(patterns_size)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/sampling/worker_script/param.data -A lp_dtai1",shell=True)
    else:
        print "/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB//patterns_size_"+str(patterns_size)+"/batch"+str(batch-1)
        generate_batch="python /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/create_new_batch.py -batch_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB//patterns_size_"+str(patterns_size)+"/batch"+str(batch-1)+"/ -pattern_level "+str(patterns_size)+" -batch_number "+str(batch-1)+" -output /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB//patterns_size_"+str(patterns_size)+"/ -data_label imdb -N 400"
        generate_commands="python /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/generate_commands.py -data_graph_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/DATA/IMDB/imdb.gml -pattern_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB//patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/ -output_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_IMDB/patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/ -output_script /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/ -path_to_scripts /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/ -runs 1 -time_interval 5 -level "+str(patterns_size)+" -max_time 300 -pattern_level_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB/patterns_size_"+str(patterns_size)+"/"
        run_sampling="wsub -l walltime=00:30:00 -l nodes=5:ppn=20:ivybridge -N fur_"+str(patterns_size)+"_imdb_batch"+str(batch)+"_smpl -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/sampling/worker_script/fur_"+str(patterns_size)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(patterns_size)+"/batch"+str(batch)+"/sampling/worker_script/param.data -A lp_dtai1"
        #print "================================================"
        #print generate_batch
        #print generate_commands
        #print run_sampling
        #print "+++++++++++++++++++++++++++++++++++++++++++++++++"
        subprocess.call(generate_batch, shell=True,)
        subprocess.call(generate_commands, shell=True)
        subprocess.call(run_sampling, shell=True,stdin=None, stdout=None, stderr=None)
    
    batch+=1
    
    if batch>53:
        break
        
    with open("/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB//patterns_size_"+str(patterns_size)+"/selected_patterns.info","r") as f:
        nr_selected=int(f.readline())
        if nr_selected>=100:
            break
    