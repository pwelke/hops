'''
Created on Feb 8, 2016

@author: irma
'''
import os,subprocess

allPaths=[]
generalPathJupiter="/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/"
allPaths.append('/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_DBLP/RESULTS_400_BATCH/patterns_size_4/')
allPaths.append('/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_DBLP/RESULTS_400_BATCH/patterns_size_5/')
allPaths.append('/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_DBLP/RESULTS_400_BATCH/patterns_size_6/')
allPaths.append('/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_DBLP/RESULTS_400_BATCH/patterns_size_7/')
allPaths.append('/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_DBLP/RESULTS_400_BATCH/patterns_size_8/')
allPaths.append('/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_DBLP/RESULTS_400_BATCH/patterns_size_9/')
allPaths.append('/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_DBLP/RESULTS_400_BATCH/patterns_size_10/')
allPaths.append('/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_DBLP/RESULTS_400_BATCH/patterns_size_11/')
allPaths.append('/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_DBLP/RESULTS_400_BATCH/patterns_size_12/')
allPaths.append('/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_DBLP/RESULTS_400_BATCH/patterns_size_13/')
allPaths.append('/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_DBLP/RESULTS_400_BATCH/patterns_size_14/')
allPaths.append('/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_DBLP/RESULTS_400_BATCH/patterns_size_15/')

furerInterrupted=[]
ffurerInterrupted=[]
randomInterrupted=[]

for p in allPaths:
    path_to_pattern=p.replace("RESULTS","PATTERNS")
    list_of_selected_patterns=os.path.join(path_to_pattern,'selected_patterns_list.info')
    print list_of_selected_patterns
    with open(list_of_selected_patterns,'r') as r:
        lines = r.readlines()
        for line in lines:
            if not os.path.exists(os.path.join(line.rstrip(),'results_furer','complete.info')):
                furerInterrupted.append(line)
            if not os.path.exists(os.path.join(line.rstrip(),'results_false_furer','complete.info')):
                ffurerInterrupted.append(line)
            if not os.path.exists(os.path.join(line.rstrip(),'random_vertex_approach','complete.info')):
                randomInterrupted.append(line)
with open('furerInterrupted_DBLP.info','w') as f: 
     for inter in furerInterrupted:
         path_pattern=inter.replace("RESULTS","PATTERNS")
         f.write(path_pattern+"\n")
         
with open('ffurerInterrupted_DBLP.info','w') as f: 
     for inter in ffurerInterrupted:
         path_pattern=inter.replace("RESULTS","PATTERNS")
         f.write(path_pattern+"\n")
         
with open('randomInterrupted_DBLP.info','w') as f: 
     for inter in randomInterrupted:
         path_pattern=inter.replace("RESULTS","PATTERNS")
         f.write(path_pattern+"\n")
    

    