import csv

import networkx as nx

from OBDs import OBDsearch
from algorithms import exhaustive_approach
from inference import ground_target_predicate as gtp


def exact_counting(pattern,data_graph,OBdecomp,root_node):
    emb=exhaustive_approach.get_nr_embeddings(data_graph, pattern, OBdecomp, root_node)
    return emb


def generate_monitoring_marks(time_interval_in_seconds,max_time_in_seconds):
    counter=0
    marks=[]
    while counter+time_interval_in_seconds<=max_time_in_seconds:
        marks.append(counter+time_interval_in_seconds)
        counter=counter+time_interval_in_seconds
    return marks

def generate_csv_exact_counts(data_graph,target_attr,target_constant,OBDTarget,root_node_target,patterns,OBDPatterns,root_nodes_patterns,csvfile,fieldnames):
    #get all groundings of the target predicate
    #for n in data_graph.nodes():
    #    if n==12:
    #        print data_graph.node[n]
    tg = gtp.find_all_groundings_of_predicates(data_graph, target_attr, target_constant)[1:100]
    #for each ground target, ground all patterns and perfom counting, output a csv row
    with open(csvfile, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for target in tg:
            #if not (target.node[2]['value']=='Protein_YAL005c' and target.node[1]['value']=='Func_id_1'):
            #    continue
            dict_res={}
            nr_target=exact_counting(target, data_graph, OBDTarget, root_node_target)
            if nr_target>0:
                nr_target=1
            else:
                nr_target=0
            dict_res['target']=nr_target
            fieldcounter=1
            for pattern,OBD,root_node in zip(patterns,OBDPatterns,root_nodes_patterns):
                ground_pattern = gtp.ground_pattern(target, pattern)
                nr_pat=exact_counting(ground_pattern, data_graph, OBD, root_node)
                dict_res[fieldnames[fieldcounter]]=nr_pat
                fieldcounter=fieldcounter+1
            writer.writerow(dict_res)


if __name__ == '__main__':
    data_graph = '/home/irma/work/DATA/DATA/YEAST_equiv.gpickle'
    data_graph = nx.read_gpickle(data_graph)
    tg=gtp.find_all_groundings_of_predicates(data_graph, 'function','constant')[0]
    pattern=nx.read_gml('/home/irma/work/DATA/DATA/yeast/pattern2.gml')
    ground_pattern = gtp.ground_pattern(tg, pattern)

    OBD1 = OBDsearch.get_heuristic4_OBD(pattern, startNode = 0)
    target_attr='function'
    target_constant='constant'
    root_node_target='function'
    OBDTarget=[[1],[2]]

    patterns=[pattern]
    OBDPatterns=[OBD1]
    root_nodes_patterns=['protein_class']
    csvfile='/home/irma/work/DATA/DATA/yeast/test.csv'
    fieldnames=['target','patt2']
    #generate_csv_furerOBD_counts(data_graph, target_attr, target_constant, OBDTarget, root_node_target, patterns,OBDPatterns, root_nodes_patterns, csvfile, fieldnames)
    generate_csv_exact_counts(data_graph, target_attr, target_constant, OBDTarget, root_node_target, patterns,
                                 OBDPatterns, root_nodes_patterns, csvfile, fieldnames)
    #print exact_counting(tg, data_graph,OBD,'function')
    #print exact_counting(ground_pattern, data_graph, OBD1,'protein_class')