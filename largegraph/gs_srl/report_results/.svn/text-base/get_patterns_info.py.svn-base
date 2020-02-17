'''
Created on Jul 27, 2015

@author: irma
'''
import argparse
import os
import shutil
import pickle
import networkx as nx
import graph_manipulator.graph_analyzer as man
import csv
import re
import numpy

def contains_predicate(pattern,predicate):
    for node in pattern.nodes():
        if pattern.node[node]['predicate']==predicate:
            return True
    return False

def is_invalid(pattern_path):
    if os.path.isfile(os.path.join(pattern_path,'invalid.info')):
        return True
    return False

def graph_characteristics_csv(pattern_path, output_path,predicate):
     csv_folder_summary=os.path.join(output_path,'graph_characteristics_csv')
     if not os.path.exists(csv_folder_summary):
        os.makedirs(csv_folder_summary)
     batch_number=pattern_path.split("/")[-1] 
     file=csv_folder_summary+"/"+batch_number+'_results_final_limit.csv'
     print "Making file: ",file
     b = open(file, 'w')
     if predicate!=None:
       field_names=['pattern_name','nr_randvar_values','nr_targets','has_cycles','max_degree','average_degree','predicate'+predicate,'invalid']
     else:
       field_names=['pattern_name','nr_randvar_values','nr_targets','has_cycles','max_degree','average_degree','invalid']

     writer = csv.DictWriter(b, fieldnames=field_names)
     writer.writeheader()
     pattern_file_gml=None
     print "Number of patterns: ",len(sorted(os.listdir(pattern_path),key = lambda x: x[:-5]))
     
     for patt in sorted(os.listdir(pattern_path),key = lambda x: x[:-5]):
        #print os.path.join(pattern_path,patt)
        if(os.path.isfile(os.path.join(pattern_path,patt))):
           continue
        pattern_file_gml=os.path.join(pattern_path,patt,patt+".gml")
        #if patt.endswith(".gml"):
        #    pattern_file_gml=os.path.join(pattern_path,patt)
        #print "Pattern file gml",pattern_file_gml
        if pattern_file_gml!=None:
            pattern=nx.read_gml(pattern_file_gml)
        else:
            continue
        pattern_file_name=patt
        #some general pattern charactersitics
        nr_randvar_values=man.count_nr_randvars_in_graph(pattern)
        cycles=man.is_there_cycle_in_graph(pattern)
        max_degree=man.get_maximum_node_degree(pattern)
        average_degree=man.get_average_node_degree(pattern)
        n_target_nodes=man.get_nr_target_nodes_other_than_head(pattern)
        contains_target_predicate=contains_predicate(pattern,predicate)
        
        row={}
        row['pattern_name']=pattern_file_name
        row['nr_randvar_values']=str(nr_randvar_values)
        row['nr_targets']=str(n_target_nodes)
        row['has_cycles']=str(cycles)
        row['max_degree']=str(max_degree)
        row['average_degree']=str(average_degree)
        row['invalid']=str(is_invalid(os.path.join(pattern_path,patt)))
        if predicate!=None:
           row['predicate'+predicate]=str(contains_target_predicate)
        writer.writerow(row)
     print "Finished writing csv ...to",file
     return file
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-pattern_path', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-output',help='in case results already processed for this batch redo is false by default unless specified true')
    parser.add_argument('-predicate', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')

    args = parser.parse_args() 
    graph_characteristics_csv(args.pattern_path,args.output,args.predicate)
    