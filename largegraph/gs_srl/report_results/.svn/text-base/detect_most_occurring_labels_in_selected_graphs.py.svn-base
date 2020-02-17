'''
Created on Feb 9, 2016

@author: irma
'''
import os,argparse,operator
import graph_manipulator.graph_analyzer as g
import networkx as nx


def main(path_to_data_graph,path_to_results,output_path,init_pattern_size,end_pattern_size):
    labels=g.get_sorted_labels_by_occurence_frequency_in_graph(path_to_data_graph)
    freq={}
    freq_not_selected={}
    D=nx.read_gpickle(path_to_data_graph)
    label_values={}
    for l in labels:
       label_values[l]=g.get_all_possible_nodes_wtih_values_in_data_graph(D,l[0])
    for i in xrange(init_pattern_size,end_pattern_size+1):
        path_results=os.path.join(path_to_results,"patterns_size_"+str(i))
        #list batches
        for batch in os.listdir(path_results):
            if(not batch.startswith("batch")):
                continue
            else:
                print os.path.join(path_to_results,"patterns_size_"+str(i),str(batch))
                #list patterns in the batch
                for p in os.listdir(os.path.join(path_to_results,"patterns_size_"+str(i),str(batch))):
                    path_to_pattern=os.path.join(os.path.join(path_to_results,"patterns_size_"+str(i),str(batch)),p,"input_pattern.gml")
                    if not (os.path.exists(path_to_pattern)):
                        continue
                    pattern=nx.read_gml(path_to_pattern)
                    if not os.path.exists(os.path.join(os.path.join(path_to_results,"patterns_size_"+str(i),str(batch)),p,"selected.info")):
                        for node in pattern.nodes():
                            if 'valueinpattern' in pattern.node[node].keys():
                                if pattern.node[node]['valueinpattern']==1:
                                   if not pattern.node[node]['value'] in freq_not_selected.keys():
                                    freq_not_selected[pattern.node[node]['value']]=1
                                   else:
                                    freq_not_selected[pattern.node[node]['value']]+=1
                    else:
                        for node in pattern.nodes():
                            if 'valueinpattern' in pattern.node[node].keys():
                                if pattern.node[node]['valueinpattern']==1:
                                    if not pattern.node[node]['value'] in freq.keys():
                                        freq[pattern.node[node]['value']]=1
                                    else:
                                        freq[pattern.node[node]['value']]+=1
    sorted_x = sorted.reverse(freq.items(), key=operator.itemgetter(1))             
    sorted_x_NS = sorted.reverse(freq_not_selected.items(), key=operator.itemgetter(1))                    
    
    with open(os.path.join(output_path,"randvarValuesFreqSelected.info")) as file:
        for f in sorted_x:
             file.write(f+"\n")
             
    with open(os.path.join(output_path,"randvarValuesFreqNotSelected.info")) as file:
        for f in sorted_x_NS:
             file.write(f+"\n")
    
    




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-D',help='path to data graph')
    parser.add_argument('-R',help='path to results')
    parser.add_argument('-O',help='output path')
    parser.add_argument('-I',type=int,help='init pattern size')
    parser.add_argument('-E',type=int,help='end pattern size')
    
    args = parser.parse_args()
    main(args.D,args.R,args.O,args.I,args.E)
     

