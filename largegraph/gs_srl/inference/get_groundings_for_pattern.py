import argparse
import os
import sys

import networkx as nx

from OBDs import OBDsearch
from inference import count_exact_patterns as exact
from inference import count_patterns_furer_OBD as furer
from inference import ground_target_predicate as gtp


def get_pattern_paths(pattern_file):
    out=[]
    with open(pattern_file,'r') as f:
        for line in f:
           out.append(line.rstrip())
    return out

def get_pattern_infos(pattern_path):
    patterns = []
    OBDPatterns = []
    root_nodes_patterns = []
    indices = []
    equiv = []
    non_equiv = []

    pattern=nx.read_gml(os.path.join(pattern_path,'pattern.gml'))
    patterns.append(pattern)
    with open(os.path.join(pattern_path,'startNodeId.info')) as f:
        start_node=int(f.readline().rstrip())
    OBD = OBDsearch.get_heuristic4_OBD(pattern, startNode=start_node)
    OBDPatterns.append(OBD)
    with open(os.path.join(pattern_path,'rootNode.info')) as f:
        root_node=f.readline().rstrip()
    root_nodes_patterns.append(root_node)
    ind=[]
    with open(os.path.join(pattern_path,'indices.info')) as f:
        for line in f:
            ind.append(int(line.rstrip()))
    indices.append(ind)

    if not os.path.isfile(os.path.join(pattern_path,'equivalence.info')):
        equiv.append(None)
    else:
        indices_equiv=[]
        with open(os.path.join(pattern_path,'equivalence.info')) as f:
            for line in f:
                a=[]
                l=line.rstrip().split(" ")
                for elem in l:
                    a.append(int(elem))
                indices_equiv.append(a)
        equiv.append(indices_equiv)
    if not os.path.isfile(os.path.join(pattern_path,'non_equivalence.info')):
        non_equiv.append(None)
    else:
        indices_equiv=[]
        with open(os.path.join(pattern_path,'non_equivalence.info')) as f:
            for line in f:
                a=[]
                l=line.rstrip().split(" ")
                for elem in l:
                    a.append(int(elem))
                indices_equiv.append(a)
        non_equiv.append(indices_equiv)
    return patterns,OBDPatterns,root_nodes_patterns,indices,equiv,non_equiv




if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Run exhaustive approach')
        parser.add_argument('-train',help='path to train gpickle')
        parser.add_argument('-test', help='path to test gpickle')
        parser.add_argument('-o', help='output')
        parser.add_argument('-p', help='pattern path')
        parser.add_argument('-e', help='experiment: exact or furer')
        parser.add_argument('-const', help='constant for the target predicate. e.g., protein')
        parser.add_argument('-attr', help='attribute for the target predicate. e.g., function')
        parser.add_argument('-rT', help='root node target, e.g., function')
        parser.add_argument('-t',default=None, help='train,test or both')
        parser.add_argument('-sT', help='start node target, e.g., 2')
        parser.add_argument('-max_time',default=600, type=int,help='start node target, e.g., 2')
        args = parser.parse_args()
        if args.e=="furer":
            #first we need to read the dictionaries of exhaustive, if not there abort. We need that first
            try:
              time_train_dict=os.path.join(args.o,"exact",'time_dict_train.csv')
            except:
                print('Problem with time dictionary. Cannot run Furer. First run exhaustiive')
                sys.exit()
            try:
              time_test_dict=os.path.join(args.o,"exact",'time_dict_test.csv')
            except:
                print('Problem with time dictionary. Cannot run Furer. First run exhaustiive')
                sys.exit()
        runtime=args.max_time
        train_data = nx.read_gpickle(args.train)
        print("Training data loaded ...")
        test_data = nx.read_gpickle(args.test)
        print("Test data loaded ...")


        if args.e=="exact":
            experiment="exact_"+str(args.max_time)
        else:
            experiment="furer_"+str(args.max_time)

        output = os.path.join(args.o, experiment)
        if not os.path.isdir(output):
            os.makedirs(output)

        output_train_csv=os.path.join(args.o,experiment,'train.csv')
        output_test_csv = os.path.join(args.o,experiment, 'test.csv')
        time_dict_train_csv=os.path.join(args.o,experiment,'time_dict_train.csv')
        time_dict_test_csv=os.path.join(args.o, experiment, 'time_dict_test.csv')

        pattern_path=args.p
        patterns,OBDPatterns,root_nodes_patterns,indices,pattern_equivalence,non_equivalence=get_pattern_infos(pattern_path)
        target = gtp.get_target_graph(args.const, args.attr)
        OBDTarget = OBDsearch.get_heuristic4_OBD(target, startNode=int(args.sT))
        root_node_target = args.rT

        fieldnames=['dummy','target',patterns[0].name]
        if args.e=="exact":
                if args.t == None or (args.t != None and args.t == "train"):
                    exact.generate_csv_exact_counts(train_data,target,args.const,args.attr, OBDTarget, root_node_target, patterns, OBDPatterns,
                                          indices, root_nodes_patterns,pattern_equivalence,non_equivalence, output_train_csv, fieldnames,time_dict_train_csv,args.max_time)
                print("Training data counted ...")

                if args.t == None or (args.t != None and args.t == "test"):
                    exact.generate_csv_exact_counts(test_data, target,args.const,args.attr, OBDTarget, root_node_target, patterns, OBDPatterns,
                                            indices, root_nodes_patterns,pattern_equivalence,non_equivalence, output_test_csv, fieldnames,time_dict_test_csv,args.max_time)

                print("Test data counted ...")
        if args.e=="furer":
            # count train
                if args.t == None or (args.t!=None and args.t == "train"):
                    furer.generate_csv_furerOBD_count(train_data, target, args.const, args.attr, OBDTarget, root_node_target,
                                            patterns, OBDPatterns,
                                            indices, root_nodes_patterns, pattern_equivalence,non_equivalence,output_train_csv, fieldnames,
                                              time_train_dict,runtime)

            # count test
                if args.t == None or (args.t != None and args.t == "test"):
                    furer.generate_csv_furerOBD_count(test_data, target, args.const, args.attr, OBDTarget, root_node_target,
                                            patterns, OBDPatterns,
                                            indices, root_nodes_patterns, pattern_equivalence,non_equivalence,output_test_csv, fieldnames,
                                              time_test_dict,runtime)

        #model = inference.train_logistic_regression(output_train_csv)
        #inference.predict_logistic_regression(output_test_csv, model, output)



