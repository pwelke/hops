import csv
import math
import sys

import networkx as nx

from OBDs import OBDsearch
from inference import ground_target_predicate as gtp
from sampling_core import furer_sampling_algorithm


def furer_OBD(pattern,data_graph,OBdecomp,root_node):
    interval_length = int(math.ceil((sys.maxint / 15)))
    intervals = [1]
    for i in range(1, 15):
        intervals.append(intervals[i - 1] + interval_length + 1)
    nr_embeddings = 0
    NLIMIT_values = intervals
    monitoring= furer_sampling_algorithm.get_nr_embedding(data_graph, pattern, OBdecomp, root_node, NLIMIT_values)
    return monitoring.report_structures[0].current_fdict


def generate_csv_exact_counts(data_graph,target_attr,target_constant,OBDTarget,root_node_target,patterns,OBDPatterns,root_nodes_patterns,csvfile,fieldnames):
    #get all groundings of the target predicate
    tg = gtp.find_all_groundings_of_predicates(data_graph, target_attr, target_constant)
    #for each ground target, ground all patterns and perfom counting, output a csv row
    with open(csvfile, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for target in tg:
            dict_res={}
            nr_target=furer_OBD(target, data_graph, OBDTarget, root_node_target)
            #print nr_target
            dict_res['target']=nr_target
            fieldcounter=1
            for pattern,OBD,root_node in zip(patterns,OBDPatterns,root_nodes_patterns):
                ground_pattern = gtp.ground_pattern(target, pattern)
                nr_pat=furer_OBD(ground_pattern, data_graph, OBD, root_node)
                dict_res[fieldnames[fieldcounter]]=nr_pat
                fieldcounter=fieldcounter+1
            writer.writerow(dict_res)


if __name__ == '__main__':
    data_graph = '/home/irma/work/DATA/DATA/yeast/YEAST_equiv.gpickle'
    data_graph = nx.read_gpickle(data_graph)
    tg=gtp.find_all_groundings_of_predicates(data_graph, 'function','constant')[0]
    pattern=nx.read_gml('/home/irma/work/DATA/DATA/yeast/pattern1.gml')
    ground_pattern = gtp.ground_pattern(tg, pattern)

    OBD1 = OBDsearch.get_heuristic4_OBD(pattern, startNode = 4)
    target_attr='function'
    target_constant='constant'
    root_node_target='function'
    OBDTarget=[[1],[2]]

    patterns=[pattern]
    OBDPatterns=[OBD1]
    root_nodes_patterns=['protein_class']
    csvfile='/home/irma/work/DATA/DATA/yeast/test.csv'
    fieldnames=['target','patt1']


    generate_csv_exact_counts(data_graph, target_attr, target_constant, OBDTarget, root_node_target, patterns,
                              OBDPatterns, root_nodes_patterns, csvfile, fieldnames)
    #print exact_counting(tg, data_graph,OBD,'function')
    #print exact_counting(ground_pattern, data_graph, OBD1,'protein_class')