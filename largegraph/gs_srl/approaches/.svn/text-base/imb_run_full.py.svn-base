'''
Created on Oct 19, 2016

@author: irma
'''
import os
import subprocess
batch=1
init=10
patterns_size=10
for i in xrange(10,11):
        subprocess.call("python /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/generate_commands_for_selected.py -data_graph_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/DATA/IMDB/imdb.gml -pattern_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB//patterns_size_"+str(i)+"/ -output_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_IMDB/patterns_size_"+str(i)+"/ -output_script /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(i)+"/ -path_to_scripts /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/ -runs 1 -time_interval 5 -level "+str(i)+" -max_time 600 -pattern_level_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB//patterns_size_"+str(i)+"/ -fo /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_IMDB/patterns_size_"+str(i)+"/",shell=True)
        subprocess.call("wsub -l walltime=00:20:00 -l nodes=5:ppn=20:ivybridge -N fur_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(i)+"/selected_patterns/worker_script/fur_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)
        subprocess.call("wsub -l walltime=00:20:00 -l nodes=5:ppn=20:ivybridge -N ffur_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(i)+"/selected_patterns/worker_script/ffur_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)
        subprocess.call("wsub -l walltime=00:20:00 -l nodes=5:ppn=20:ivybridge -N rnd_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(i)+"/selected_patterns/worker_script/rnd_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)
        subprocess.call("wsub -l walltime=00:20:00 -l nodes=5:ppn=20:ivybridge -N exh_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(i)+"/selected_patterns/worker_script/exh_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)