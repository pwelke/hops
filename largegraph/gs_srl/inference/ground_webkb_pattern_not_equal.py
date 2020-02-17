import os
import shutil

import networkx as nx

from graph import graph_analyzer as an


def ground_pattern(pattern,groundings,node_ids):
    patterns=[]
    for g1 in groundings:
       for g2 in groundings:
           if g1==g2:
               continue
           pTemp=pattern.copy()
           pTemp.node[node_ids[0]]['valueinpattern']=1
           pTemp.node[node_ids[0]]['value'] = g1
           pTemp.node[node_ids[1]]['valueinpattern']=1
           pTemp.node[node_ids[1]]['value'] = g2
           patterns.append(pTemp)
    return patterns

def write_patterns(ground_patterns,path_to_files,counter_offset,output):
    counter=counter_offset
    for g in ground_patterns:
        pattern_name = "pattern" + str(counter)
        g.name=pattern_name
        output_path=os.path.join(output,pattern_name)
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
        nx.write_gml(g,os.path.join(output_path,"pattern.gml"))
        shutil.copy(os.path.join(path_to_files,'indices.info'),os.path.join(output_path,'indices.info'))
        shutil.copy(os.path.join(path_to_files,'rootNode.info'),os.path.join(output_path,'rootNode.info'))
        shutil.copy(os.path.join(path_to_files,'startNodeId.info'),os.path.join(output_path,'startNodeId.info'))
        if os.path.isfile(os.path.join(path_to_files,'equivalence.info')):
            shutil.copy(os.path.join(path_to_files, 'equivalence.info'), os.path.join(output_path, 'equivalence.info'))

        counter+=1


if __name__ == '__main__':
    data='/home/irma/work/DATA/INFERENCE_DATA/WEBKB/folds/fold1-train.gpickle'
    pattern_path='/home/irma/work/DATA/INFERENCE_DATA/WEBKB/experiments_inference/page_class/General_patterns/pattern3/'
    output='/home/irma/work/DATA/INFERENCE_DATA/WEBKB/experiments_inference/page_class/PATTERNS/'
    general_path_file='/home/irma/work/DATA/INFERENCE_DATA/WEBKB/experiments_inference/page_class/patterns.info'
    data_graph=nx.read_gpickle(data)
    pattern=nx.read_gml(os.path.join(pattern_path,'pattern.gml'))
    groundings=an.get_all_possible_values(data_graph, 'word')
    ground_patterns=ground_pattern(pattern, groundings, [4,6])
    write_patterns(ground_patterns,pattern_path,52,output)
    #write file with all the patterns
    dirs=os.listdir(output)
    dirs.sort(key=lambda f: int(filter(str.isdigit, f)))
    with open(general_path_file,'w') as fajl:
        for d in dirs:
                if "pattern" in d:
                    fajl.write(os.path.join(output,d)+"\n")


